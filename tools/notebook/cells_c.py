CELLS = []


def md(text):
    CELLS.append(("md", text))


def code(text):
    CELLS.append(("code", text))


# ---------------------------------------------------------------- 8. Caracterização
md(r'''
---
# 8. Interpretação e Caracterização dos Clusters

Esta é a etapa que transforma o resultado técnico em conhecimento de negócio. Descrevemos cada segmento em **unidades naturais** (dólares, anos, quilômetros), e não nos valores padronizados usados pelo algoritmo.

## 8.1 Perfil de cada segmento
''')

code(r'''
# Tabela de análise: features em unidades naturais + segmento + flags
seg = df_feat.assign(segmento=segment, no_teto=cap_flags["MedHouseVal_no_teto"],
                     casa_nova=df_feat["HouseAge"] <= 10)
grouped = seg.groupby("segmento")

# Perfil de cada segmento em unidades naturais (medianas, percentuais e tamanhos)
profile = pd.DataFrame({
    "block_groups": grouped.size(),
    "pct_block_groups": 100 * grouped.size() / len(seg),
    "domicilios": grouped["households"].sum().round(),
    "pct_domicilios": 100 * grouped["households"].sum() / seg["households"].sum(),
    "renda_mediana_usd": grouped["MedInc"].median() * 10_000,
    "renda_per_capita_usd": grouped["income_per_person"].median(),
    "valor_mediano_usd": grouped["MedHouseVal"].median() * 100_000,
    "valor_p25_usd": grouped["MedHouseVal"].quantile(0.25) * 100_000,
    "valor_p75_usd": grouped["MedHouseVal"].quantile(0.75) * 100_000,
    "pct_no_teto_500k": 100 * grouped["no_teto"].mean(),
    "anos_de_renda_por_casa": grouped["price_to_income"].median(),
    "idade_casas_anos": grouped["HouseAge"].median(),
    "pct_casas_ate_10_anos": 100 * grouped["casa_nova"].mean(),
    "comodos_por_domicilio": grouped["AveRooms"].median(),
    "pessoas_por_domicilio": grouped["AveOccup"].median(),
    "dist_costa_km": grouped["dist_coast_km"].median(),
    "densidade_hab_km2": grouped["pop_density_3km"].median(),
    "dist_grande_cidade_km": grouped["dist_big_city_km"].median(),
    "indice_luxo": grouped["luxury_index"].median(),
})

# Rótulos legíveis e formato de cada linha da tabela de perfil
PROFILE_ROWS = {
    "block_groups": ("Block groups", "int"), "pct_block_groups": ("% dos block groups", "pct"),
    "domicilios": ("Domicílios", "int"), "pct_domicilios": ("% dos domicílios", "pct"),
    "renda_mediana_usd": ("Renda mediana", "usd_mil"), "renda_per_capita_usd": ("Renda per capita", "usd"),
    "valor_mediano_usd": ("Valor mediano das casas", "usd_mil"), "valor_p25_usd": ("Valor: 1º quartil", "usd_mil"),
    "valor_p75_usd": ("Valor: 3º quartil", "usd_mil"), "pct_no_teto_500k": ("% no teto de US$ 500 mil", "pct"),
    "anos_de_renda_por_casa": ("Anos de renda por casa", "dec1"), "idade_casas_anos": ("Idade das casas (anos)", "int"),
    "pct_casas_ate_10_anos": ("% com casas de até 10 anos", "pct"), "comodos_por_domicilio": ("Cômodos por domicílio", "dec1"),
    "pessoas_por_domicilio": ("Pessoas por domicílio", "dec1"), "dist_costa_km": ("Distância da costa", "km"),
    "densidade_hab_km2": ("Densidade (hab./km²)", "int"), "dist_grande_cidade_km": ("Distância de cidade grande", "km"),
    "indice_luxo": ("Índice de luxo (0 a 100)", "dec1"),
}
exec_table(profile.T.rename(index={k: v[0] for k, v in PROFILE_ROWS.items()}), index=True,
           formats={label: kind for label, kind in PROFILE_ROWS.values()},
           labels={s: f"S{s}" for s in SEGMENTS}, caption="Perfil de cada segmento (medianas)")
''')

code(r'''
def top_shares(column, n=3):
    """As n categorias mais frequentes de cada segmento, com a sua participação."""
    shares = pd.crosstab(segment, df_feat[column], normalize="index") * 100
    return shares.apply(lambda row: ", ".join(f"{name} ({value:.0f}%)" for name, value in row.nlargest(n).items()),
                        axis=1)


def top_cities(n=4):
    """Cidades de referência com mais domicílios em cada segmento."""
    totals = seg.groupby(["segmento", "nearest_city"])["households"].sum()
    return totals.groupby(level=0, group_keys=False).nlargest(n).reset_index().groupby("segmento")["nearest_city"].agg(", ".join)


# Principais regiões, faixas costeiras e cidades de referência de cada segmento
location = pd.DataFrame({"principais_regioes": top_shares("region"),
                         "faixa_costeira": top_shares("coastal_class", n=2),
                         "cidades_de_referencia": top_cities()})
exec_table(location.reset_index().assign(segmento=lambda d: "S" + d["segmento"].astype(str)), formats={},
           labels={"segmento": "Segmento", "principais_regioes": "Principais regiões",
                   "faixa_costeira": "Faixa costeira", "cidades_de_referencia": "Cidades de referência"})
''')

