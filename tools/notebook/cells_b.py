CELLS = []


def md(text):
    CELLS.append(("md", text))


def code(text):
    CELLS.append(("code", text))


# ---------------------------------------------------------------- 4. Engenharia de features
md(r'''
---
# 4. Engenharia de Features

As colunas originais nem sempre expressam as ideias que interessam ao negócio. Em clustering, isso importa ainda mais: **as features definem o que significa "parecido"**. Se queremos agrupar vizinhanças por estilo de vida, acessibilidade e localização, precisamos de colunas que meçam exatamente isso.

Todas as novas features são calculadas em **unidades naturais** (dólares, quilômetros, pessoas), sobre `df_clean`. Só depois recebem o tratamento de outliers e o scaling.

| Nova feature | Como é calculada | Pergunta de negócio que responde |
|---|---|---|
| `dist_coast_km` | distância exata até o litoral (mapa do Natural Earth) | Quanto vale a proximidade do oceano? |
| `coastal_class` | faixas de `dist_coast_km` | Classificação litoral / costeira / interior para comunicação e relatórios |
| `dist_big_city_km` | distância até a cidade mais próxima com 400 mil+ habitantes | Qual o acesso aos grandes polos de emprego? |
| `pop_density_3km` | pessoas num raio de 3 km ÷ área do círculo | O entorno é urbano, suburbano ou rural? |
| `income_per_person` | `MedInc × 10.000 ÷ AveOccup` | Renda per capita: poder de compra real de cada morador |
| `price_to_income` | `valor da casa ÷ renda anual` | Quantos anos de renda custa uma casa? (acessibilidade) |
| `rooms_per_person` | `AveRooms ÷ AveOccup` | Espaço por pessoa: conforto ou superlotação |
| `bedroom_share` | `AveBedrms ÷ AveRooms` | Tipo de imóvel: apartamentos compactos vs. casas com salas |
| `households` | `Population ÷ AveOccup` | Tamanho do mercado: quantos domicílios (clientes potenciais) |
| `income_vs_neighbors` | `log(renda ÷ renda média dos 10 vizinhos)` | O bairro é mais rico ou mais pobre que o entorno? |
| `luxury_index` | média dos percentis de renda, valor e cômodos (0 a 100) | Indicador de padrão socioeconômico / luxo |

## 4.1 Features geográficas

### Distância até a costa

Na Califórnia, estar perto do oceano significa clima ameno, praias, vista e acesso aos empregos das metrópoles litorâneas. Mas **a costa não está nos dados**: só temos latitude e longitude. Trazemos o litoral do **Natural Earth** (mapa gratuito, escala 1:10 milhões, precisão de cerca de 1 km) e medimos a distância exata de cada block group até a linha da costa, numa projeção plana em metros (`EPSG:3310`, California Albers).
''')

code(r'''
# Tabela de trabalho das features, com condado e região de cada block group
df_feat = df_clean.copy()
df_feat[["county", "region"]] = geo.loc[df_feat.index, ["county", "region"]]

# Linha da costa do Natural Earth, recortada para a Califórnia e projetada em metros
coast_path = download(
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_coastline.geojson",
    "ne_10m_coastline.geojson")
coast = gpd.clip(gpd.read_file(coast_path), box(-125.0, 32.0, -114.0, 42.5))
coast_m = coast.to_crs("EPSG:3310")


def distance_to_coast_km(lat, lon, index):
    """Distância exata (km) de cada ponto até o litoral, numa projeção plana em metros."""
    pts = gpd.GeoDataFrame(index=index, crs="EPSG:4326", geometry=gpd.points_from_xy(lon, lat)).to_crs("EPSG:3310")
    near = gpd.sjoin_nearest(pts, coast_m[["geometry"]], how="left", distance_col="distance_m")
    return near.loc[~near.index.duplicated(), "distance_m"] / 1000


df_feat["dist_coast_km"] = distance_to_coast_km(df_feat["Latitude"], df_feat["Longitude"], df_feat.index)
df_feat["dist_coast_km"].describe()
''')

md(r'''
**Validação com um rótulo independente.** A versão do Kaggle deste dataset tem uma coluna `ocean_proximity`, feita à mão (`NEAR OCEAN`, `NEAR BAY`, `<1H OCEAN`, `INLAND`, `ISLAND`). Se a nossa feature estiver correta, as linhas `NEAR OCEAN` devem estar perto da costa e as `INLAND`, longe. Como os arquivos não têm ID, o join usa várias colunas que, juntas, identificam um block group.
''')

code(r'''
# Rótulo ocean_proximity da versão do Kaggle, unido por colunas que identificam o block group
kaggle = pd.read_csv(download(
    "https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv",
    "housing_kaggle.csv"))
join_keys = pd.DataFrame({
    "longitude": df_raw["Longitude"], "latitude": df_raw["Latitude"],
    "housing_median_age": df_raw["HouseAge"], "population": df_raw["Population"],
    "median_income": df_raw["MedInc"], "median_house_value": (df_raw["MedHouseVal"] * 100_000).round(),
}).loc[df_feat.index]
ocean_label = (join_keys.reset_index()
               .merge(kaggle[list(join_keys.columns) + ["ocean_proximity"]],
                      on=list(join_keys.columns), how="left", validate="one_to_one")
               .set_index("index")["ocean_proximity"])
print(f"Linhas com rótulo encontrado: {ocean_label.notna().sum():,} de {len(ocean_label):,}")

# Distância calculada (km) para cada rótulo independente
LABEL_ORDER = ["ISLAND", "NEAR OCEAN", "NEAR BAY", "<1H OCEAN", "INLAND"]
df_feat["dist_coast_km"].groupby(ocean_label).describe()[["count", "25%", "50%", "75%"]].reindex(LABEL_ORDER).round(1)
''')

md(r'''
[[INTERP-COAST-VALIDATION]]

### Classificação litoral / interior

Para comunicação com as equipes comerciais, transformamos a distância em **quatro faixas**. Os limites seguem a validação acima: a mediana de `NEAR OCEAN` fica perto de 3 km, a de `<1H OCEAN` perto de 18 km e a de `INLAND` perto de 80 km.
''')

code(r'''
# Classificação em quatro faixas de distância até a costa
COASTAL_CLASSES = ["Litoral (até 5 km)", "Costeira (5–25 km)", "Intermediária (25–80 km)", "Interior (> 80 km)"]
df_feat["coastal_class"] = pd.cut(df_feat["dist_coast_km"], bins=[-0.01, 5, 25, 80, np.inf], labels=COASTAL_CLASSES)

# Valor e renda medianos por faixa costeira
price_by_class = (df_feat.groupby("coastal_class", observed=True)
                  .agg(block_groups=("MedHouseVal", "size"),
                       valor_mediano_usd_mil=("MedHouseVal", lambda s: 100 * s.median()),
                       renda_mediana_usd_mil=("MedInc", lambda s: 10 * s.median())))
display(exec_table(price_by_class.reset_index(),
                   formats={"block_groups": "int", "valor_mediano_usd_mil": "int", "renda_mediana_usd_mil": "int"},
                   labels={"coastal_class": "Faixa costeira", "block_groups": "Block groups",
                           "valor_mediano_usd_mil": "Valor mediano (US$ mil)",
                           "renda_mediana_usd_mil": "Renda mediana (US$ mil)"},
                   highlight="valor_mediano_usd_mil"))

# Valor mediano das casas por faixa fina de distância até a costa
distance_bins = [0, 1, 2, 5, 10, 20, 50, 100, 200, 400]
value_by_distance = df_feat.groupby(pd.cut(df_feat["dist_coast_km"], distance_bins), observed=True)["MedHouseVal"].median()
fig, ax = plt.subplots(figsize=(9, 3.6))
ax.bar(range(len(value_by_distance)), value_by_distance * 100, color=BLUE, width=0.7)
ax.set_xticks(range(len(value_by_distance)), [f"{b.left:g}–{b.right:g}" for b in value_by_distance.index])
for i, v in enumerate(value_by_distance * 100):
    ax.text(i, v, f"{v:.0f}", ha="center", va="bottom", fontsize=8, color=INK_2)
ax.set_title("Valor mediano das casas por distância até a costa")
ax.set_xlabel("distância até a costa (km)")
ax.set_ylabel("valor mediano (US$ mil)")
coast_premium = price_by_class["valor_mediano_usd_mil"].iloc[0] / price_by_class["valor_mediano_usd_mil"].iloc[-1]
action_title(fig, f"A casa mediana vale {br(coast_premium, 1)}× mais no litoral (até 5 km) "
                  "do que no interior (mais de 80 km)")
finish(fig, SOURCE_NOTE + " · Litoral: Natural Earth")
print(f"Correlação com MedHouseVal: {np.corrcoef(np.log1p(df_feat['dist_coast_km']), df_feat['MedHouseVal'])[0, 1]:.2f} "
      "(usando log(1 + km))")
''')