md(r'''
[[INTERP-PROFILE]]
''')

md(r'''
## 8.2 A "impressão digital" de cada segmento

O mapa de calor abaixo mostra, para cada segmento, a média de cada variável em **desvios padrão em relação à média da Califórnia** (0 = típico do estado; azul = abaixo; vermelho = acima). Incluímos também variáveis que não entraram no algoritmo (renda per capita, anos de renda por casa, índice de luxo, distância de grandes cidades), para enriquecer a descrição.
''')

code(r'''
# Média de cada variável por segmento, em desvios padrão em relação ao estado
DESCRIBE_COLS = FINAL_FEATURES + ["income_per_person", "price_to_income", "luxury_index", "dist_big_city_km",
                                  "bedroom_share", "income_vs_neighbors"]
X_describe = pd.concat([X_candidates[FINAL_FEATURES],
                        X_candidates[[c for c in DESCRIBE_COLS if c not in FINAL_FEATURES]]], axis=1)
fingerprint = standardize(X_describe).groupby(segment).mean().T

fig, ax = plt.subplots(figsize=(1.3 * K_FINAL + 4, 6.5))
sns.heatmap(fingerprint.rename(columns=lambda s: f"S{s}"), cmap=DIVERGING, center=0, vmin=-2, vmax=2,
            annot=True, fmt=".1f", annot_kws={"fontsize": 8}, linewidths=0.5, linecolor=SURFACE, ax=ax,
            cbar_kws={"shrink": 0.7, "label": "desvios padrão em relação à média do estado"})
ax.axhline(len(FINAL_FEATURES), color=INK, linewidth=1.5)
ax.set_title("Acima da linha: variáveis usadas no clustering; abaixo: apenas descritivas")
ax.set_xlabel("segmento")
action_title(fig, "A impressão digital de cada segmento, em desvios padrão em relação à média do estado")
finish(fig)
''')

md(r'''
## 8.3 Distribuição das variáveis em cada segmento

Os boxplots mostram não só o valor típico (a linha azul é a mediana), mas também a **variação interna** de cada segmento: caixas estreitas indicam um segmento homogêneo.
''')

code(r'''
# Variável, fator de conversão para unidade natural, rótulo e uso de escala log
BOX_VARS = [("MedInc", 10, "renda mediana (US$ mil/ano)", False),
            ("MedHouseVal", 100, "valor mediano (US$ mil)", False),
            ("price_to_income", 1, "anos de renda por casa", False),
            ("HouseAge", 1, "idade mediana das casas (anos)", False),
            ("AveRooms", 1, "cômodos por domicílio", False),
            ("AveOccup", 1, "pessoas por domicílio", False),
            ("dist_coast_km", 1, "distância até a costa (km, log)", True),
            ("pop_density_3km", 1, "densidade (hab./km², log)", True),
            ("income_per_person", 1 / 1000, "renda per capita (US$ mil)", False)]
# Um boxplot por variável, com os segmentos lado a lado
long = seg.assign(seg_label=seg["segmento"].map(lambda s: f"S{s}"))
fig, axes = plt.subplots(3, 3, figsize=(14, 10.5))
for ax, (col, factor, label, log_scale) in zip(axes.flat, BOX_VARS):
    values = long[col] * factor
    if col in ["AveRooms", "AveOccup", "price_to_income"]:
        values = values.clip(upper=values.quantile(0.99))
    sns.boxplot(x=long["seg_label"], y=values + (0.1 if log_scale else 0), hue=long["seg_label"],
                palette={f"S{s}": SEG_COLOR[s] for s in SEGMENTS}, order=[f"S{s}" for s in SEGMENTS],
                ax=ax, linewidth=0.8, fliersize=1, legend=False, log_scale=log_scale,
                medianprops={"color": INK, "linewidth": 1.5}, flierprops={"alpha": 0.3})
    ax.set_title(label)
    ax.set_xlabel("")
    ax.set_ylabel("")
action_title(fig, "Segmentos com o mesmo preço diferem em renda, idade, tamanho das casas e família "
                  "(linha preta = mediana)")
finish(fig)
''')

code(r'''
# Histograma do valor das casas em cada segmento (em % do segmento)
bins = np.linspace(0, 500, 41)
fig, axes = plt.subplots(1, K_FINAL, figsize=(2.6 * K_FINAL, 3.2), sharex=True, sharey=True)
for ax, s in zip(axes, SEGMENTS):
    values = seg.loc[seg["segmento"] == s, "MedHouseVal"] * 100
    ax.hist(values, bins=bins, color=SEG_COLOR[s], edgecolor=SURFACE, linewidth=0.3,
            weights=np.full(len(values), 100 / len(values)))
    ax.axvline(values.median(), color=INK, linewidth=1.2, linestyle="--")
    ax.set_title(f"S{s}: mediana US$ {br(values.median())} mil", fontsize=9)
    ax.set_xlabel("valor (US$ mil)")
axes[0].set_ylabel("% dos block groups do segmento")
action_title(fig, "Padrão de preços: cada segmento ocupa uma faixa própria, e S6 encosta no teto de US$ 500 mil")
finish(fig)

# Composição de cada segmento por faixa de distância até a costa
coastal_mix = pd.crosstab(segment, df_feat["coastal_class"], normalize="index") * 100
fig, ax = plt.subplots(figsize=(10, 0.55 * K_FINAL + 1.2))
left = np.zeros(K_FINAL)
for coastal, color in zip(COASTAL_CLASSES, ["#0d366b", "#1c5cab", "#3987e5", "#86b6ef"]):
    values = coastal_mix[coastal].to_numpy()
    ax.barh([f"S{s}" for s in SEGMENTS], values, left=left, color=color, edgecolor=SURFACE, linewidth=2,
            label=coastal)
    for i, (start, width) in enumerate(zip(left, values)):
        if width >= 8:
            ax.text(start + width / 2, i, f"{width:.0f}%", ha="center", va="center", fontsize=8,
                    color="white" if coastal != COASTAL_CLASSES[-1] else INK)
    left += values
ax.invert_yaxis()
ax.set_xlim(0, 100)
ax.set_xlabel("% dos block groups do segmento")
ax.set_title("Proximidade do oceano em cada segmento")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=4)
most_coastal = int(coastal_mix[COASTAL_CLASSES[0]].idxmax())
most_inland = int(coastal_mix[COASTAL_CLASSES[-1]].idxmax())
action_title(fig, f"S{most_coastal} é o segmento mais litorâneo; S{most_inland}, o do interior")
finish(fig)
''')