md(r'''
[[INTERP-COAST-PRICE]]

### Distância de centros urbanos, densidade e contexto de renda

- **`dist_big_city_km`:** distância até a cidade mais próxima com 400 mil+ habitantes (tabela de cidades dos EUA com coordenadas). Usamos a fórmula **haversine** (distância sobre a esfera) com uma `BallTree`.
- **`pop_density_3km`:** pessoas que moram num raio de 3 km, divididas pela área do círculo. Não temos a área de cada block group, mas conseguimos medir a densidade do **entorno**.
- **`income_vs_neighbors`:** renda do block group comparada com a média dos 10 vizinhos mais próximos (em log: > 0 = mais rico que o entorno).
- **`nearest_city`:** a cidade mais próxima (entre as 212 maiores da Califórnia), usada para **descrever** os segmentos e localizar equipes de venda.
''')

code(r'''
# Cidades da Califórnia com população e coordenadas
ca_cities = (pd.read_csv(download("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv",
                                  "us_cities_top1k.csv"))
             .query("State == 'California'").reset_index(drop=True))
lat_lon_rad = np.radians(df_feat[["Latitude", "Longitude"]].to_numpy())

# Cidade de referência = a cidade mais próxima (distância haversine sobre a esfera)
city_tree = BallTree(np.radians(ca_cities[["lat", "lon"]]), metric="haversine")
df_feat["nearest_city"] = ca_cities.loc[city_tree.query(lat_lon_rad, k=1)[1][:, 0], "City"].to_numpy()

# Distância até a cidade grande (400 mil+ habitantes) mais próxima, em km
big_cities = ca_cities[ca_cities["Population"] >= 400_000]
big_city_tree = BallTree(np.radians(big_cities[["lat", "lon"]]), metric="haversine")
df_feat["dist_big_city_km"] = big_city_tree.query(lat_lon_rad, k=1)[0][:, 0] * EARTH_RADIUS_KM

# Árvore com todos os block groups para buscar vizinhos por raio
RADIUS_KM = 3
neighbour_tree = BallTree(lat_lon_rad, metric="haversine")
population = df_feat["Population"].to_numpy()


def density_3km(lat_lon_radians):
    """Pessoas por km² num raio de 3 km, usando a população de todos os block groups conhecidos."""
    nearby = neighbour_tree.query_radius(lat_lon_radians, r=RADIUS_KM / EARTH_RADIUS_KM)
    return np.array([population[idx].sum() for idx in nearby]) / (np.pi * RADIUS_KM ** 2)


# Densidade do entorno de cada block group
df_feat["pop_density_3km"] = density_3km(lat_lon_rad)

# Renda do block group comparada com a média dos 10 vizinhos mais próximos (log da razão)
nearest_idx = neighbour_tree.query(lat_lon_rad, k=11)[1][:, 1:]     # o primeiro vizinho é o próprio ponto
income = df_feat["MedInc"].to_numpy()
df_feat["income_vs_neighbors"] = np.log(income / income[nearest_idx].mean(axis=1))

print("Cidades grandes:", ", ".join(big_cities["City"]))
''')

md(r'''
## 4.2 Features socioeconômicas e de tipo de imóvel
''')

code(r'''
# Features socioeconômicas e de tipo de imóvel (fórmulas na tabela do início da seção 4)
df_feat["income_per_person"] = df_feat["MedInc"] * 10_000 / df_feat["AveOccup"]
df_feat["price_to_income"] = (df_feat["MedHouseVal"] * 100_000) / (df_feat["MedInc"] * 10_000)
df_feat["rooms_per_person"] = df_feat["AveRooms"] / df_feat["AveOccup"]
df_feat["bedroom_share"] = df_feat["AveBedrms"] / df_feat["AveRooms"]
df_feat["households"] = df_feat["Population"] / df_feat["AveOccup"]
df_feat["luxury_index"] = 100 * df_feat[["MedInc", "MedHouseVal", "AveRooms"]].rank(pct=True).mean(axis=1)

# Resumo estatístico das 10 novas features numéricas
NEW_FEATURES = ["dist_coast_km", "dist_big_city_km", "pop_density_3km", "income_vs_neighbors",
                "income_per_person", "price_to_income", "rooms_per_person", "bedroom_share",
                "households", "luxury_index"]
df_feat[NEW_FEATURES].describe().T
''')

code(r'''
# Mapa da densidade (escala log) e mapa do índice de luxo
fig, axes = plt.subplots(1, 2, figsize=(13, 6.5))
points = axes[0].scatter(df_feat["Longitude"], df_feat["Latitude"], c=df_feat["pop_density_3km"].clip(lower=10),
                         cmap=BLUES, norm=LogNorm(vmin=10, vmax=10_000), s=2)
fig.colorbar(points, ax=axes[0], shrink=0.6, label="pessoas por km² (escala log)")
style_map(axes[0], "Densidade populacional num raio de 3 km")

order = df_feat["luxury_index"].sort_values().index
points = axes[1].scatter(df_feat.loc[order, "Longitude"], df_feat.loc[order, "Latitude"],
                         c=df_feat.loc[order, "luxury_index"], cmap=BLUES, s=2)
fig.colorbar(points, ax=axes[1], shrink=0.6, label="índice de luxo (0 a 100)")
style_map(axes[1], "Índice de luxo / padrão socioeconômico")
action_title(fig, "Densidade e padrão socioeconômico desenham as metrópoles e a faixa litorânea")
finish(fig)
''')

md(r'''
[[INTERP-NEW-FEATURES]]
''')

md(r'''
## 4.3 Tratamento das novas features

As novas features também têm caudas longas e extremos (por exemplo, `rooms_per_person` nas casas de veraneio). Aplicamos a mesma lógica da seção 3.2: winsorização nos percentis 0,5% / 99,5% e a transformação que deixa cada coluna mais simétrica (log, `log(1 + x)` para distâncias que podem ser zero, ou raiz quadrada para a densidade, em que o log corrige demais).
''')

code(r'''
# Winsorização e transformação escolhidas para cada nova feature
NEW_TREATMENT = {
    "dist_coast_km":       {"clip_pct": None, "transform": "log1p"},
    "dist_big_city_km":    {"clip_pct": None, "transform": "log1p"},
    "pop_density_3km":     {"clip_pct": 0.5, "transform": "sqrt"},
    "income_vs_neighbors": {"clip_pct": 0.5, "transform": None},
    "income_per_person":   {"clip_pct": 0.5, "transform": "log"},
    "price_to_income":     {"clip_pct": 0.5, "transform": "log"},
    "rooms_per_person":    {"clip_pct": 0.5, "transform": "log"},
    "bedroom_share":       {"clip_pct": 0.5, "transform": "log"},
    "households":          {"clip_pct": 0.5, "transform": "log"},
    "luxury_index":        {"clip_pct": None, "transform": None},
}
NEW_CLIP_LIMITS = {col: tuple(df_feat[col].quantile([rule["clip_pct"] / 100, 1 - rule["clip_pct"] / 100]))
                   for col, rule in NEW_TREATMENT.items() if rule["clip_pct"] is not None}
TRANSFORMS = {"log": np.log, "log1p": np.log1p, "sqrt": np.sqrt}


def treat_new_features(df):
    """Aplica a winsorização e a transformação escolhidas às novas features presentes em df."""
    out = df.copy()
    for col in out.columns.intersection(list(NEW_TREATMENT)):
        if col in NEW_CLIP_LIMITS:
            out[col] = out[col].clip(*NEW_CLIP_LIMITS[col])
        if NEW_TREATMENT[col]["transform"]:
            out[col] = TRANSFORMS[NEW_TREATMENT[col]["transform"]](out[col])
    return out


# Assimetria e extremos das novas features antes e depois do tratamento
treated_new = treat_new_features(df_feat[NEW_FEATURES])
pd.DataFrame({
    "transformação": [NEW_TREATMENT[c]["transform"] or "-" for c in NEW_FEATURES],
    "skew_antes": df_feat[NEW_FEATURES].skew(),
    "skew_depois": treated_new.skew(),
    "max_z_antes": [max_abs_z(df_feat[c]) for c in NEW_FEATURES],
    "max_z_depois": [max_abs_z(treated_new[c]) for c in NEW_FEATURES],
}).round(2)
''')

md(r'''
[[INTERP-NEW-TREATMENT]]
''')

md(r'''
## 4.4 Análise de correlação e seleção de features para a clusterização

Usar todas as colunas seria um erro:

- **Contagem dupla:** se três colunas dizem a mesma coisa, essa ideia ganha três vezes o peso nas distâncias, sem ninguém ter decidido isso.
- **Maldição da dimensionalidade:** com muitas colunas, todas as vizinhanças parecem igualmente distantes e os clusters ficam difusos.
- **Interpretação:** um segmento descrito por 7 variáveis claras é fácil de explicar a um gestor; com 20, não é.

Seguimos três filtros:

1. **Objetivo de negócio:** queremos *tipos* de vizinhança, não regiões do mapa. Por isso **latitude, longitude, condado e região ficam fora** do clustering e são usados depois, para descrever e mapear os segmentos. O *significado* da localização entra pelas features `dist_coast_km`, `pop_density_3km` e `dist_big_city_km`.
2. **Redundância entre pares:** correlação de Spearman (pega também relações curvas) e um dendrograma de colunas. Colunas com |correlação| ≥ 0,8 dizem a mesma coisa.
3. **Redundância em combinação:** o **VIF** (Variance Inflation Factor) mede o quanto cada coluna pode ser reconstruída pelas outras juntas. VIF acima de 10 indica uma coluna quase redundante.
''')

code(r'''
# Candidatas à clusterização: originais (sem coordenadas) + novas, tratadas e padronizadas
ORIGINAL_CANDIDATES = ["MedInc", "HouseAge", "AveRooms", "AveBedrms", "Population", "AveOccup", "MedHouseVal"]
CANDIDATES = ORIGINAL_CANDIDATES + NEW_FEATURES
X_candidates = pd.concat([treat_outliers(df_feat[df_clean.columns])[ORIGINAL_CANDIDATES],
                          treat_new_features(df_feat[NEW_FEATURES])], axis=1)
Z_candidates = apply_scaler(StandardScaler(), X_candidates)

# Correlação de Spearman e dendrograma das colunas (distância = 1 - |correlação|)
spearman = Z_candidates.corr(method="spearman")
column_links = linkage(squareform((1 - spearman.abs()).to_numpy(), checks=False), method="average")

fig, axes = plt.subplots(1, 2, figsize=(15, 6.5), gridspec_kw={"width_ratios": [1, 1.3]})
tree = dendrogram(column_links, labels=CANDIDATES, orientation="left", ax=axes[0], leaf_font_size=9,
                  color_threshold=0, above_threshold_color=GRAY)
axes[0].axvline(0.2, color=ORANGE, linewidth=1.5)
axes[0].text(0.21, 1, "corte: |corr| = 0,8", color=INK_2, fontsize=8)
axes[0].set_title("Colunas agrupadas por correlação")
axes[0].set_xlabel("1 − |correlação de Spearman|")
axes[0].grid(False)
order = tree["ivl"][::-1]
sns.heatmap(spearman.loc[order, order], cmap=DIVERGING, vmin=-1, vmax=1, ax=axes[1], annot=True, fmt=".1f",
            annot_kws={"fontsize": 6.5}, linewidths=0.5, linecolor=SURFACE,
            cbar_kws={"shrink": 0.7, "label": "correlação de Spearman"})
axes[1].set_title("Matriz de correlação das candidatas (mesma ordem)")
n_redundant = int((pd.Series(fcluster(column_links, t=0.2, criterion="distance")).value_counts() > 1).sum())
action_title(fig, f"{n_redundant} grupos de variáveis dizem praticamente a mesma coisa (|correlação| ≥ 0,8)")
finish(fig)

# Grupos de colunas redundantes: |correlação| >= 0,8 (corte em 0,2 no dendrograma)
groups = pd.Series(fcluster(column_links, t=0.2, criterion="distance"), index=CANDIDATES)
for _, members in groups.groupby(groups):
    if len(members) > 1:
        names = list(members.index)
        values = spearman.loc[names, names].abs().to_numpy()[np.triu_indices(len(names), 1)]
        print(f"{names}  ->  |corr| entre {values.min():.2f} e {values.max():.2f}")
''')

md(r'''
[[INTERP-SPEARMAN]]
''')

code(r'''
def vif(Z):
    """VIF de cada coluna: 1 / (1 - R²) da regressão dessa coluna sobre todas as outras."""
    result = {}
    for col in Z.columns:
        others = Z.drop(columns=col)
        r2 = LinearRegression().fit(others, Z[col]).score(others, Z[col])
        result[col] = 1 / (1 - r2)
    return pd.Series(result, name="VIF").sort_values(ascending=False)


# VIF das candidatas que sobraram depois de remover as redundâncias entre pares
after_pairs = [c for c in CANDIDATES if c not in [[PAIR_DROPS]]]
vif(Z_candidates[after_pairs]).round(1)
''')

md(r'''
[[INTERP-VIF]]
''')

code(r'''
# Decisão final (manter/remover) e o motivo de negócio para cada candidata
DECISIONS = [[DECISIONS]]

FINAL_FEATURES = [c for c in CANDIDATES if DECISIONS[c][0] == "manter"]
selection = pd.DataFrame(DECISIONS, index=["decisão", "motivo"]).T.reindex(CANDIDATES)
print(f"VIF máximo das features finais: {vif(Z_candidates[FINAL_FEATURES]).max():.1f}")
print(f"Features finais ({len(FINAL_FEATURES)}): {FINAL_FEATURES}")
selection.sort_values("decisão", ascending=False)
''')

md(r'''
[[INTERP-SELECTION]]
''')

code(r'''
# Matriz final: as 7 features tratadas e padronizadas (média 0, desvio padrão 1)
X_final = X_candidates[FINAL_FEATURES]
final_scaler = StandardScaler().fit(X_final)
Z = pd.DataFrame(final_scaler.transform(X_final), columns=FINAL_FEATURES, index=X_final.index)
print(f"Matriz para a clusterização: {Z.shape[0]:,} block groups x {Z.shape[1]} features padronizadas")
Z.describe().T[["mean", "std", "min", "max"]].round(2)
''')

# ---------------------------------------------------------------- 5. PCA
md(r'''
---
# 5. Redução de Dimensionalidade (PCA)

O **PCA** (Análise de Componentes Principais) constrói novos eixos, os componentes, que resumem as colunas. O primeiro componente captura a maior parte da variação, o segundo a maior parte do que sobrou, e assim por diante. Os **loadings** mostram quais colunas constroem cada componente, ou seja, o que cada "dimensão do mercado" significa.

Usamos o PCA para duas coisas: (1) entender quantas dimensões reais o mercado tem; (2) **visualizar** os clusters em 2D e 3D (seção 7).
''')