md(r'''
## 8.4 Os segmentos, um a um

Os nomes resumem o perfil de cada segmento. O painel abaixo mostra os seis lado a lado; em seguida, cada um é descrito em detalhe.
''')

code(r'''
# Nomes de negócio dos segmentos, definidos a partir dos perfis acima
SEGMENT_NAMES = [[SEGMENT_NAMES]]
segment_name = segment.map(SEGMENT_NAMES).rename("nome_segmento")
SEG_LABEL = {s: f"S{s} · {SEGMENT_NAMES[s]}" for s in SEGMENTS}
profile.insert(0, "nome", pd.Series(SEGMENT_NAMES))

# Painel executivo: um cartão por segmento, com os indicadores principais e um mini-mapa
fig = plt.figure(figsize=(15, 10))
cards = fig.add_gridspec(2, 3, left=0.01, right=0.99, top=0.9, bottom=0.03, hspace=0.12, wspace=0.05)
for i, s in enumerate(SEGMENTS):
    card = cards[i // 3, i % 3].subgridspec(2, 2, height_ratios=[0.16, 1], width_ratios=[1, 1], hspace=0.05,
                                            wspace=0.02)
    header, kpis, mini = fig.add_subplot(card[0, :]), fig.add_subplot(card[1, 0]), fig.add_subplot(card[1, 1])
    p = profile.loc[s]
    header.set_facecolor(SEG_COLOR[s])
    header.set_xticks([])
    header.set_yticks([])
    for spine in header.spines.values():
        spine.set_visible(False)
    header.text(0.03, 0.5, SEG_LABEL[s], color="white", fontsize=12, fontweight="bold", va="center",
                transform=header.transAxes)
    kpis.set_axis_off()
    indicators = [(f"{br(p['pct_domicilios'])}%", "dos domicílios"),
                  (f"US$ {br(p['valor_mediano_usd'] / 1000)} mil", "casa mediana"),
                  (f"US$ {br(p['renda_mediana_usd'] / 1000)} mil", "renda mediana por ano"),
                  (f"{br(p['dist_costa_km'], 1 if p['dist_costa_km'] < 10 else 0)} km", "da costa"),
                  (f"{br(p['idade_casas_anos'])} anos", "idade das casas")]
    for j, (value, label) in enumerate(indicators):
        y = 0.9 - j * 0.2
        kpis.text(0.06, y, value, fontsize=15, fontweight="bold", color=INK, va="center", transform=kpis.transAxes)
        kpis.text(0.06, y - 0.075, label, fontsize=8.5, color=GRAY, va="center", transform=kpis.transAxes)
    inside = segment == s
    mini.scatter(df_feat.loc[~inside, "Longitude"], df_feat.loc[~inside, "Latitude"], s=0.3, color="#e1e0d9")
    mini.scatter(df_feat.loc[inside, "Longitude"], df_feat.loc[inside, "Latitude"], s=0.8, color=SEG_COLOR[s])
    style_map(mini)
action_title(fig, "Seis tipos de bairro, cada um com perfil e geografia próprios")
finish(fig, tight=False)
''')

md(r'''
[[INTERP-SEGMENT-CARDS]]
''')

# ---------------------------------------------------------------- 8.5 Técnicas avançadas
md(r'''
## 8.5 Técnicas avançadas

### (a) Clusterização hierárquica: diferentes níveis de granularidade

Um gestor de marketing pode querer **poucos** grupos para a comunicação institucional e **mais** grupos para campanhas locais. Aplicamos o clustering hierárquico de Ward sobre os **centróides** dos segmentos, o que mostra quais segmentos são "primos" e como eles se juntam em macro-segmentos.
''')

code(r'''
# Ward sobre os centróides: mostra quais segmentos são parecidos entre si
centroid_links = linkage(centroids.to_numpy(), method="ward")

fig, ax = plt.subplots(figsize=(10, 4.2))
dendrogram(centroid_links, labels=[SEG_LABEL[s] for s in SEGMENTS], orientation="right", ax=ax,
           color_threshold=centroid_links[-2, 2] * 0.999, above_threshold_color=GRAY, leaf_font_size=9)
ax.set_title("Ward sobre os centróides dos segmentos")
ax.set_xlabel("distância de Ward")
ax.grid(False)
action_title(fig, "Os seis segmentos se agrupam em três macro-segmentos")
finish(fig)

# Corte em 3 macro-segmentos
macro = pd.Series(fcluster(centroid_links, t=3, criterion="maxclust"), index=SEGMENTS, name="macro_segmento")
macro_table = (pd.DataFrame({"macro_segmento": macro, "segmento": [SEG_LABEL[s] for s in SEGMENTS],
                             "pct_domicilios": profile["pct_domicilios"].round(1)})
               .sort_values("macro_segmento"))
exec_table(macro_table, formats={"macro_segmento": "int", "pct_domicilios": "pct"},
           labels={"macro_segmento": "Macro-segmento", "segmento": "Segmento", "pct_domicilios": "% dos domicílios"})
''')

md(r'''
[[INTERP-MACRO]]

### (b) Clusterização recursiva: subsegmentos dentro de um segmento

Escolhemos o segmento **mais heterogêneo** entre os grandes (menor silhouette média entre os que têm pelo menos 12% dos block groups) e aplicamos o K-Means **dentro dele**. Isso responde a uma pergunta prática: *vale a pena tratar esse segmento como um bloco único, ou ele esconde mercados diferentes?*
''')

code(r'''
# Segmento mais heterogêneo entre os grandes (>= 12% dos block groups): menor silhouette média
large = separation[separation["block_groups"] >= 0.12 * len(Z)]
target_segment = int(large["silhouette_media"].idxmin())
inside = segment == target_segment
Z_inside = Z[inside]

# Número de subsegmentos escolhido pela silhouette dentro do segmento
sub_rows = []
for k in range(2, 6):
    labels = KMeans(n_clusters=k, n_init=10, random_state=RANDOM_STATE).fit_predict(Z_inside)
    sub_rows.append({"k": k, "silhouette": silhouette_score(Z_inside, labels, sample_size=6_000,
                                                            random_state=RANDOM_STATE)})
sub_scores = pd.DataFrame(sub_rows).set_index("k")
K_SUB = int(sub_scores["silhouette"].idxmax())
print(f"Segmento analisado: {SEG_LABEL[target_segment]} ({br(inside.sum())} block groups)")
print(f"Melhor número de subsegmentos pela silhouette: {K_SUB}")
display(sub_scores.round(3).T)

# Subsegmentos numerados pelo valor mediano das casas
sub_model = KMeans(n_clusters=K_SUB, n_init=10, random_state=RANDOM_STATE).fit(Z_inside)
sub_order = df_feat.loc[inside, "MedHouseVal"].groupby(sub_model.labels_).median().sort_values().index
sub_label = pd.Series(sub_model.labels_, index=Z_inside.index).map(
    {old: f"S{target_segment}.{new}" for new, old in enumerate(sub_order, start=1)})

# Perfil dos subsegmentos em unidades naturais
sub_profile = (seg.loc[inside].groupby(sub_label)
               .agg(block_groups=("MedInc", "size"),
                    renda_mediana_usd=("MedInc", lambda s: 10_000 * s.median()),
                    valor_mediano_usd=("MedHouseVal", lambda s: 100_000 * s.median()),
                    idade_casas_anos=("HouseAge", "median"),
                    comodos=("AveRooms", "median"),
                    pessoas_por_domicilio=("AveOccup", "median"),
                    dist_costa_km=("dist_coast_km", "median"),
                    densidade_hab_km2=("pop_density_3km", "median")))
display(exec_table(sub_profile.reset_index(names="subsegmento"),
                   formats={"block_groups": "int", "renda_mediana_usd": "usd_mil", "valor_mediano_usd": "usd_mil",
                            "idade_casas_anos": "int", "comodos": "dec1", "pessoas_por_domicilio": "dec1",
                            "dist_costa_km": "km", "densidade_hab_km2": "int"},
                   labels={"subsegmento": "Subsegmento", "block_groups": "Block groups",
                           "renda_mediana_usd": "Renda mediana", "valor_mediano_usd": "Valor mediano",
                           "idade_casas_anos": "Idade das casas", "comodos": "Cômodos",
                           "pessoas_por_domicilio": "Pessoas/domicílio", "dist_costa_km": "Distância da costa",
                           "densidade_hab_km2": "Densidade (hab./km²)"}))

fig, ax = plt.subplots(figsize=(7, 7))
ax.scatter(df_feat.loc[~inside, "Longitude"], df_feat.loc[~inside, "Latitude"], s=0.5, color="#e1e0d9")
for i, name in enumerate(sorted(sub_label.unique())):
    sel = sub_label[sub_label == name].index
    ax.scatter(df_feat.loc[sel, "Longitude"], df_feat.loc[sel, "Latitude"], s=2.5, color=PALETTE[i], label=name)
coast.plot(ax=ax, color=GRAY, linewidth=0.5)
style_map(ax, f"Subsegmentos de {SEG_LABEL[target_segment]}")
ax.legend(loc="upper right", markerscale=4)
action_title(fig, f"S{target_segment} esconde {K_SUB} mercados diferentes")
finish(fig, SOURCE_NOTE + " · Litoral: Natural Earth")
''')