code(r'''
# PCA com todos os componentes: variância explicada e loadings (peso de cada feature)
pca = PCA(random_state=RANDOM_STATE).fit(Z)
explained = pd.DataFrame({"variancia_explicada_pct": 100 * pca.explained_variance_ratio_,
                          "acumulada_pct": 100 * np.cumsum(pca.explained_variance_ratio_)},
                         index=[f"PC{i + 1}" for i in range(Z.shape[1])])
loadings = pd.DataFrame(pca.components_.T, index=FINAL_FEATURES, columns=explained.index)

# Variância explicada (barras e acumulada) e mapa de calor dos loadings dos 4 primeiros componentes
fig, axes = plt.subplots(1, 2, figsize=(14, 4.8), gridspec_kw={"width_ratios": [1, 1.2]})
axes[0].bar(explained.index, explained["variancia_explicada_pct"], color=BLUE, width=0.6)
axes[0].plot(explained.index, explained["acumulada_pct"], marker="o", color=ORANGE, linewidth=2)
for i, v in enumerate(explained["acumulada_pct"]):
    axes[0].text(i, v + 2, f"{v:.0f}%", ha="center", fontsize=8, color=INK_2)
axes[0].set_title("Variação explicada por componente (barras) e acumulada (linha)")
axes[0].set_ylabel("% da variação total")
axes[0].set_ylim(0, 110)
sns.heatmap(loadings.iloc[:, :4], cmap=DIVERGING, vmin=-0.8, vmax=0.8, annot=True, fmt=".2f", ax=axes[1],
            annot_kws={"fontsize": 8}, linewidths=0.5, linecolor=SURFACE,
            cbar_kws={"shrink": 0.7, "label": "loading"})
axes[1].set_title("O que constrói cada componente (loadings)")
n_for_85 = int((explained["acumulada_pct"] < 85).sum() + 1)
action_title(fig, f"São precisos {n_for_85} componentes para explicar "
                  f"{br(explained['acumulada_pct'].iloc[n_for_85 - 1])}% da variação: o mercado tem várias dimensões")
finish(fig)
explained.round(1).T
''')

md(r'''
[[INTERP-PCA]]
''')

code(r'''
# Coordenadas de cada block group nos 3 primeiros componentes; densidade de pontos no plano PC1 x PC2
pcs = pd.DataFrame(pca.transform(Z)[:, :3], columns=["PC1", "PC2", "PC3"], index=Z.index)
fig, ax = plt.subplots(figsize=(8, 6))
hb = ax.hexbin(pcs["PC1"], pcs["PC2"], gridsize=70, cmap=BLUES, bins="log", mincnt=1)
fig.colorbar(hb, ax=ax, shrink=0.8, label="block groups (escala log)")
ax.set_title("Densidade dos block groups no plano PC1 × PC2 (antes da clusterização)")
ax.set_xlabel(f"PC1 ({explained.iloc[0, 0]:.0f}% da variação)")
ax.set_ylabel(f"PC2 ({explained.iloc[1, 0]:.0f}% da variação)")
action_title(fig, "Uma única nuvem contínua: não há grupos isolados")
finish(fig)
''')

md(r'''
[[INTERP-PCA-DENSITY]]
''')

# ---------------------------------------------------------------- 6. Clusterização
md(r'''
---
# 6. Implementação dos Algoritmos de Clusterização

## 6.1 Quais algoritmos e por quê

Testamos quatro famílias de algoritmos. Cada uma faz uma suposição diferente sobre o que é um "grupo", e cada uma entrega algo diferente para o negócio:

| Algoritmo | O que é um grupo para ele | O que entrega ao negócio | Risco neste problema |
|---|---|---|---|
| **K-Means** | pontos próximos de um centro (grupos compactos) | um **perfil médio** (centróide) por segmento, fácil de virar persona; todo block group recebe um segmento; classifica novos block groups instantaneamente | supõe grupos de tamanho e formato parecidos |
| **Gaussian Mixture (GMM)** | nuvens elípticas com probabilidades | **probabilidade** de pertencer a cada segmento: identifica bairros "em transição" | mais parâmetros; pode ficar instável |
| **Hierárquico (Ward)** | grupos que se unem passo a passo | uma **árvore** de segmentos: macro-segmentos e subsegmentos | custo alto (usamos amostra) |
| **DBSCAN** | regiões densas separadas por regiões vazias | encontra grupos de formato livre e marca **ruído** (atípicos) | se o mercado for contínuo, vira um grande grupo + ruído |

Começamos pelo K-Means (o candidato natural para segmentação de mercado), escolhendo o número de clusters com o **método do cotovelo**, a **silhouette** e outros critérios. Depois testamos os demais e comparamos todos na seção 6.6.

## 6.2 K-Means: escolhendo o número de clusters (k)

Para cada k de 2 a 12 calculamos:

- **Inércia** (soma das distâncias ao quadrado até o centro): cai sempre com k; procuramos o **cotovelo**, onde ganhar mais um cluster passa a valer pouco;
- **Silhouette** (−1 a 1, maior é melhor): compara a distância até o próprio cluster com a distância até o cluster vizinho;
- **Davies-Bouldin** (menor é melhor): razão entre dispersão interna e separação entre clusters;
- **Calinski-Harabasz** (maior é melhor): razão entre a variação *entre* clusters e *dentro* deles;
- **Estabilidade por bootstrap** (técnica avançada de validação): reamostramos os dados com reposição 15 vezes, refazemos o K-Means e medimos com o **ARI** (Adjusted Rand Index, 1 = mesma segmentação) se os segmentos se repetem. Uma segmentação que muda a cada amostra não serve para orientar uma estratégia.
''')

code(r'''
K_RANGE = range(2, 13)
kmeans_models, rows = {}, []
for k in K_RANGE:
    model = KMeans(n_clusters=k, n_init=10, random_state=RANDOM_STATE).fit(Z)
    kmeans_models[k] = model
    rows.append({"k": k, "inercia": model.inertia_,
                 "silhouette": silhouette_score(Z, model.labels_, sample_size=10_000, random_state=RANDOM_STATE),
                 "davies_bouldin": davies_bouldin_score(Z, model.labels_),
                 "calinski_harabasz": calinski_harabasz_score(Z, model.labels_),
                 "menor_cluster_pct": 100 * np.bincount(model.labels_).min() / len(Z)})
k_scores = pd.DataFrame(rows).set_index("k")

rng = np.random.default_rng(RANDOM_STATE)
N_BOOT = 15
for k in K_RANGE:
    aris = []
    for b in range(N_BOOT):
        idx = rng.choice(len(Z), size=len(Z), replace=True)
        boot = KMeans(n_clusters=k, n_init=3, random_state=b).fit(Z.iloc[idx])
        aris.append(adjusted_rand_score(kmeans_models[k].labels_, boot.predict(Z)))
    k_scores.loc[k, "estabilidade_ARI"] = np.mean(aris)
    k_scores.loc[k, "estabilidade_ARI_min"] = np.min(aris)


def elbow_point(x, y):
    """Cotovelo: o ponto da curva mais distante da reta que liga o primeiro ao último ponto."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    xn, yn = (x - x.min()) / np.ptp(x), (y - y.min()) / np.ptp(y)
    distance = np.abs((yn[-1] - yn[0]) * xn - (xn[-1] - xn[0]) * yn + xn[-1] * yn[0] - yn[-1] * xn[0])
    return int(np.argmax(distance))


elbow_k = list(K_RANGE)[elbow_point(list(K_RANGE), k_scores["inercia"])]
print(f"Cotovelo da inércia: k = {elbow_k}")
exec_table(k_scores.reset_index(),
           formats={"k": "int", "inercia": "int", "silhouette": "dec3", "davies_bouldin": "dec3",
                    "calinski_harabasz": "int", "menor_cluster_pct": "pct", "estabilidade_ARI": "dec3",
                    "estabilidade_ARI_min": "dec3"},
           labels={"inercia": "Inércia", "silhouette": "Silhouette", "davies_bouldin": "Davies-Bouldin",
                   "calinski_harabasz": "Calinski-Harabasz", "menor_cluster_pct": "Menor segmento",
                   "estabilidade_ARI": "Estabilidade (ARI médio)", "estabilidade_ARI_min": "ARI mínimo"},
           highlight="estabilidade_ARI")
''')

code(r'''
K_FINAL = [[K_FINAL]]   # número de segmentos escolhido (justificativa logo abaixo)

fig, axes = plt.subplots(2, 2, figsize=(13, 7.5), sharex=True)
panels = [(axes[0, 0], "inercia", "Inércia: método do cotovelo (menor é melhor, procure a dobra)"),
          (axes[0, 1], "silhouette", "Silhouette (maior é melhor)"),
          (axes[1, 0], "davies_bouldin", "Davies-Bouldin (menor é melhor)"),
          (axes[1, 1], "estabilidade_ARI", "Estabilidade por bootstrap: ARI médio (maior é melhor)")]
for ax, col, title in panels:
    ax.plot(k_scores.index, k_scores[col], marker="o", markersize=6, linewidth=2, color=BLUE)
    ax.axvline(K_FINAL, color=ORANGE, linewidth=1.5, linestyle="--")
    ax.set_title(title)
axes[0, 0].annotate("cotovelo", (elbow_k, k_scores.loc[elbow_k, "inercia"]), xytext=(15, 20),
                    textcoords="offset points", fontsize=8, color=INK_2, arrowprops={"arrowstyle": "-", "color": GRAY})
axes[1, 1].fill_between(k_scores.index, k_scores["estabilidade_ARI_min"], k_scores["estabilidade_ARI"],
                        color=BLUE, alpha=0.15, linewidth=0)
for ax in axes[1]:
    ax.set_xlabel("número de clusters (k)")
    ax.set_xticks(list(K_RANGE))
action_title(fig, f"k = {K_FINAL} (linha laranja): o maior número de segmentos que continua estável "
                  f"(ARI de {br(k_scores.loc[K_FINAL, 'estabilidade_ARI'], 2)})")
finish(fig)
''')

md(r'''
[[INTERP-K-CHOICE]]
''')

md(r'''
## 6.3 DBSCAN: grupos por densidade

O DBSCAN tem dois parâmetros:

- `min_samples`: quantos vizinhos um ponto precisa ter para ser "núcleo" de um grupo. Usamos a regra prática **2 × número de dimensões = 14**.
- `eps`: o raio da vizinhança. Escolhemos pelo **k-distance plot**: ordenamos a distância de cada ponto até o seu 14º vizinho; o "joelho" da curva separa os pontos em regiões densas (à esquerda) dos pontos isolados (à direita).
''')

code(r'''
# k-distance: distância de cada ponto até o seu 14º vizinho, ordenada; eps = joelho da curva
MIN_SAMPLES = 2 * Z.shape[1]
kth_distance = np.sort(NearestNeighbors(n_neighbors=MIN_SAMPLES).fit(Z).kneighbors(Z)[0][:, -1])
EPS = float(kth_distance[elbow_point(np.arange(len(kth_distance)), kth_distance)])

# Sensibilidade do DBSCAN: número de grupos e ruído para eps em torno do joelho
dbscan_rows = []
for factor in [0.75, 1.0, 1.25, 1.5]:
    labels = DBSCAN(eps=EPS * factor, min_samples=MIN_SAMPLES).fit_predict(Z)
    sizes = pd.Series(labels[labels >= 0]).value_counts()
    dbscan_rows.append({"eps": EPS * factor, "clusters": labels.max() + 1, "ruido_pct": 100 * (labels == -1).mean(),
                        "maior_cluster_pct": 100 * sizes.max() / len(Z) if len(sizes) else 0})
dbscan_table = pd.DataFrame(dbscan_rows)
at_knee = dbscan_table.iloc[1]

fig, ax = plt.subplots(figsize=(12, 3.8))
ax.plot(kth_distance, color=BLUE, linewidth=2)
ax.axhline(EPS, color=ORANGE, linewidth=1.5, linestyle="--")
ax.text(len(kth_distance) * 0.02, EPS, f"  joelho: eps = {br(EPS, 2)}", va="bottom", fontsize=8, color=INK_2)
ax.set_title(f"k-distance plot (distância até o {MIN_SAMPLES}º vizinho, ordenada)")
ax.set_xlabel("block groups ordenados")
ax.set_ylabel("distância (unidades padronizadas)")
groups_text = ("um único grupo" if int(at_knee["clusters"]) == 1
               else f"{int(at_knee['clusters'])} grupos, o maior")
action_title(fig, f"No eps do joelho, o DBSCAN forma {groups_text} com {br(at_knee['maior_cluster_pct'], 1)}% "
                  "dos bairros: o mercado não tem ilhas densas")
finish(fig)

exec_table(dbscan_table, formats={"eps": "dec2", "clusters": "int", "ruido_pct": "pct", "maior_cluster_pct": "pct"},
           labels={"eps": "eps", "clusters": "Grupos", "ruido_pct": "Ruído", "maior_cluster_pct": "Maior grupo"})
''')

md(r'''
[[INTERP-DBSCAN]]
''')

code(r'''
# Perfil (mediana) dos pontos de ruído comparado com o dos demais
dbscan_labels = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES).fit_predict(Z)
dbscan_noise = pd.Series(dbscan_labels == -1, index=Z.index)
noise_profile = pd.DataFrame({"mediana_ruido": df_feat.loc[dbscan_noise, FINAL_FEATURES].median(),
                              "mediana_demais": df_feat.loc[~dbscan_noise, FINAL_FEATURES].median()})
noise_profile
''')

md(r'''
[[INTERP-DBSCAN-NOISE]]

## 6.4 Clustering hierárquico (Ward)

O método de **Ward** começa com cada ponto sozinho e une, a cada passo, os dois grupos cuja união aumenta menos a variância interna. O **dendrograma** mostra a ordem das uniões: cortes altos dão poucos macro-grupos; cortes baixos, muitos grupos finos.

O custo de memória cresce com o quadrado do número de linhas, então usamos uma **amostra aleatória de 5.000 block groups** e depois atribuímos cada um dos demais ao centro do grupo hierárquico mais próximo.
''')

code(r'''
# Ward sobre uma amostra de 5.000 (o custo de memória cresce com o quadrado das linhas)
sample_idx = Z.sample(5_000, random_state=RANDOM_STATE).index
ward_links = linkage(Z.loc[sample_idx], method="ward")
ward_cut = (ward_links[-(K_FINAL - 1), 2] + ward_links[-K_FINAL, 2]) / 2   # entre as uniões que dão K e K+1 grupos

fig, ax = plt.subplots(figsize=(12, 4.5))
dendrogram(ward_links, truncate_mode="lastp", p=30, ax=ax, color_threshold=ward_cut,
           above_threshold_color=GRAY, leaf_font_size=7)
ax.axhline(ward_cut, color=ORANGE, linewidth=1.5, linestyle="--")
ax.set_title(f"Dendrograma de Ward (amostra de 5.000; linha laranja = corte em {K_FINAL} grupos)")
ax.set_ylabel("distância de Ward")
ax.set_xlabel("grupos (número de block groups entre parênteses)")
ax.grid(False)
action_title(fig, f"Não há uma divisão natural nítida perto do corte em {K_FINAL} grupos: o mercado é contínuo")
finish(fig)

# Silhouette da amostra para cortes de 3 a 10 grupos
ward_rows = []
for k in range(3, 11):
    sample_labels = fcluster(ward_links, t=k, criterion="maxclust")
    ward_rows.append({"k": k, "silhouette_amostra": silhouette_score(Z.loc[sample_idx], sample_labels)})
pd.DataFrame(ward_rows).set_index("k").round(3).T
''')

code(r'''
# Corta a árvore em K_FINAL grupos e atribui cada block group ao centro de grupo mais próximo
ward_sample_labels = fcluster(ward_links, t=K_FINAL, criterion="maxclust") - 1
ward_centers = Z.loc[sample_idx].groupby(ward_sample_labels).mean()
ward_labels = cdist(Z, ward_centers).argmin(axis=1)
print(f"Ward com {K_FINAL} grupos, atribuído a todos os {len(Z):,} block groups.")
print("Tamanho dos grupos (%):", np.round(100 * np.bincount(ward_labels) / len(Z), 1))
''')

md(r'''
## 6.5 Gaussian Mixture Models (GMM)

O GMM supõe que os dados vêm de uma mistura de nuvens gaussianas (elípticas) e dá, para cada block group, a **probabilidade** de pertencer a cada segmento. Escolhemos o número de componentes pelo **BIC** e pelo **AIC** (critérios que premiam o ajuste e penalizam a complexidade; menor é melhor).
''')