md(r'''
[[INTERP-RECURSIVE]]

### (c) Ensemble de clustering: o núcleo estável e as zonas de transição

Combinamos os três algoritmos que segmentam todo o mercado (K-Means, GMM e Ward). Como cada algoritmo numera seus grupos de forma arbitrária, primeiro **alinhamos os rótulos** ao K-Means com o algoritmo húngaro (que encontra a correspondência de máxima sobreposição). Depois, cada block group recebe um **voto de consenso**:

- **Núcleo estável (3 de 3):** os três algoritmos concordam. São os block groups que representam o segmento "puro".
- **Confirmado pela maioria (2 de 3):** um algoritmo discorda, mas a maioria confirma o segmento do K-Means.
- **Contestado (só o K-Means):** os outros dois algoritmos discordam do K-Means. São bairros na fronteira entre dois segmentos, que podem migrar com o tempo.
''')

code(r'''
def align_to_segments(labels):
    """Renomeia os rótulos de outro algoritmo para o segmento do K-Means com maior sobreposição."""
    table = pd.crosstab(pd.Series(labels, index=Z.index), segment)
    rows, cols = linear_sum_assignment(-table.to_numpy())
    mapping = {table.index[r]: table.columns[c] for r, c in zip(rows, cols)}
    return pd.Series(labels, index=Z.index).map(mapping)


# Rótulos dos três algoritmos alinhados à numeração do K-Means
votes = pd.DataFrame({"kmeans": segment, "gmm": align_to_segments(gmm_labels),
                      "ward": align_to_segments(ward_labels)})
support = (votes[["gmm", "ward"]].eq(segment, axis=0)).sum(axis=1) + 1     # algoritmos que concordam com o K-Means
AGREEMENT_LEVELS = {3: "núcleo estável (3 de 3)", 2: "confirmado pela maioria (2 de 3)", 1: "contestado (só o K-Means)"}
agreement_level = support.map(AGREEMENT_LEVELS)
agreement = support == 3

# Nível de concordância por segmento e concordância de cada algoritmo com o K-Means
ensemble = (pd.crosstab(segment, agreement_level, normalize="index")[list(AGREEMENT_LEVELS.values())] * 100).rename_axis(columns=None)
ensemble["concordancia_GMM_pct"] = 100 * (votes["gmm"] == segment).groupby(segment).mean()
ensemble["concordancia_Ward_pct"] = 100 * (votes["ward"] == segment).groupby(segment).mean()
ensemble = ensemble.rename(index=SEG_LABEL)
display(exec_table(agreement_level.value_counts(normalize=True).mul(100).rename("pct").reset_index(),
                   formats={"pct": "pct"}, labels={"index": "Nível de concordância", "pct": "% dos block groups"}))
display(exec_table(ensemble.reset_index(names="segmento"),
                   formats={c: "pct" for c in ensemble.columns},
                   labels={"segmento": "Segmento", "concordancia_GMM_pct": "Concordância do GMM",
                           "concordancia_Ward_pct": "Concordância do Ward"},
                   highlight=AGREEMENT_LEVELS[3]))

fig, ax = plt.subplots(figsize=(7, 7))
for level, color, size in [(3, LIGHT_GRAY, 1), (2, BLUE, 1.5), (1, ORANGE, 4)]:
    sel = support == level
    ax.scatter(df_feat.loc[sel, "Longitude"], df_feat.loc[sel, "Latitude"], s=size, color=color,
               label=f"{AGREEMENT_LEVELS[level]}: {br(100 * sel.mean())}%")
style_map(ax, "Concordância entre K-Means, GMM e Ward")
ax.legend(loc="upper right", markerscale=4)
action_title(fig, f"A maioria dos algoritmos confirma o segmento de {br(100 * (support >= 2).mean(), 1)}% dos bairros")
finish(fig)
''')

md(r'''
[[INTERP-ENSEMBLE]]
''')

# ---------------------------------------------------------------- 9. Estratégias
md(r'''
---
# 9. Estratégias de Negócio por Segmento

Descrever os segmentos não basta: precisamos transformar esse conhecimento em **ações concretas**. Esta seção constrói, a partir dos dados, os indicadores de que um comitê de investimento e marketing precisa para decidir onde e como atuar.

## 9.1 Tamanho de mercado
''')

code(r'''
# Tamanho de mercado: domicílios, população e valor estimado do estoque (domicílios x valor mediano)
seg["valor_estoque_usd"] = seg["households"] * seg["MedHouseVal"] * 100_000
market = pd.DataFrame({
    "segmento": [SEG_LABEL[s] for s in SEGMENTS],
    "domicilios": grouped["households"].sum().round(),
    "pct_domicilios": profile["pct_domicilios"],
    "populacao": grouped["Population"].sum(),
    "valor_estoque_usd_bi": seg.groupby("segmento")["valor_estoque_usd"].sum() / 1e9,
}).set_index("segmento")
market["pct_valor_estoque"] = 100 * market["valor_estoque_usd_bi"] / market["valor_estoque_usd_bi"].sum()
exec_table(market.reset_index(),
           formats={"domicilios": "int", "pct_domicilios": "pct", "populacao": "int",
                    "valor_estoque_usd_bi": "usd_bi", "pct_valor_estoque": "pct"},
           labels={"segmento": "Segmento", "domicilios": "Domicílios", "pct_domicilios": "% dos domicílios",
                   "populacao": "População", "valor_estoque_usd_bi": "Valor do estoque",
                   "pct_valor_estoque": "% do valor"},
           highlight="pct_valor_estoque", caption="Tamanho de mercado de cada segmento (valores de 1990)")
''')