code(r'''
# Ajusta um GMM (covariância completa) para cada número de componentes e guarda BIC e AIC
gmm_rows, gmm_models = [], {}
for k in K_RANGE:
    gmm = GaussianMixture(n_components=k, covariance_type="full", n_init=2, random_state=RANDOM_STATE).fit(Z)
    gmm_models[k] = gmm
    gmm_rows.append({"k": k, "BIC": gmm.bic(Z), "AIC": gmm.aic(Z)})
gmm_scores = pd.DataFrame(gmm_rows).set_index("k")

fig, ax = plt.subplots(figsize=(9, 3.8))
for col, color in [("BIC", BLUE), ("AIC", ORANGE)]:
    ax.plot(gmm_scores.index, gmm_scores[col] / 1000, marker="o", color=color, linewidth=2, label=col)
ax.axvline(K_FINAL, color=GRAY, linestyle="--", linewidth=1)
ax.set_title("GMM: critérios de informação por número de componentes (menor é melhor)")
ax.set_xlabel("número de componentes")
ax.set_ylabel("valor (milhares)")
ax.set_xticks(list(K_RANGE))
ax.legend()
best_bic = gmm_scores["BIC"].idxmin()
action_title(fig, f"O BIC do GMM cai até {max(K_RANGE)} componentes: ele não aponta um número natural de grupos"
             if best_bic == max(K_RANGE) else f"O BIC do GMM é mínimo com {best_bic} componentes")
finish(fig)

print(f"Menor BIC: {gmm_scores['BIC'].idxmin()} componentes | menor AIC: {gmm_scores['AIC'].idxmin()} componentes")
# GMM final: rótulo mais provável e a probabilidade máxima de cada block group
gmm_final = gmm_models[K_FINAL]
gmm_labels = gmm_final.predict(Z)
gmm_max_prob = gmm_final.predict_proba(Z).max(axis=1)
print(f"GMM com {K_FINAL} componentes | block groups com probabilidade máxima < 0,6: {(gmm_max_prob < 0.6).mean():.1%}")
print("Tamanho dos grupos (%):", np.round(100 * np.bincount(gmm_labels, minlength=K_FINAL) / len(Z), 1))
''')

md(r'''
[[INTERP-GMM]]

## 6.6 Comparação dos algoritmos e escolha final

Comparamos todos com o mesmo número de segmentos e as mesmas métricas. A silhouette é calculada sobre a mesma amostra de 10.000 block groups para todos. No DBSCAN, as métricas ignoram os pontos de ruído.
''')

code(r'''
kmeans_raw_labels = kmeans_models[K_FINAL].labels_


def summarize(name, labels, note=""):
    """Métricas de qualidade de uma segmentação; sem pelo menos 2 grupos, as métricas não existem (NaN)."""
    valid = labels >= 0
    sizes = np.bincount(labels[valid]) / len(labels) * 100
    sizes = sizes[sizes > 0]
    has_groups = len(sizes) >= 2
    return {"algoritmo": name, "clusters": len(sizes),
            "silhouette": silhouette_score(Z[valid], labels[valid], sample_size=10_000,
                                           random_state=RANDOM_STATE) if has_groups else np.nan,
            "davies_bouldin": davies_bouldin_score(Z[valid], labels[valid]) if has_groups else np.nan,
            "calinski_harabasz": calinski_harabasz_score(Z[valid], labels[valid]) if has_groups else np.nan,
            "menor_cluster_pct": sizes.min(), "maior_cluster_pct": sizes.max(),
            "ruido_pct": 100 * (~valid).mean(),
            "ARI_vs_KMeans": adjusted_rand_score(kmeans_raw_labels[valid], labels[valid]), "observação": note}


# Tabela comparativa com as mesmas métricas para todos os algoritmos
dbscan_tight_labels = DBSCAN(eps=EPS * 0.75, min_samples=MIN_SAMPLES).fit_predict(Z)
comparison = pd.DataFrame([
    summarize(f"K-Means (k={K_FINAL})", kmeans_raw_labels, "centróides interpretáveis"),
    summarize(f"GMM ({K_FINAL} componentes)", gmm_labels, "probabilidades de pertencimento"),
    summarize(f"Ward ({K_FINAL} grupos)", ward_labels, "amostra de 5.000 + centro mais próximo"),
    summarize(f"DBSCAN (eps={EPS:.2f}, joelho)", dbscan_labels, "um único grupo denso + ruído"),
    summarize(f"DBSCAN (eps={EPS * 0.75:.2f})", dbscan_tight_labels, "eps menor: mais ruído"),
]).set_index("algoritmo")
exec_table(comparison.reset_index(),
           formats={"clusters": "int", "silhouette": "dec3", "davies_bouldin": "dec3", "calinski_harabasz": "int",
                    "menor_cluster_pct": "pct", "maior_cluster_pct": "pct", "ruido_pct": "pct",
                    "ARI_vs_KMeans": "dec2"},
           labels={"algoritmo": "Algoritmo", "clusters": "Grupos", "silhouette": "Silhouette",
                   "davies_bouldin": "Davies-Bouldin", "calinski_harabasz": "Calinski-Harabasz",
                   "menor_cluster_pct": "Menor grupo", "maior_cluster_pct": "Maior grupo", "ruido_pct": "Ruído",
                   "ARI_vs_KMeans": "Concordância com o K-Means (ARI)", "observação": "Observação"},
           highlight="silhouette", caption="Comparação dos algoritmos com as mesmas métricas")
''')

md(r'''
[[INTERP-COMPARISON]]
''')

code(r'''
km_final = kmeans_models[K_FINAL]

# Numeração estável: segmento 1 = menor valor mediano das casas, ..., segmento K = maior
price_order = df_feat["MedHouseVal"].groupby(kmeans_raw_labels).median().sort_values().index
RELABEL = {old: new for new, old in enumerate(price_order, start=1)}
segment = pd.Series(kmeans_raw_labels, index=Z.index).map(RELABEL).rename("segmento")
SEGMENTS = list(range(1, K_FINAL + 1))
SEG_COLOR = dict(zip(SEGMENTS, PALETTE))
segment.value_counts().sort_index().rename("block_groups").to_frame().T
''')

# ---------------------------------------------------------------- 7. Avaliação
md(r'''
---
# 7. Avaliação e Validação dos Clusters

Validamos a segmentação final (K-Means) em quatro frentes: **métricas de qualidade interna**, **separação e coesão**, **estabilidade** e **coerência geográfica**. Por fim, visualizamos os clusters no espaço do PCA.

## 7.1 Métricas de qualidade interna
''')

code(r'''
# Métricas do modelo final, comparadas com uma referência de rótulos sorteados ao acaso
final_metrics = pd.Series({
    "Silhouette (todos os 20.555 block groups)": silhouette_score(Z, segment),
    "Inércia": km_final.inertia_,
    "Davies-Bouldin": davies_bouldin_score(Z, segment),
    "Calinski-Harabasz": calinski_harabasz_score(Z, segment),
}, name="valor")

shuffled = np.random.default_rng(RANDOM_STATE).permutation(segment.to_numpy())
baseline = pd.Series({
    "Silhouette (todos os 20.555 block groups)": silhouette_score(Z, shuffled, sample_size=10_000,
                                                                   random_state=RANDOM_STATE),
    "Inércia": float(((Z - Z.groupby(shuffled).transform("mean")) ** 2).to_numpy().sum()),
    "Davies-Bouldin": davies_bouldin_score(Z, shuffled),
    "Calinski-Harabasz": calinski_harabasz_score(Z, shuffled),
}, name="rótulos aleatórios (referência)")
metrics_table = pd.concat([final_metrics, baseline], axis=1)
exec_table(metrics_table, index=True, formats={"Silhouette (todos os 20.555 block groups)": "dec3",
                                               "Inércia": "int", "Davies-Bouldin": "dec3",
                                               "Calinski-Harabasz": "int"},
           labels={"valor": "Segmentação final", "rótulos aleatórios (referência)": "Rótulos aleatórios (referência)"})
''')

md(r'''
[[INTERP-METRICS]]

## 7.2 Separação e coesão

- **Gráfico de silhouette:** cada barra horizontal é um block group; a largura é a sua silhouette. Barras largas e positivas = bem encaixado no seu segmento; negativas = mais perto de outro segmento.
- **Distância entre centróides vs. dispersão interna:** um segmento é bem separado quando a distância até o centróide vizinho mais próximo é grande em relação à distância média dos seus membros até o próprio centro.
''')

code(r'''
# Silhouette de cada block group (gráfico de faca por segmento)
sil = pd.Series(silhouette_samples(Z, segment), index=Z.index)

fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), gridspec_kw={"width_ratios": [1.2, 1]})
y_low = 0
for s in SEGMENTS:
    values = np.sort(sil[segment == s].to_numpy())
    axes[0].fill_betweenx(np.arange(y_low, y_low + len(values)), 0, values, color=SEG_COLOR[s], linewidth=0)
    axes[0].text(-0.08, y_low + len(values) / 2, f"S{s}", va="center", ha="right", fontsize=9, color=INK_2)
    y_low += len(values) + 150
axes[0].axvline(sil.mean(), color=INK_2, linestyle="--", linewidth=1)
axes[0].set_title("Silhouette de cada block group, por segmento (tracejado = média)")
axes[0].set_xlabel("silhouette")
axes[0].set_yticks([])

# Distância entre os centróides dos segmentos (separação)
centroids = Z.groupby(segment).mean()
centroid_dist = pd.DataFrame(cdist(centroids, centroids), index=[f"S{s}" for s in SEGMENTS],
                             columns=[f"S{s}" for s in SEGMENTS])
sns.heatmap(centroid_dist, cmap=BLUES, annot=True, fmt=".1f", ax=axes[1], linewidths=0.5, linecolor=SURFACE,
            cbar_kws={"shrink": 0.7, "label": "distância (unidades padronizadas)"})
axes[1].set_title("Distância entre os centróides dos segmentos")
closest = centroid_dist.replace(0, np.nan).stack().idxmin()
action_title(fig, f"Silhouette média de {br(sil.mean(), 2)}: segmentos bem definidos num mercado contínuo; "
                  f"{closest[0]} e {closest[1]} são os vizinhos mais próximos")
finish(fig)

# Coesão (distância média ao próprio centróide) e separação (distância ao centróide vizinho) por segmento
cohesion = pd.Series(np.linalg.norm(Z.to_numpy() - centroids.loc[segment].to_numpy(), axis=1), index=Z.index)
separation = pd.DataFrame({
    "block_groups": segment.value_counts().sort_index(),
    "silhouette_media": sil.groupby(segment).mean(),
    "pct_silhouette_negativa": 100 * (sil < 0).groupby(segment).mean(),
    "dispersao_interna": cohesion.groupby(segment).mean(),
    "distancia_ao_vizinho_mais_proximo": centroid_dist.replace(0, np.nan).min(axis=1).to_numpy(),
})
separation["razao_separacao_coesao"] = separation["distancia_ao_vizinho_mais_proximo"] / separation["dispersao_interna"]
exec_table(separation.reset_index().assign(segmento=lambda d: "S" + d["segmento"].astype(str)),
           formats={"block_groups": "int", "silhouette_media": "dec2", "pct_silhouette_negativa": "pct",
                    "dispersao_interna": "dec2", "distancia_ao_vizinho_mais_proximo": "dec2",
                    "razao_separacao_coesao": "dec2"},
           labels={"segmento": "Segmento", "block_groups": "Block groups", "silhouette_media": "Silhouette média",
                   "pct_silhouette_negativa": "Silhouette negativa", "dispersao_interna": "Dispersão interna",
                   "distancia_ao_vizinho_mais_proximo": "Distância ao vizinho",
                   "razao_separacao_coesao": "Separação ÷ coesão"},
           highlight="silhouette_media")
''')

md(r'''
[[INTERP-SEPARATION]]

## 7.3 Estabilidade dos clusters (bootstrap)

Repetimos o K-Means em **30 amostras bootstrap** (sorteio com reposição). Para cada segmento original, medimos o **índice de Jaccard** com o segmento mais parecido da amostra (1 = os mesmos block groups). Pela regra de Hennig (2007), Jaccard médio acima de 0,75 indica um cluster **estável** e abaixo de 0,5 um cluster que "se dissolve".
''')

code(r'''
# Estabilidade: refaz o K-Means em 30 reamostragens e mede ARI global e Jaccard por segmento
N_BOOT_FINAL = 30
seg_array = segment.to_numpy()
jaccard_scores = {s: [] for s in SEGMENTS}
boot_aris = []
rng = np.random.default_rng(RANDOM_STATE)
for b in range(N_BOOT_FINAL):
    idx = np.unique(rng.choice(len(Z), size=len(Z), replace=True))
    boot = KMeans(n_clusters=K_FINAL, n_init=4, random_state=100 + b).fit(Z.iloc[idx])
    boot_aris.append(adjusted_rand_score(seg_array, boot.predict(Z)))
    original = seg_array[idx]
    for s in SEGMENTS:
        in_s = original == s
        best = max((in_s & (boot.labels_ == c)).sum() / (in_s | (boot.labels_ == c)).sum() for c in range(K_FINAL))
        jaccard_scores[s].append(best)

# Classificação de Hennig: Jaccard >= 0,75 estável; >= 0,6 moderado; abaixo, instável
stability = pd.DataFrame({"jaccard_medio": {s: np.mean(v) for s, v in jaccard_scores.items()},
                          "jaccard_minimo": {s: np.min(v) for s, v in jaccard_scores.items()}})
stability["avaliacao"] = np.select([stability["jaccard_medio"] >= 0.75, stability["jaccard_medio"] >= 0.6],
                                   ["estável", "moderadamente estável"], "instável")
print(f"ARI médio entre a segmentação final e as {N_BOOT_FINAL} reamostragens: "
      f"{np.mean(boot_aris):.3f} (mínimo {np.min(boot_aris):.3f})")
exec_table(stability.reset_index(names="segmento").assign(segmento=lambda d: "S" + d["segmento"].astype(str)),
           formats={"jaccard_medio": "dec3", "jaccard_minimo": "dec3"},
           labels={"segmento": "Segmento", "jaccard_medio": "Jaccard médio", "jaccard_minimo": "Jaccard mínimo",
                   "avaliacao": "Avaliação (Hennig)"},
           highlight="jaccard_medio")
''')

md(r'''
[[INTERP-STABILITY]]

### Teste de controle: e se o mercado não tivesse grupos?

Rótulos sorteados ao acaso (seção 7.1) são uma referência fácil de vencer. Uma referência mais exigente é um **mercado simulado sem nenhum grupo**: uma única nuvem gaussiana, com a mesma média e as mesmas correlações das 7 features. Aplicamos a ela exatamente o mesmo K-Means e as mesmas 30 reamostragens. Se os nossos segmentos fossem só cortes arbitrários de um contínuo, os números seriam parecidos.
''')

code(r'''
# Mercado simulado sem grupos: uma única nuvem gaussiana com a média e a covariância das 7 features
gaussian_null = np.random.default_rng(RANDOM_STATE).multivariate_normal(Z.mean().to_numpy(), np.cov(Z.T), size=len(Z))
null_model = KMeans(n_clusters=K_FINAL, n_init=10, random_state=RANDOM_STATE).fit(gaussian_null)

# Mesma estabilidade por bootstrap da célula anterior, aplicada à simulação
rng = np.random.default_rng(RANDOM_STATE)
null_aris = []
for b in range(N_BOOT_FINAL):
    idx = np.unique(rng.choice(len(gaussian_null), size=len(gaussian_null), replace=True))
    boot = KMeans(n_clusters=K_FINAL, n_init=4, random_state=100 + b).fit(gaussian_null[idx])
    null_aris.append(adjusted_rand_score(null_model.labels_, boot.predict(gaussian_null)))


def explained_variance_pct(X, inertia):
    """Parte da variação total explicada pelos grupos: 1 - inércia / soma dos quadrados em torno da média."""
    X = np.asarray(X)
    return 100 * (1 - inertia / ((X - X.mean(axis=0)) ** 2).sum())


null_test = pd.DataFrame({
    "Segmentação real": [final_metrics.iloc[0], explained_variance_pct(Z, km_final.inertia_),
                         np.mean(boot_aris), np.min(boot_aris)],
    "Mercado simulado sem grupos": [silhouette_score(gaussian_null, null_model.labels_),
                                    explained_variance_pct(gaussian_null, null_model.inertia_),
                                    np.mean(null_aris), np.min(null_aris)],
}, index=["Silhouette", "Variação explicada pelos grupos", "Estabilidade (ARI médio)", "Pior reamostragem (ARI)"])
exec_table(null_test, index=True, formats={"Silhouette": "dec3", "Variação explicada pelos grupos": "pct",
                                           "Estabilidade (ARI médio)": "dec2", "Pior reamostragem (ARI)": "dec2"},
           caption=f"O mesmo K-Means (k = {K_FINAL}) nos dados reais e num mercado sem grupos")
''')