md(r'''
[[INTERP-MARKET]]

## 9.2 Oportunidades de investimento: crescimento e subvalorização

**Crescimento.** Os dados são uma fotografia de 1990, sem série histórica. Usamos como indicador de crescimento a **participação de block groups com casas de até 10 anos**: onde se construiu muito recentemente, há expansão urbana, demanda nova e terrenos sendo incorporados.

**Áreas subvalorizadas.** Para cada block group, estimamos o **valor esperado** das casas a partir das suas características (renda, idade, tamanho, ocupação, distância da costa, densidade, acesso a grandes cidades e localização), com um modelo de *gradient boosting*. Cada previsão é feita **sem que o modelo tenha visto aquele block group** (validação cruzada em 5 partes). Um block group cujo valor real está **20% ou mais abaixo do esperado** é marcado como **subvalorizado**: tem fundamentos de um bairro mais caro, mas preço de um mais barato. Block groups no teto de US\$ 500 mil ficam fora dessa marcação, porque o valor real deles é desconhecido.

> Este é o único passo supervisionado do projeto. Ele não altera os segmentos: é uma ferramenta de apoio para priorizar oportunidades **dentro** deles.
''')

code(r'''
# Modelo de valor esperado: gradient boosting com previsão fora da amostra (validação cruzada em 5 partes)
VALUE_MODEL_FEATURES = ["MedInc", "HouseAge", "AveRooms", "AveBedrms", "AveOccup", "Population",
                        "dist_coast_km", "pop_density_3km", "dist_big_city_km", "Latitude", "Longitude"]
value_model = HistGradientBoostingRegressor(max_iter=400, learning_rate=0.06, random_state=RANDOM_STATE)
log_value = np.log(df_feat["MedHouseVal"])
predicted_log = cross_val_predict(value_model, df_feat[VALUE_MODEL_FEATURES], log_value,
                                  cv=KFold(5, shuffle=True, random_state=RANDOM_STATE))
print(f"Qualidade do modelo de valor esperado (R², validação cruzada): {r2_score(log_value, predicted_log):.3f}")

# Razão entre preço real e esperado; subvalorizado = 20% ou mais abaixo do esperado (fora do teto)
seg["valor_esperado_usd"] = np.exp(predicted_log) * 100_000
seg["preco_vs_esperado"] = seg["MedHouseVal"] * 100_000 / seg["valor_esperado_usd"]
seg["subvalorizado"] = (seg["preco_vs_esperado"] <= 0.8) & ~seg["no_teto"]
seg["sobrevalorizado"] = (seg["preco_vs_esperado"] >= 1.25) & ~seg["no_teto"]

# Indicadores de crescimento, oportunidade e risco de preço por segmento
opportunity = pd.DataFrame({
    "segmento": [SEG_LABEL[s] for s in SEGMENTS],
    "pct_casas_ate_10_anos": profile["pct_casas_ate_10_anos"],
    "pct_subvalorizados": 100 * seg.groupby("segmento")["subvalorizado"].mean(),
    "domicilios_em_areas_subvalorizadas": seg[seg["subvalorizado"]].groupby("segmento")["households"].sum().reindex(SEGMENTS, fill_value=0).round(),
    "pct_sobrevalorizados": 100 * seg.groupby("segmento")["sobrevalorizado"].mean(),
    "anos_de_renda_por_casa": profile["anos_de_renda_por_casa"],
    "dispersao_preco_IQR_sobre_mediana": (profile["valor_p75_usd"] - profile["valor_p25_usd"]) / profile["valor_mediano_usd"],
    "pct_no_teto_500k": profile["pct_no_teto_500k"],
}).set_index("segmento")
exec_table(opportunity.reset_index(),
           formats={"pct_casas_ate_10_anos": "pct", "pct_subvalorizados": "pct",
                    "domicilios_em_areas_subvalorizadas": "int", "pct_sobrevalorizados": "pct",
                    "anos_de_renda_por_casa": "dec1", "dispersao_preco_IQR_sobre_mediana": "dec2",
                    "pct_no_teto_500k": "pct"},
           labels={"segmento": "Segmento", "pct_casas_ate_10_anos": "Casas de até 10 anos",
                   "pct_subvalorizados": "Subvalorizados",
                   "domicilios_em_areas_subvalorizadas": "Domicílios em áreas subvalorizadas",
                   "pct_sobrevalorizados": "Sobrevalorizados", "anos_de_renda_por_casa": "Anos de renda por casa",
                   "dispersao_preco_IQR_sobre_mediana": "Dispersão de preço (IQR ÷ mediana)",
                   "pct_no_teto_500k": "No teto de US$ 500 mil"},
           highlight="pct_subvalorizados")
''')

code(r'''
# Mapa dos block groups subvalorizados, coloridos pelo segmento
fig, ax = plt.subplots(figsize=(7.5, 7.5))
ax.scatter(df_feat["Longitude"], df_feat["Latitude"], s=0.5, color="#e1e0d9")
under = seg[seg["subvalorizado"]]
for s in SEGMENTS:
    sel = under[under["segmento"] == s]
    ax.scatter(sel["Longitude"], sel["Latitude"], s=4, color=SEG_COLOR[s], label=f"{SEG_LABEL[s]} ({br(len(sel))})")
coast.plot(ax=ax, color=GRAY, linewidth=0.5)
style_map(ax, f"Block groups subvalorizados ({br(len(under))}), por segmento")
ax.legend(loc="upper right", markerscale=3, fontsize=7)
counts = under["segmento"].value_counts()
top_share = 100 * counts.iloc[:2].sum() / len(under)
action_title(fig, f"{br(len(under))} bairros valem 20% ou mais abaixo do esperado; "
                  f"S{counts.index[0]} e S{counts.index[1]} concentram {br(top_share)}% deles")
finish(fig, SOURCE_NOTE + " · Litoral: Natural Earth")
''')