md(r'''
**Os segmentos passam no teste:**

- **Estabilidade:** no mercado simulado, o K-Means também "encontra" 6 grupos, mas eles mudam a cada amostra (ARI de 0,71, com reamostragens que caem para 0,45). Nos dados reais, os segmentos se repetem (0,94; pior caso de 0,89).
- **Silhouette e variação explicada:** 0,185 e 52% nos dados reais, contra 0,137 e 46% no mercado sem grupos.

**Conclusão:** o mercado é contínuo (não há vazios entre os segmentos), mas não é uma nuvem sem forma: a sua estrutura mantém as fronteiras dos segmentos no mesmo lugar, amostra após amostra. É isso que torna os segmentos confiáveis para orientar uma estratégia, apesar da silhouette moderada.

## 7.4 Distribuição geográfica dos clusters
''')

code(r'''
# Mapa obrigatório: latitude x longitude colorido pelo segmento
fig, ax = plt.subplots(figsize=(8, 8))
for s in SEGMENTS:
    inside = segment == s
    ax.scatter(df_feat.loc[inside, "Longitude"], df_feat.loc[inside, "Latitude"], s=3, color=SEG_COLOR[s],
               label=f"S{s} ({br(inside.sum())})")
coast.plot(ax=ax, color=GRAY, linewidth=0.5)
style_map(ax, "Segmentos de mercado no mapa da Califórnia (latitude × longitude)")
ax.legend(loc="upper right", markerscale=4, title="segmento (block groups)", title_fontsize=8)
action_title(fig, "Sem usar latitude e longitude, os segmentos desenham o mapa da Califórnia")
finish(fig, SOURCE_NOTE + " · Litoral: Natural Earth")
''')

code(r'''
# Um mapa pequeno por segmento, com os demais em cinza
n_cols = 3
n_rows = int(np.ceil(K_FINAL / n_cols))
fig, axes = plt.subplots(n_rows, n_cols, figsize=(4.2 * n_cols, 4.4 * n_rows))
for ax in axes.flat[K_FINAL:]:
    ax.set_visible(False)
for ax, s in zip(axes.flat, SEGMENTS):
    inside = segment == s
    ax.scatter(df_feat.loc[~inside, "Longitude"], df_feat.loc[~inside, "Latitude"], s=0.5, color="#e1e0d9")
    ax.scatter(df_feat.loc[inside, "Longitude"], df_feat.loc[inside, "Latitude"], s=1.5, color=SEG_COLOR[s])
    style_map(ax, f"S{s} ({br(100 * inside.mean())}% dos block groups)")
action_title(fig, "Cada segmento tem uma geografia própria (em destaque; os demais em cinza)")
finish(fig)

# Participação de cada segmento dentro de cada região
region_mix = pd.crosstab(df_feat["region"], segment, normalize="index") * 100
fig, ax = plt.subplots(figsize=(9, 4.8))
sns.heatmap(region_mix.rename(columns=lambda s: f"S{s}"), cmap=BLUES, annot=True, fmt=".0f", ax=ax,
            linewidths=0.5, linecolor=SURFACE, cbar_kws={"shrink": 0.7, "label": "% dos block groups da região"})
ax.set_title("Composição de cada região por segmento (% da linha)")
ax.set_xlabel("segmento")
ax.set_ylabel("")
action_title(fig, "Toda metrópole mistura vários segmentos: a estratégia deve ser por segmento, e não por cidade")
finish(fig)
''')

md(r'''
[[INTERP-GEO]]

## 7.5 Os clusters no espaço reduzido do PCA

**Como ler os gráficos abaixo:**

- Cada ponto é um block group (amostra de 6.000), colorido pelo segmento. Os rótulos `S1`, `S2`, ... marcam os centróides.
- Os eixos são os componentes principais da seção 5. As **setas** mostram a direção em que cada variável original cresce: um segmento posicionado na direção de uma seta tem valores altos daquela variável.
- Segmentos bem separados aparecem como nuvens em lugares diferentes; a sobreposição nas bordas mostra que o mercado é **contínuo**: há bairros de transição entre segmentos vizinhos.
''')

code(r'''
# Biplot: amostra de pontos e centróides no plano PC1 x PC2, com as setas das variáveis
plot_idx = Z.sample(6_000, random_state=RANDOM_STATE).index
centroid_pcs = pd.DataFrame(pca.transform(centroids)[:, :3], index=SEGMENTS, columns=["PC1", "PC2", "PC3"])

fig, ax = plt.subplots(figsize=(10, 7.5))
for s in SEGMENTS:
    sel = plot_idx[segment.loc[plot_idx] == s]
    ax.scatter(pcs.loc[sel, "PC1"], pcs.loc[sel, "PC2"], s=4, color=SEG_COLOR[s], alpha=0.45, label=f"S{s}")
for s in SEGMENTS:
    ax.scatter(*centroid_pcs.loc[s, ["PC1", "PC2"]], s=160, color=SEG_COLOR[s], edgecolor=SURFACE, linewidth=2, zorder=5)
    ax.annotate(f"S{s}", centroid_pcs.loc[s, ["PC1", "PC2"]], xytext=(7, 7), textcoords="offset points",
                fontsize=10, fontweight="bold", color=INK, zorder=6)
arrow_scale = 3.2
for feature in FINAL_FEATURES:
    dx, dy = loadings.loc[feature, "PC1"] * arrow_scale, loadings.loc[feature, "PC2"] * arrow_scale
    ax.arrow(0, 0, dx, dy, color=INK_2, width=0.012, head_width=0.12, length_includes_head=True, zorder=7)
    ax.text(dx * 1.12, dy * 1.12, feature, fontsize=8, color=INK, ha="center", va="center", zorder=8,
            bbox={"boxstyle": "round,pad=0.2", "facecolor": SURFACE, "edgecolor": "none", "alpha": 0.8})
ax.set_title("Biplot: segmentos no plano PC1 × PC2 e direção das variáveis")
ax.set_xlabel(f"PC1 ({explained.iloc[0, 0]:.0f}% da variação)")
ax.set_ylabel(f"PC2 ({explained.iloc[1, 0]:.0f}% da variação)")
ax.legend(loc="lower left", markerscale=4, ncol=2)
richest = int(centroid_pcs["PC1"].idxmax())
action_title(fig, f"S{richest} lidera o eixo da riqueza (PC1); o eixo vertical separa centros urbanos do interior")
finish(fig)
''')

code(r'''
# Mesma amostra nos três primeiros componentes (3D)
fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(projection="3d")
sub_idx = plot_idx[:4_000]
for s in SEGMENTS:
    sel = sub_idx[segment.loc[sub_idx] == s]
    ax.scatter(pcs.loc[sel, "PC1"], pcs.loc[sel, "PC2"], pcs.loc[sel, "PC3"], s=3, color=SEG_COLOR[s],
               alpha=0.5, label=f"S{s}")
ax.set_xlabel(f"PC1 ({explained.iloc[0, 0]:.0f}%)")
ax.set_ylabel(f"PC2 ({explained.iloc[1, 0]:.0f}%)")
ax.set_zlabel(f"PC3 ({explained.iloc[2, 0]:.0f}%)")
ax.set_title(f"Segmentos nos três primeiros componentes ({explained.iloc[2, 1]:.0f}% da variação)")
ax.view_init(elev=22, azim=-55)
ax.legend(loc="upper left", markerscale=4, ncol=2)
action_title(fig, "A terceira dimensão (tamanho do domicílio) separa segmentos que se sobrepõem no plano")
finish(fig)
''')

md(r'''
[[INTERP-PCA-CLUSTERS]]
''')