md(r'''
[[INTERP-OPPORTUNITY]]

## 9.3 Matriz de priorização

Combinamos quatro critérios, cada um normalizado de 0 a 1 entre os segmentos:

| Critério | Medida | Por que importa |
|---|---|---|
| **Crescimento** | % de block groups com casas de até 10 anos | demanda nova e lançamentos |
| **Oportunidade de preço** | % de block groups subvalorizados | espaço para valorização e captação de imóveis |
| **Tamanho em clientes** | número de domicílios | alcance de marketing e volume de transações |
| **Tamanho em valor** | valor estimado do estoque (US\$) | a comissão é proporcional ao preço: receita potencial |

O **índice de atratividade** é a média simples dos quatro, sem pesos escolhidos a dedo.
''')

code(r'''
# Normaliza um critério para a faixa 0 a 1 entre os segmentos
def minmax(series):
    return (series - series.min()) / (series.max() - series.min())


# Índice de atratividade = média simples dos quatro critérios normalizados
priority = pd.DataFrame({
    "crescimento": minmax(opportunity["pct_casas_ate_10_anos"]),
    "oportunidade_de_preco": minmax(opportunity["pct_subvalorizados"]),
    "tamanho_em_clientes": minmax(market["domicilios"]),
    "tamanho_em_valor": minmax(market["valor_estoque_usd_bi"]),
})
priority["indice_atratividade"] = priority.mean(axis=1)
priority = priority.sort_values("indice_atratividade", ascending=False)
display(exec_table(priority.reset_index(),
                   formats={c: "dec2" for c in priority.columns},
                   labels={"segmento": "Segmento", "crescimento": "Crescimento",
                           "oportunidade_de_preco": "Oportunidade de preço", "tamanho_em_clientes": "Tamanho em clientes",
                           "tamanho_em_valor": "Tamanho em valor", "indice_atratividade": "Índice de atratividade"},
                   highlight="indice_atratividade"))

# Matriz de priorização: crescimento x oportunidade, bolha proporcional aos domicílios
fig, ax = plt.subplots(figsize=(10, 6.5))
for s in SEGMENTS:
    name = SEG_LABEL[s]
    x, y = opportunity.loc[name, "pct_casas_ate_10_anos"], opportunity.loc[name, "pct_subvalorizados"]
    ax.scatter(x, y, s=market.loc[name, "domicilios"] / 1_500, color=SEG_COLOR[s], alpha=0.85,
               edgecolor=SURFACE, linewidth=2, label=name)
    ax.annotate(f"S{s}", (x, y), ha="center", va="center", fontsize=9, fontweight="bold", color=INK)
ax.axvline(opportunity["pct_casas_ate_10_anos"].median(), color=LIGHT_GRAY, linestyle="--", linewidth=1)
ax.axhline(opportunity["pct_subvalorizados"].median(), color=LIGHT_GRAY, linestyle="--", linewidth=1)
ax.set_title("Tamanho da bolha = número de domicílios")
ax.set_xlabel("crescimento: % de block groups com casas de até 10 anos")
ax.set_ylabel("oportunidade: % de block groups subvalorizados")
ax.margins(0.25)
legend = ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), labelspacing=1.2)
for handle in legend.legend_handles:
    handle.set_sizes([60])
leader = priority.index[0]
action_title(fig, f"Matriz de priorização: {leader.split(' · ')[0]} lidera o índice de atratividade")
finish(fig)
''')

md(r'''
[[INTERP-PRIORITY]]

## 9.4 Alocação de orçamento de marketing e equipes de vendas

Uma regra simples e auditável: o peso de cada segmento é a sua **participação nos domicílios** multiplicada por **(0,5 + índice de atratividade)**. Assim, todo segmento recebe atenção proporcional ao seu tamanho, e os segmentos mais atrativos recebem até 3× mais por domicílio. Para ilustrar, distribuímos um orçamento anual de **US\$ 10 milhões** e uma equipe de **100 corretores**.
''')

code(r'''
# Orçamento anual e tamanho da equipe usados no exemplo
BUDGET_USD = 10_000_000
SALES_TEAM = 100

# O peso de cada segmento é a sua participação nos domicílios vezes (0,5 + atratividade)
allocation = pd.DataFrame({"pct_domicilios": market["pct_domicilios"],
                           "indice_atratividade": priority["indice_atratividade"]})
allocation["peso"] = allocation["pct_domicilios"] * (0.5 + allocation["indice_atratividade"])
allocation["pct_orcamento"] = 100 * allocation["peso"] / allocation["peso"].sum()
allocation["orcamento_usd"] = (BUDGET_USD * allocation["pct_orcamento"] / 100).round(-3)
# Corretores: parte inteira da cota de cada segmento + as vagas restantes para as maiores frações
raw_team = SALES_TEAM * allocation["pct_orcamento"] / 100
team = np.floor(raw_team).astype(int)
team[(raw_team - team).sort_values(ascending=False).index[:SALES_TEAM - team.sum()]] += 1
allocation["corretores"] = team
allocation["onde_posicionar_as_equipes"] = location["cidades_de_referencia"].rename(index=SEG_LABEL)
allocation = allocation.sort_values("pct_orcamento", ascending=False)
exec_table(allocation.drop(columns="peso").reset_index(names="segmento"),
           formats={"pct_domicilios": "pct", "indice_atratividade": "dec2", "pct_orcamento": "pct",
                    "orcamento_usd": "usd", "corretores": "int"},
           labels={"segmento": "Segmento", "pct_domicilios": "% dos domicílios",
                   "indice_atratividade": "Atratividade", "pct_orcamento": "% do orçamento",
                   "orcamento_usd": "Orçamento anual", "corretores": "Corretores",
                   "onde_posicionar_as_equipes": "Onde posicionar as equipes"},
           highlight="pct_orcamento", caption="Proposta de alocação: US$ 10 milhões e 100 corretores")
''')

md(r'''
[[INTERP-ALLOCATION]]

## 9.5 Estratégias por segmento

[[INTERP-STRATEGIES]]
''')

md(r'''
## 9.6 Respostas diretas às perguntas de negócio

[[INTERP-BUSINESS-QA]]
''')

md(r'''
## 9.7 Como a imobiliária aplica a segmentação no dia a dia

A segmentação só gera valor se chegar ao CRM e às equipes. Deixamos dois artefatos prontos:

1. **Um arquivo** com o segmento de cada block group, o nome do segmento, o nível de concordância entre os algoritmos e a marcação de subvalorização, para cruzar com a base de clientes e imóveis.
2. **Uma função** que classifica **novos** block groups (ou atualizações do Censo) no segmento certo, aplicando exatamente o mesmo tratamento, as mesmas features e o mesmo modelo.
''')

code(r'''
# Arquivo para o CRM: segmento, nome, concordância, subvalorização e localização de cada block group
export = pd.DataFrame({
    "segmento": segment, "nome_segmento": segment_name, "concordancia_algoritmos": agreement_level,
    "subvalorizado": seg["subvalorizado"], "valor_esperado_usd": seg["valor_esperado_usd"].round(-2),
    "valor_mediano_usd": df_feat["MedHouseVal"] * 100_000, "renda_mediana_usd": df_feat["MedInc"] * 10_000,
    "domicilios": df_feat["households"].round(), "dist_costa_km": df_feat["dist_coast_km"].round(2),
    "faixa_costeira": df_feat["coastal_class"], "latitude": df_feat["Latitude"], "longitude": df_feat["Longitude"],
    "condado": df_feat["county"], "regiao": df_feat["region"], "cidade_de_referencia": df_feat["nearest_city"],
})
export_path = DATA_DIR / "segmentos_california.csv"
export.to_csv(export_path, index_label="block_group_id")
print(f"Arquivo salvo: {export_path} ({len(export):,} linhas)")
export.head(3)
''')

code(r'''
def assign_segment(new_block_groups):
    """Classifica novos block groups (com as colunas originais do Censo) num segmento de mercado."""
    data = new_block_groups.copy()
    # Recalcula as features geográficas usadas no modelo
    data["dist_coast_km"] = distance_to_coast_km(data["Latitude"], data["Longitude"], data.index)
    data["pop_density_3km"] = density_3km(np.radians(data[["Latitude", "Longitude"]].to_numpy()))
    # Mesmo tratamento de outliers e transformações do treino
    features = pd.concat([treat_outliers(data[df_clean.columns]),
                          treat_new_features(data[["dist_coast_km", "pop_density_3km"]])], axis=1)[FINAL_FEATURES]
    # Mesmo scaler e mesmo K-Means; o rótulo é renumerado como nos segmentos
    raw_labels = km_final.predict(pd.DataFrame(final_scaler.transform(features), columns=FINAL_FEATURES,
                                               index=features.index))
    segments = pd.Series(raw_labels, index=data.index).map(RELABEL)
    return pd.DataFrame({"segmento": segments, "nome_segmento": segments.map(SEGMENT_NAMES)})


# Teste: a função deve reproduzir o segmento dos block groups já classificados
check_rows = df_clean.sample(500, random_state=RANDOM_STATE)
reassigned = assign_segment(check_rows)
print(f"Teste de consistência: {(reassigned['segmento'] == segment.loc[check_rows.index]).mean():.1%} "
      "dos 500 block groups recebem o mesmo segmento")

# Exemplo de uso com dois block groups hipotéticos
new_example = pd.DataFrame({"MedInc": [9.5, 2.6], "HouseAge": [15, 22], "AveRooms": [7.2, 5.4],
                            "AveBedrms": [1.05, 1.08], "Population": [1_100, 1_200], "AveOccup": [2.8, 2.9],
                            "Latitude": [33.62, 36.80], "Longitude": [-117.85, -119.75],
                            "MedHouseVal": [4.6, 0.78]}, index=["Irvine (exemplo)", "Fresno (exemplo)"])
assign_segment(new_example)
''')

md(r'''
[[INTERP-CALLOUT-9]]
''')

# ---------------------------------------------------------------- 10. Conclusão
md(r'''
---
# 10. Conclusão Final

[[INTERP-CONCLUSION]]
''')
