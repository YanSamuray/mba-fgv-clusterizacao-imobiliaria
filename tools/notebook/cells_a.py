CELLS = []


def md(text):
    CELLS.append(("md", text))


def code(text):
    CELLS.append(("code", text))


# ---------------------------------------------------------------- 0. Identificação
md(r'''
# Projeto Final — Segmentação do Mercado Imobiliário da Califórnia com Clusterização

### Seis tipos de bairro, uma estratégia para cada um

**Disciplina:** Aprendizado Não Supervisionado (Prof. Sergio Polimante) · Executive MBA em Business Analytics e Big Data · FGV

**Integrantes:**

1. Jorge Adriano Fontes de Almeida Filho
2. Rafael Collet
3. Stephanie Santin Padovesi
4. Thaís Pereira de Vasconcelos Moreira
5. Yan Samuray Siepamann Vieira

**Dados:** California Housing (Censo dos EUA, 1990), com 20.640 vizinhanças, enriquecido com dados de litoral, condados e cidades · **Stack:** Python, pandas, scikit-learn, GeoPandas, Matplotlib
''')

# ---------------------------------------------------------------- Resumo executivo
md(r'''
# Resumo executivo

**A pergunta:** a imobiliária segmenta a Califórnia por cidade e por faixa de preço. Existe uma divisão melhor, baseada no comportamento real dos bairros?

**A resposta:** sim. Agrupamos 20.555 vizinhanças com clusterização e encontramos **seis tipos de bairro**. Eles se repetem em todo o estado, são estáveis e pedem estratégias diferentes.

[[HERO_IMAGE]]

### Cinco achados

1. **Preço não define o cliente.** Três segmentos têm o mesmo preço mediano (cerca de US\$ 210 mil): apartamentos compactos perto do mar, casas novas de famílias no subúrbio e casas antigas da classe média. A segmentação por faixa de preço mistura os três.
2. **O mar vale por si só.** A casa mediana custa US\$ 256 mil até 5 km da costa e US\$ 87 mil a mais de 80 km, embora a renda dos moradores quase não mude.
3. **O crescimento está nos subúrbios.** O segmento S4 tem 23% dos bairros com casas de até 10 anos e é o maior mercado do estado, com 24% dos domicílios.
4. **O alto padrão é pequeno em clientes e grande em valor.** O segmento S6 tem 10% dos domicílios e 21% do valor do estoque de imóveis.
5. **Há oportunidades mapeadas.** Cerca de 1.700 bairros estão pelo menos 20% abaixo do preço que os seus fundamentos indicam, concentrados nos segmentos S3 e S1.

### Os seis segmentos

| Segmento | Domicílios | Casa mediana | Quem é | Papel na estratégia |
|---|---|---|---|---|
| **S1 · Interior acessível** | 18% | US\$ 91 mil | famílias de renda baixa a média no Vale Central, a 110 km do mar | volume e financiamento |
| **S2 · Famílias urbanas populares** | 14% | US\$ 145 mil | famílias grandes nos bairros mais densos de Los Angeles | locação e acesso à moradia |
| **S3 · Urbano compacto costeiro** | 17% | US\$ 206 mil | solteiros e casais em apartamentos a 7 km do mar | investidores e captação |
| **S4 · Subúrbios familiares em expansão** | 24% | US\$ 215 mil | famílias de renda média-alta em casas novas e grandes | **prioridade nº 1:** lançamentos |
| **S5 · Classe média urbana consolidada** | 17% | US\$ 216 mil | classe média nos bairros antigos de Los Angeles e San Francisco | revenda e reforma |
| **S6 · Alto padrão costeiro** | 10% | US\$ 444 mil ou mais | a maior renda do estado, em casas grandes a 5,5 km do mar | margem e relacionamento |

### Três recomendações

1. **Substituir a segmentação por cidade e preço pelos seis segmentos**, aplicando a mesma estratégia por segmento em todas as cidades.
2. **Concentrar cerca de um terço do orçamento e das equipes em S4**, com foco em lançamentos e na troca de imóvel.
3. **Abrir uma frente de investimento em S3**, usando o modelo de valor esperado para captar imóveis subvalorizados, e **tratar S6 como uma operação de luxo** dedicada.

**Como chegamos lá:** 20.555 vizinhanças · 7 variáveis · 4 algoritmos comparados · K-Means com 6 segmentos · estabilidade de 0,94 em 30 reamostragens.

### Como navegar

| Seção | Pergunta que responde |
|---|---|
| 2. Exploração e Análise dos Dados | Como é o mercado? Existem dados faltantes ou estranhos? |
| 3. Pré-processamento | Como preparar os dados para que as distâncias façam sentido? |
| 4. Engenharia de Features | Quais variáveis novas descrevem melhor um tipo de vizinhança? Quais usar? |
| 5. Redução de Dimensionalidade | Quantas dimensões reais o mercado tem? |
| 6. Algoritmos de Clusterização | Qual algoritmo e quantos segmentos? |
| 7. Avaliação e Validação | Os segmentos são bem separados, estáveis e fazem sentido no mapa? |
| 8. Interpretação e Caracterização | Quem é cada segmento? |
| 9. Estratégias de Negócio | O que a empresa deve fazer em cada segmento? |
| 10. Conclusão Final | Qualidade, insights, limitações, próximos passos e recomendações |
''')

# ---------------------------------------------------------------- 1. Introdução
md(r'''
# 1. Introdução e Objetivos

## Contexto de negócio

Somos a equipe de análise de dados da **California Real Estate Analytics**, consultoria de mercado imobiliário que atende uma grande imobiliária da Califórnia, além de investidores institucionais, fundos imobiliários e construtoras. Hoje esses clientes segmentam o mercado do jeito tradicional: por **localização** (norte vs. sul, cidade) ou por **faixa de preço**. Essa divisão esconde diferenças importantes. Dois bairros com o mesmo preço podem ter clientes completamente diferentes (por exemplo, um apartamento pequeno perto da praia e uma casa grande no interior).

A empresa precisa de uma segmentação **baseada em padrões naturais dos dados** para:

- desenvolver **estratégias de marketing** direcionadas;
- **alocar equipes de vendas** e orçamento onde há mais potencial;
- identificar **oportunidades de investimento** (áreas em crescimento e subvalorizadas);
- **personalizar produtos e serviços** para cada tipo de cliente;
- definir **estratégias de precificação** por segmento.

**Metas de negócio** que a segmentação deve apoiar:

- aumentar a taxa de conversão de vendas de **12% para 25 a 30%**, com estratégias por segmento;
- reduzir o tempo médio de venda em **40%**, com marketing direcionado;
- identificar nichos subexplorados que representem **US\$ 50 a 100 milhões** em novos investimentos por ano.

Na conclusão (seção 10) avaliamos o que os resultados permitem afirmar sobre cada meta.

## Objetivo do projeto

Agrupar as vizinhanças da Califórnia em **segmentos de mercado acionáveis**, usando técnicas de clusterização (aprendizado não supervisionado), e traduzir cada segmento em uma estratégia de negócio.

**O que queremos que um segmento represente:** um *tipo* de vizinhança (quem mora lá, como é a moradia e qual é o entorno), e não apenas uma região do mapa. Um "bairro rico no litoral" deve ser reconhecido como tal, esteja ele perto de Los Angeles ou de San Francisco.

## Os dados

O **California Housing Dataset** (Censo dos EUA de 1990) tem 20.640 linhas. Cada linha é um **block group**: uma pequena vizinhança de 600 a 3.000 pessoas, descrita por renda, idade das casas, tamanho das moradias, população, localização e valor mediano das casas.

> **Nota sobre os números:** no texto e nas tabelas de resultados usamos o formato brasileiro (vírgula decimal: 0,5; ponto para milhar: 20.640). As saídas técnicas intermediárias do Python (como `describe()`) mantêm o formato americano (0.5; 20,640).
''')

md(r'''
## Setup

Importamos as bibliotecas e fixamos uma semente aleatória (`RANDOM_STATE`), para que cada execução produza exatamente os mesmos resultados.

Também definimos a identidade visual do relatório:

- **Paleta acessível**, a mesma em todos os gráficos.
- **Títulos que já dizem a conclusão.** O título de cada eixo diz o que está sendo medido.
- **Fonte dos dados** no rodapé de cada figura.
- **Tabelas de resultados** com números no formato brasileiro.
''')

code(r'''
from pathlib import Path
import urllib.request
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, LogNorm, TwoSlopeNorm
import seaborn as sns
import geopandas as gpd
from shapely.geometry import box
from IPython.display import display

from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import squareform, cdist
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import IsolationForest, HistGradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.neighbors import BallTree, NearestNeighbors
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.metrics import (silhouette_score, silhouette_samples, davies_bouldin_score,
                             calinski_harabasz_score, adjusted_rand_score, r2_score)
from sklearn.model_selection import KFold, cross_val_predict

warnings.filterwarnings("ignore", category=FutureWarning)
pd.set_option("display.max_columns", 60)
pd.set_option("display.width", 220)
pd.set_option("display.float_format", lambda x: f"{x:,.3f}")

RANDOM_STATE = 42          # mesma aleatoriedade em toda execução
DATA_DIR = Path("data")    # arquivos externos são baixados aqui uma única vez
DATA_DIR.mkdir(exist_ok=True)
EARTH_RADIUS_KM = 6371
''')

code(r'''
# Paleta acessível (segura para daltonismo nos 3 primeiros tons) e estilo dos gráficos
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = (
    "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948")
PALETTE = [BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED]
GRAY, LIGHT_GRAY, INK, INK_2, SURFACE = "#898781", "#c3c2b7", "#0b0b0b", "#52514e", "#fcfcfb"

BLUES = LinearSegmentedColormap.from_list(
    "azuis", ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
DIVERGING = LinearSegmentedColormap.from_list("divergente", [BLUE, "#f0efec", RED])

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "figure.dpi": 100, "axes.edgecolor": LIGHT_GRAY, "axes.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#e1e0d9", "grid.linewidth": 0.6, "axes.axisbelow": True,
    "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.labelcolor": INK_2, "axes.labelsize": 9,
    "xtick.color": GRAY, "ytick.color": GRAY, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "text.color": INK, "legend.frameon": False, "legend.fontsize": 8,
    "axes.prop_cycle": plt.cycler(color=PALETTE),
    "figure.titlesize": 14, "figure.titleweight": "bold",
    "text.parse_math": False,
})
SOURCE_NOTE = "Fonte: Censo dos EUA (1990), via scikit-learn · Análise da equipe"


def finish(fig, note=SOURCE_NOTE, tight=True):
    """Ajusta o layout, escreve a fonte dos dados no rodapé e exibe a figura."""
    if tight:
        fig.tight_layout()
    fig.text(0.01, 0.0, note, ha="left", va="top", fontsize=7.5, color=GRAY)
    plt.show()


def action_title(fig, text):
    """Título da figura que já diz a conclusão (o título de cada eixo diz o que está sendo medido)."""
    fig.suptitle(text, x=0.01, ha="left")


def br(value, decimals=0):
    """Formata um número no padrão brasileiro: ponto para milhar e vírgula decimal."""
    if round(value, decimals) == 0:
        value = 0.0
    return f"{value:,.{decimals}f}".replace(",", "_").replace(".", ",").replace("_", ".")


# Formatos das tabelas executivas
TABLE_FORMATS = {
    "int": lambda v: br(v),
    "dec1": lambda v: br(v, 1),
    "dec2": lambda v: br(v, 2),
    "dec3": lambda v: br(v, 3),
    "pct": lambda v: f"{br(v, 1)}%",
    "pct0": lambda v: f"{br(v)}%",
    "usd": lambda v: f"US$ {br(v)}",
    "usd_mil": lambda v: f"US$ {br(v / 1000)} mil",
    "usd_bi": lambda v: f"US$ {br(v, 1)} bi",
    "km": lambda v: f"{br(v, 1)} km",
    "anos": lambda v: f"{br(v, 1)} anos",
}


def exec_table(df, formats, labels=None, highlight=None, caption=None, index=False):
    """Tabela de resultados: números no padrão brasileiro, rótulos legíveis e realce opcional numa coluna.

    `formats` associa colunas (ou linhas, em tabelas transpostas) a um formato de TABLE_FORMATS.
    `index=True` mantém os rótulos das linhas visíveis (por exemplo, o nome de cada métrica).
    """
    styler = df.style
    for key, kind in formats.items():
        subset = [key] if key in df.columns else pd.IndexSlice[[key], :]
        styler = styler.format(TABLE_FORMATS[kind], subset=subset, na_rep="–")
    if highlight is not None:
        styler = styler.background_gradient(cmap=BLUES, subset=[highlight], low=0, high=0.6)
    if labels:
        styler = styler.relabel_index([labels.get(c, c) for c in df.columns], axis="columns")
    if caption:
        styler = styler.set_caption(caption)
    styler = styler.hide(axis="index", names=True) if index else styler.hide(axis="index")
    # A classe tex2jax_ignore impede que o Jupyter interprete "US$ ... US$" como fórmula
    return (styler
            .set_table_attributes('class="tex2jax_ignore"')
            .set_table_styles([{"selector": "caption", "props": "text-align: left; font-weight: bold;"},
                               {"selector": "th", "props": "text-align: left;"}], overwrite=False))


def style_map(ax, title=None):
    """Enquadra a Califórnia com a proporção correta entre latitude e longitude."""
    ax.set_xlim(-124.6, -114.0)
    ax.set_ylim(32.4, 42.1)
    ax.set_aspect(1.25)
    ax.set_axis_off()
    if title:
        ax.set_title(title)


def boxplot_style():
    """Parâmetros comuns dos boxplots."""
    return dict(color="#cde2fb", linecolor=GRAY, linewidth=0.8, fliersize=2,
                flierprops={"markerfacecolor": ORANGE, "markeredgecolor": "none", "alpha": 0.5},
                medianprops={"color": BLUE, "linewidth": 2})


def download(url, filename):
    """Baixa um arquivo externo uma única vez e o guarda na pasta data/."""
    path = DATA_DIR / filename
    if not path.exists():
        print(f"Baixando {filename} ...")
        urllib.request.urlretrieve(url, path)
    return path
''')

md(r'''
## Carregar os dados

Usamos a versão do dataset que vem com o **scikit-learn**. Se o download for bloqueado (por um firewall corporativo, por exemplo), a função reconstrói exatamente a mesma tabela a partir de uma cópia pública do arquivo original.
''')

code(r'''
def load_california_housing():
    """Retorna o California Housing como um único DataFrame (8 variáveis + valor das casas)."""
    try:
        return fetch_california_housing(as_frame=True).frame
    except Exception as error:
        print(f"Download do scikit-learn falhou ({error}). Usando a cópia do GitHub.")
        url = ("https://media.githubusercontent.com/media/EpistasisLab/pmlb/"
               "master/datasets/537_houses/537_houses.tsv.gz")
        raw = pd.read_csv(url, sep="\t")
        households = raw["households"].round()
        return pd.DataFrame({
            "MedInc": raw["median_income"].round(4),
            "HouseAge": raw["housing_median_age"].round(),
            "AveRooms": raw["total_rooms"].round() / households,
            "AveBedrms": raw["total_bedrooms"].round() / households,
            "Population": raw["population"].round(),
            "AveOccup": raw["population"].round() / households,
            "Latitude": raw["latitude"].round(2),
            "Longitude": raw["longitude"].round(2),
            "MedHouseVal": raw["target"].round() / 100_000,
        })


df_raw = load_california_housing()
print(f"Linhas: {df_raw.shape[0]:,}  |  Colunas: {df_raw.shape[1]}")
df_raw.head()
''')

md(r'''
### Dicionário de dados

| Coluna | Significado | Unidade |
|---|---|---|
| `MedInc` | Renda mediana dos domicílios | dezenas de milhares de US\$ (3,5 = US\$ 35.000 por ano) |
| `HouseAge` | Idade mediana das casas | anos |
| `AveRooms` | Número médio de cômodos por domicílio | cômodos |
| `AveBedrms` | Número médio de quartos por domicílio | quartos |
| `Population` | Pessoas que moram no block group | pessoas |
| `AveOccup` | Número médio de pessoas por domicílio | pessoas |
| `Latitude` / `Longitude` | Localização do block group | graus |
| `MedHouseVal` | Valor mediano das casas | centenas de milhares de US\$ (2,0 = US\$ 200.000) |

**`MedHouseVal` não é um "alvo" aqui.** Em clustering não existe variável a prever. O preço é tratado como mais uma característica da vizinhança, e uma das mais importantes para o negócio.
''')

# ---------------------------------------------------------------- 2. EDA
md(r'''
---
# 2. Exploração e Análise dos Dados

Antes de agrupar, precisamos entender o mercado: como cada variável se distribui, como elas se relacionam, onde ficam os preços altos e baixos e quais valores são estranhos.

## 2.1 Estrutura, tipos e valores ausentes
''')

code(r'''
# Tipos de dado e contagem de valores preenchidos em cada coluna
df_raw.info()
''')

code(r'''
# Quantidade de nulos, percentual de nulos e número de valores distintos por coluna
data_quality = pd.DataFrame({
    "valores_nulos": df_raw.isna().sum(),
    "pct_nulos": 100 * df_raw.isna().mean(),
    "valores_distintos": df_raw.nunique(),
})
print(f"Total de valores nulos: {df_raw.isna().sum().sum()}")
print(f"Linhas duplicadas: {df_raw.duplicated().sum()}")
data_quality
''')

md(r'''
**Verificação de valores ausentes (documentada):**

- As 9 colunas são numéricas (`float64`) e têm 20.640 valores preenchidos.
- **Não há nenhum valor nulo** e não há linhas duplicadas. Portanto, **nenhuma imputação é necessária** (seção 3.1).
- Ausência de nulos não significa ausência de problemas: valores impossíveis ou extremos podem estar "escondidos" como números válidos. Investigamos isso na seção 2.6.
''')

md(r'''
## 2.2 Estatísticas descritivas de todas as variáveis

Além das estatísticas usuais, mostramos a **assimetria (skew)**: perto de 0 significa uma distribuição simétrica; acima de 1 indica uma cauda longa à direita (poucos valores muito grandes).
''')

code(r'''
# Estatísticas descritivas de todas as variáveis, acrescidas da assimetria (skew)
descriptive = df_raw.describe().T
descriptive["skew"] = df_raw.skew()
descriptive
''')

md(r'''
[[INTERP-DESCRIBE]]
''')

md(r'''
## 2.3 Distribuições
''')

code(r'''
# Um histograma por variável, com a mediana marcada
fig, axes = plt.subplots(3, 3, figsize=(13, 8.5))
for ax, col in zip(axes.flat, df_raw.columns):
    ax.hist(df_raw[col], bins=60, color=BLUE, edgecolor=SURFACE, linewidth=0.3)
    ax.axvline(df_raw[col].median(), color=INK_2, linewidth=1.2, linestyle="--")
    ax.set_title(f"{col}   (assimetria = {br(df_raw[col].skew(), 1)})")
    ax.set_ylabel("block groups")
action_title(fig, "Renda, preço e tamanho das moradias têm caudas longas; preço e idade têm um teto artificial")
finish(fig)
''')

md(r'''
[[INTERP-HIST]]
''')

md(r'''
## 2.4 Correlações entre as variáveis
''')

code(r'''
# Correlação de Pearson entre as variáveis originais (só o triângulo inferior, sem repetição)
corr_raw = df_raw.corr(method="pearson")
upper_mask = np.triu(np.ones_like(corr_raw, dtype=bool), k=1)

fig, ax = plt.subplots(figsize=(8.5, 7))
sns.heatmap(corr_raw, mask=upper_mask, cmap=DIVERGING, vmin=-1, vmax=1, annot=True, fmt=".2f",
            annot_kws={"fontsize": 8}, linewidths=0.5, linecolor=SURFACE, square=True,
            cbar_kws={"shrink": 0.7, "label": "correlação de Pearson"}, ax=ax)
ax.set_title("Correlação de Pearson entre as variáveis originais")
ax.grid(False)
action_title(fig, f"A renda é a variável que mais acompanha o preço (r = {br(corr_raw.loc['MedInc', 'MedHouseVal'], 2)})")
finish(fig)

# Os pares de variáveis com as correlações mais fortes, em valor absoluto
pairs = corr_raw.where(upper_mask).stack().rename("correlação")
pairs.reindex(pairs.abs().sort_values(ascending=False).index).head(6).to_frame()
''')

md(r'''
[[INTERP-CORR]]
''')

md(r'''
## 2.5 Padrões geográficos e demográficos

### Onde ficam os preços e as rendas altas?
''')

code(r'''
# Mapas de dispersão (longitude x latitude) coloridos pelo valor das casas e pela renda
fig, axes = plt.subplots(1, 2, figsize=(13, 6.5))
for ax, col, factor, title in [
        (axes[0], "MedHouseVal", 100, "Valor mediano das casas (US$ mil)"),
        (axes[1], "MedInc", 10, "Renda mediana dos domicílios (US$ mil por ano)")]:
    order = df_raw[col].sort_values().index        # valores altos desenhados por cima
    points = ax.scatter(df_raw.loc[order, "Longitude"], df_raw.loc[order, "Latitude"],
                        c=df_raw.loc[order, col] * factor, cmap=BLUES, s=2)
    fig.colorbar(points, ax=ax, shrink=0.6, label="US$ mil")
    style_map(ax, title)
action_title(fig, "Preços e rendas altos se concentram numa faixa estreita do litoral")
finish(fig)
''')

md(r'''
[[INTERP-MAPS]]
''')

md(r'''
### Estatísticas descritivas por região

O dataset só tem latitude e longitude. Para analisar o mercado por região, **juntamos dados externos**:

1. **Condado:** os limites oficiais dos 58 condados da Califórnia (US Census Bureau, arquivo GeoJSON). Um *spatial join* encontra o condado que contém cada block group. Pontos no litoral que caem "no mar" (os limites são simplificados) recebem o condado mais próximo.
2. **Região:** uma tabela condado → região, com as 10 regiões usadas pelo governo da Califórnia no Censo de 2020.
''')

code(r'''
# Limites oficiais dos condados (GeoJSON) para descobrir em qual condado está cada block group
counties_path = download(
    "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
    "us_counties_fips.geojson")
ca_counties = (gpd.read_file(counties_path)
               .query("STATE == '06'")
               .rename(columns={"NAME": "county"})[["county", "geometry"]])

# Spatial join: o condado cujo polígono contém o ponto de cada block group
points = gpd.GeoDataFrame(index=df_raw.index, crs="EPSG:4326",
                          geometry=gpd.points_from_xy(df_raw["Longitude"], df_raw["Latitude"]))
joined = gpd.sjoin(points, ca_counties, predicate="within", how="left")
joined = joined[~joined.index.duplicated(keep="first")]

# Pontos fora de todos os polígonos (litoral simplificado): condado mais próximo, em metros
outside = joined["county"].isna()
nearest = gpd.sjoin_nearest(points[outside].to_crs("EPSG:3310"), ca_counties.to_crs("EPSG:3310"),
                            how="left")
joined.loc[outside, "county"] = nearest.loc[~nearest.index.duplicated(), "county"]

# Tabela condado -> região (10 regiões do Censo de 2020 da Califórnia)
REGIONS = {
    "Superior California": ["Butte", "Colusa", "El Dorado", "Glenn", "Lassen", "Modoc", "Nevada",
                            "Placer", "Plumas", "Sacramento", "Shasta", "Sierra", "Siskiyou",
                            "Sutter", "Tehama", "Yolo", "Yuba"],
    "North Coast": ["Del Norte", "Humboldt", "Lake", "Mendocino", "Napa", "Sonoma", "Trinity"],
    "San Francisco Bay Area": ["Alameda", "Contra Costa", "Marin", "San Francisco", "San Mateo",
                               "Santa Clara", "Solano"],
    "Northern San Joaquin Valley": ["Alpine", "Amador", "Calaveras", "Madera", "Mariposa", "Merced",
                                    "Mono", "San Joaquin", "Stanislaus", "Tuolumne"],
    "Central Coast": ["Monterey", "San Benito", "San Luis Obispo", "Santa Barbara", "Santa Cruz",
                      "Ventura"],
    "Southern San Joaquin Valley": ["Fresno", "Inyo", "Kern", "Kings", "Tulare"],
    "Inland Empire": ["Riverside", "San Bernardino"],
    "Los Angeles County": ["Los Angeles"],
    "Orange County": ["Orange"],
    "San Diego - Imperial": ["Imperial", "San Diego"],
}
county_to_region = {county: region for region, counties in REGIONS.items() for county in counties}

geo = pd.DataFrame({"county": joined["county"]}, index=df_raw.index)
geo["region"] = geo["county"].map(county_to_region)
print(f"Block groups sem condado: {geo['county'].isna().sum()} | sem região: {geo['region'].isna().sum()}")
''')

code(r'''
# Estatísticas por região, convertidas para dólares, ordenadas pelo valor mediano das casas
value_ceiling = df_raw["MedHouseVal"].max()
region_stats = (df_raw.assign(region=geo["region"])
                .groupby("region")
                .agg(block_groups=("MedInc", "size"),
                     renda_mediana_usd=("MedInc", "median"),
                     valor_mediano_usd=("MedHouseVal", "median"),
                     pct_no_teto_500k=("MedHouseVal", lambda s: 100 * (s == value_ceiling).mean()),
                     idade_mediana_anos=("HouseAge", "median"),
                     comodos_por_domicilio=("AveRooms", "median"),
                     pessoas_por_domicilio=("AveOccup", "median"),
                     populacao_total=("Population", "sum"))
                .sort_values("valor_mediano_usd", ascending=False))
region_stats["renda_mediana_usd"] = (region_stats["renda_mediana_usd"] * 10_000).round(-2)
region_stats["valor_mediano_usd"] = (region_stats["valor_mediano_usd"] * 100_000).round(-3)
exec_table(region_stats.reset_index(),
           formats={"block_groups": "int", "renda_mediana_usd": "usd_mil", "valor_mediano_usd": "usd_mil",
                    "pct_no_teto_500k": "pct", "idade_mediana_anos": "int", "comodos_por_domicilio": "dec1",
                    "pessoas_por_domicilio": "dec1", "populacao_total": "int"},
           labels={"region": "Região", "block_groups": "Block groups", "renda_mediana_usd": "Renda mediana",
                   "valor_mediano_usd": "Valor mediano", "pct_no_teto_500k": "No teto de US$ 500 mil",
                   "idade_mediana_anos": "Idade das casas (anos)", "comodos_por_domicilio": "Cômodos",
                   "pessoas_por_domicilio": "Pessoas/domicílio", "populacao_total": "População"},
           highlight="valor_mediano_usd", caption="Estatísticas descritivas por região (medianas)")
''')

md(r'''
[[INTERP-REGION]]
''')

md(r'''
### Identificando possíveis segmentos visualmente

A relação entre **renda** e **valor das casas** é o eixo central do mercado. Separamos as regiões em três grandes áreas para ver se elas formam padrões diferentes nesse gráfico.
''')

code(r'''
# Agrupa as regiões em três grandes áreas para a análise visual
AREA_OF_REGION = {
    "San Francisco Bay Area": "Metrópoles do litoral", "Los Angeles County": "Metrópoles do litoral",
    "Orange County": "Metrópoles do litoral", "San Diego - Imperial": "Metrópoles do litoral",
    "Central Coast": "Costa central e norte", "North Coast": "Costa central e norte",
}
area = geo["region"].map(AREA_OF_REGION).fillna("Interior")
AREAS = ["Metrópoles do litoral", "Costa central e norte", "Interior"]

# Renda e valor medianos por área, e quantas vezes a renda anual a casa custa
area_summary = (df_raw.groupby(area)[["MedInc", "MedHouseVal"]].median()
                .assign(preco_por_renda=lambda d: (d["MedHouseVal"] * 100_000) / (d["MedInc"] * 10_000))
                .reindex(AREAS))

fig, axes = plt.subplots(1, 3, figsize=(14, 4.6), sharex=True, sharey=True)
for ax, name, color in zip(axes, AREAS, [BLUE, ORANGE, AQUA]):
    inside = area == name
    ax.scatter(df_raw.loc[~inside, "MedInc"] * 10, df_raw.loc[~inside, "MedHouseVal"] * 100,
               s=2, color="#e1e0d9")
    ax.scatter(df_raw.loc[inside, "MedInc"] * 10, df_raw.loc[inside, "MedHouseVal"] * 100,
               s=2, color=color, alpha=0.5)
    ax.set_title(f"{name} ({br(inside.sum())} block groups)")
    ax.set_xlabel("renda mediana (US$ mil por ano)")
axes[0].set_ylabel("valor mediano das casas (US$ mil)")
action_title(fig, f"No interior, a casa custa {br(area_summary.loc['Interior', 'preco_por_renda'], 1)} anos de renda; "
                  f"nas metrópoles do litoral, {br(area_summary.loc['Metrópoles do litoral', 'preco_por_renda'], 1)}")
finish(fig)

exec_table(area_summary.assign(MedInc=area_summary["MedInc"] * 10_000,
                               MedHouseVal=area_summary["MedHouseVal"] * 100_000).reset_index(names="area"),
           formats={"MedInc": "usd_mil", "MedHouseVal": "usd_mil", "preco_por_renda": "dec1"},
           labels={"area": "Área", "MedInc": "Renda mediana", "MedHouseVal": "Valor mediano",
                   "preco_por_renda": "Anos de renda por casa"})
''')

md(r'''
[[INTERP-VISUAL-SEGMENTS]]
''')

md(r'''
## 2.6 Identificação de outliers

Um **outlier** é um valor muito diferente do resto, mas "diferente" não significa "errado". Para clustering, outliers importam porque o K-Means coloca o centro de cada cluster na **média** dos seus pontos: um único ponto extremo pode arrastar um centro para longe ou virar um cluster sozinho.

Usamos três lentes complementares:

1. **Regra do IQR (boxplot):** olha uma coluna de cada vez.
2. **Valores de teto:** valores gravados no limite máximo do Censo.
3. **Isolation Forest:** olha todas as colunas juntas (anomalias multivariadas).

Depois perguntamos o mais importante: **o que essas linhas são no mundo real?**

### Regra do IQR e boxplots

Um valor é outlier se cair fora de `[Q1 − 1,5 × IQR, Q3 + 1,5 × IQR]`, em que `IQR = Q3 − Q1`. Os quartis não são puxados por valores extremos, o que torna a regra mais robusta que o z-score em dados assimétricos.
''')

code(r'''
def iqr_bounds(series, k=1.5):
    """Limites (inferior, superior) da regra do IQR para uma coluna."""
    q1, q3 = series.quantile([0.25, 0.75])
    return q1 - k * (q3 - q1), q3 + k * (q3 - q1)


# Marca, coluna a coluna, os valores fora dos limites do IQR
iqr_flags = pd.DataFrame({col: ~df_raw[col].between(*iqr_bounds(df_raw[col])) for col in df_raw.columns})
iqr_table = pd.DataFrame({
    "limite_inferior": [iqr_bounds(df_raw[c])[0] for c in df_raw.columns],
    "limite_superior": [iqr_bounds(df_raw[c])[1] for c in df_raw.columns],
    "outliers": iqr_flags.sum(),
    "pct_outliers": 100 * iqr_flags.mean(),
}, index=df_raw.columns)
iqr_any = iqr_flags.any(axis=1)
print(f"Linhas marcadas em pelo menos uma coluna: {iqr_any.sum():,} ({iqr_any.mean():.1%})")
iqr_table
''')

code(r'''
# Boxplot de cada variável, com o percentual de outliers no título
fig, axes = plt.subplots(3, 3, figsize=(13, 6.5))
for ax, col in zip(axes.flat, df_raw.columns):
    sns.boxplot(x=df_raw[col], ax=ax, **boxplot_style())
    ax.set_title(f"{col}   ({br(iqr_table.loc[col, 'pct_outliers'], 1)}% outliers)")
    ax.set_xlabel("")
action_title(fig, f"A regra do IQR marca {br(100 * iqr_any.mean())}% das linhas: quase tudo é cauda natural, "
                  "de um lado só (pontos laranja)")
finish(fig)
''')

md(r'''
[[INTERP-IQR]]
''')

md(r'''
### Valores de teto (censura)

Alguns campos do Censo gravam todo valor acima de um limite **como o próprio limite**. Para encontrá-los, contamos quantas linhas têm exatamente o valor máximo: numa coluna normal, só uma ou duas.
''')

code(r'''
# Conta quantas linhas têm exatamente o valor máximo de cada coluna (sinal de teto/censura)
ceiling = pd.DataFrame({"valor_maximo": df_raw.max(), "linhas_no_maximo": (df_raw == df_raw.max()).sum()})
ceiling["pct_no_maximo"] = 100 * ceiling["linhas_no_maximo"] / len(df_raw)
display(ceiling.sort_values("linhas_no_maximo", ascending=False).head(4))

# Histogramas das três colunas censuradas, com o teto marcado em laranja
fig, axes = plt.subplots(1, 3, figsize=(13, 3.2))
for ax, col in zip(axes, ["HouseAge", "MedHouseVal", "MedInc"]):
    ax.hist(df_raw[col], bins=50, color=BLUE, edgecolor=SURFACE, linewidth=0.3)
    ax.axvline(df_raw[col].max(), color=ORANGE, linewidth=2)
    ax.set_title(f"{col}: {br(ceiling.loc[col, 'linhas_no_maximo'])} linhas no teto ({br(df_raw[col].max(), 0)})")
    ax.set_ylabel("block groups")
action_title(fig, "Três colunas foram censuradas no limite máximo do Censo (linha laranja)")
finish(fig)
''')

md(r'''
[[INTERP-CEILING]]
''')

md(r'''
### A regra do IQR na escala log

Em colunas assimétricas, a cauda longa à direita é *normal*, mas a regra do IQR a marca mesmo assim. Uma transformação log comprime a cauda. Se um valor **continua** sendo outlier na escala log, ele é de fato extremo.
''')

code(r'''
# Compara o número de outliers do IQR na escala original e na escala log, nas colunas assimétricas
skewed_cols = [col for col in df_raw.columns if df_raw[col].skew() > 0.5]
log_compare = pd.DataFrame({
    "outliers_escala_original": [iqr_flags[c].sum() for c in skewed_cols],
    "outliers_escala_log": [(~np.log(df_raw[c]).between(*iqr_bounds(np.log(df_raw[c])))).sum()
                            for c in skewed_cols],
}, index=skewed_cols)
log_compare["variacao_pct"] = 100 * (log_compare["outliers_escala_log"] / log_compare["outliers_escala_original"] - 1)
log_compare
''')

md(r'''
[[INTERP-LOGIQR]]
''')

md(r'''
### Isolation Forest: anomalias multivariadas

- O algoritmo constrói muitas árvores com cortes aleatórios. Um ponto **comum** precisa de muitos cortes para ficar isolado; um ponto **incomum** fica isolado com poucos cortes.
- Ele olha **todas as colunas ao mesmo tempo** e não precisa de scaling.
- A fração esperada de anomalias (`contamination`) é uma escolha de negócio. Usamos **1%**: o suficiente para encontrar os casos mais isolados sem marcar vizinhanças normais.
''')

code(r'''
# Isolation Forest sobre todas as colunas: marca o 1% de linhas mais fáceis de isolar
iso = IsolationForest(n_estimators=300, contamination=0.01, random_state=RANDOM_STATE, n_jobs=-1)
if_flag = pd.Series(iso.fit_predict(df_raw) == -1, index=df_raw.index)

# Onde ficam, no mapa, as linhas marcadas por cada método
fig, axes = plt.subplots(1, 2, figsize=(12, 5.5), sharex=True, sharey=True)
for ax, flag, name in [(axes[0], iqr_any, "Regra do IQR (qualquer coluna)"),
                       (axes[1], if_flag, "Isolation Forest (1% mais isolados)")]:
    ax.scatter(df_raw.loc[~flag, "Longitude"], df_raw.loc[~flag, "Latitude"], s=2, color=LIGHT_GRAY,
               label="normal")
    ax.scatter(df_raw.loc[flag, "Longitude"], df_raw.loc[flag, "Latitude"], s=6, color=ORANGE,
               label="marcado")
    style_map(ax, f"{name}: {br(flag.sum())} linhas")
    ax.legend(loc="upper right", markerscale=3)
action_title(fig, f"O IQR espalha {br(iqr_any.sum())} marcações pelo estado; "
                  f"o Isolation Forest isola só {br(if_flag.sum())} casos")
finish(fig)

# Perfil típico (mediana) das anomalias comparado com o das linhas normais
anomaly_profile = pd.DataFrame({
    "mediana_linhas_normais": df_raw[~if_flag].median(),
    "mediana_anomalias_IF": df_raw[if_flag].median(),
})
anomaly_profile["razao"] = anomaly_profile["mediana_anomalias_IF"] / anomaly_profile["mediana_linhas_normais"]
anomaly_profile
''')

md(r'''
[[INTERP-IF]]
''')

md(r'''
### Quem são os outliers? Dando significado de negócio

Os detectores dizem **quais** linhas são estranhas, mas não **por quê**. Reconstruímos uma coluna escondida, o **número de domicílios** (`Population / AveOccup`), e olhamos os casos mais extremos.
''')

code(r'''
# Número de domicílios = população / pessoas por domicílio (coluna que o dataset não traz)
households_raw = (df_raw["Population"] / df_raw["AveOccup"]).round()
with_households = df_raw.assign(households=households_raw)

print("Maiores AveOccup (pessoas por domicílio)")
display(with_households.nlargest(6, "AveOccup"))
print("Maiores AveRooms (cômodos por domicílio)")
display(with_households.nlargest(6, "AveRooms"))
print("Maiores Population")
display(with_households.nlargest(4, "Population"))
''')

md(r'''
Procuramos essas coordenadas num mapa. Elas apontam para **lugares reais**:

| Linha | O que os dados dizem | Localização (lat, lon) | O que existe lá |
|---|---|---|---|
| 19006 | 7.460 pessoas em 6 domicílios | 38,32, −121,98 | Vacaville: duas prisões estaduais |
| 3364 | 4.198 pessoas em 7 domicílios | 40,41, −120,51 | Susanville: duas prisões estaduais |
| 16669 | 6.532 pessoas em 13 domicílios | 35,32, −120,70 | California Men's Colony (prisão), San Luis Obispo |
| 13034 | 6.675 pessoas em 29 domicílios | 38,69, −121,15 | Folsom State Prison |
| 1914, 1979 | 132 a 142 cômodos por domicílio | ~38,9, −120,1 | Lake Tahoe: casas de veraneio |
| 15360 | 35.682 pessoas, 7,5 por domicílio | 33,35, −117,42 | Camp Pendleton (base dos Fuzileiros Navais) |
| 9880 | 28.566 pessoas | 36,64, −121,79 | Fort Ord (base do Exército em 1990) |

**Cada extremo tem uma causa clara:**

- **`AveOccup` enorme = domicílios coletivos.** O Censo conta quem vive em prisões, alojamentos e quartéis na *população*, mas não como *domicílios*. Por isso "pessoas por domicílio" explode.
- **`AveRooms` enorme = casas de veraneio.** Os cômodos são contados em todas as casas, mas os domicílios só nas ocupadas. Um resort de casas vazias tem muitos cômodos e poucos domicílios.
- **`Population` enorme = block groups grandes** (bases militares, loteamentos novos). São lugares reais, só que grandes.
''')

code(r'''
# Regras simples e explicáveis para cada tipo de outlier encontrado
outlier_types = pd.DataFrame(index=df_raw.index)
outlier_types["domicilios_coletivos"] = df_raw["AveOccup"] > 10
outlier_types["block_group_minusculo"] = households_raw < 10
outlier_types["valor_impossivel"] = df_raw["AveOccup"] < 1
outlier_types["casas_de_veraneio"] = (df_raw["AveRooms"] > 10) & ~outlier_types["block_group_minusculo"]
outlier_types["block_group_muito_grande"] = df_raw["Population"] > 10_000
outlier_types["valor_no_teto"] = ((df_raw["HouseAge"] == df_raw["HouseAge"].max())
                                  | (df_raw["MedHouseVal"] == df_raw["MedHouseVal"].max())
                                  | (df_raw["MedInc"] == df_raw["MedInc"].max()))

pd.DataFrame({
    "linhas": outlier_types.sum(),
    "pct_dos_dados": 100 * outlier_types.mean(),
    "pct_pego_pelo_IQR": [100 * iqr_any[outlier_types[c]].mean() for c in outlier_types],
    "pct_pego_pelo_IF": [100 * if_flag[outlier_types[c]].mean() for c in outlier_types],
})
''')

md(r'''
[[INTERP-OUTLIER-TYPES]]
''')

md(r'''
## 2.7 Conclusões da exploração

[[INTERP-EDA-CONCLUSION]]
''')

# ---------------------------------------------------------------- 3. Pré-processamento
md(r'''
---
# 3. Pré-processamento

Algoritmos de clustering agrupam linhas **próximas** umas das outras, e "próximo" é medido por uma **distância**. Todas as decisões desta seção respondem a uma pergunta: *o que isso faz com as distâncias entre as vizinhanças?*

## 3.1 Valores nulos

A verificação da seção 2.1 encontrou **zero valores nulos** em todas as colunas. Não há nada a imputar, e **não removemos nem preenchemos nenhum valor**.

Se houvesse nulos, nossa política seria: (1) verificar se são aleatórios ou concentrados em algum tipo de vizinhança; (2) nunca preencher com a média em massa, porque isso cria um "pico" artificial que um algoritmo de clustering pode confundir com um grupo; (3) preferir um imputador que usa as outras colunas (KNN ou iterativo) sobre os dados já padronizados.
''')

code(r'''
# Trava de segurança: interrompe a execução se algum dia o dataset vier com nulos
assert df_raw.isna().sum().sum() == 0, "Há valores nulos: revisar a seção 3.1"
print("Verificação concluída: nenhum valor nulo no dataset.")
''')

md(r'''
## 3.2 Tratamento de outliers

Encontramos **tipos diferentes** de outliers, então cada tipo recebe uma decisão própria:

| Tipo | Linhas | Decisão | Justificativa |
|---|---|---|---|
| Domicílios coletivos (`AveOccup` > 10) | ~37 | **Remover** | Prisões, alojamentos e quartéis não são vizinhanças residenciais, que é o que queremos segmentar |
| Block groups minúsculos (< 10 domicílios) | ~51 | **Remover** | Uma média sobre 1 a 9 domicílios é ruído, não um perfil de vizinhança |
| Valores impossíveis (`AveOccup` < 1) | 3 | **Remover** | Menos pessoas que domicílios: erro nos dados |
| Casas de veraneio | ~218 | **Manter**, com log e winsorização | Mercado real e distinto (Lake Tahoe, Palm Springs), relevante para o negócio |
| Block groups grandes e caudas longas | muitas | **Manter**, com log | Assimetria natural de renda, população e tamanho |
| Valores no teto (52 anos, US\$ 500 mil, US\$ 150 mil) | ~2.070 | **Manter** e marcar com flags | São reais: o valor verdadeiro é *pelo menos* o teto |

**Por que não aplicar o capping pelo IQR em todas as colunas** (a abordagem do notebook-template)? Na seção 2.6, a regra do IQR marcou **21% das linhas**, a maioria por pura assimetria natural. O capping achataria a cauda de renda e de preço justamente onde estão os bairros de alto padrão (5% dos preços seriam cortados em US\$ 482 mil), e trataria do mesmo jeito uma prisão e uma vizinhança rica. Preferimos decisões por **tipo** de outlier: remover o que não é residencial, e usar log e uma winsorização leve (0,5%) no restante.

### Remover apenas o que não pertence ao mercado residencial
''')

code(r'''
# Motivo de remoção de cada linha (vazio = a linha fica nos dados)
removal_reason = pd.Series("", index=df_raw.index)
removal_reason[outlier_types["domicilios_coletivos"]] = "domicílios coletivos"
removal_reason[outlier_types["block_group_minusculo"]] = "block group minúsculo"
removal_reason[outlier_types["valor_impossivel"]] = "valor impossível"

to_remove = removal_reason != ""
df_removed = df_raw[to_remove].assign(motivo=removal_reason[to_remove])
df_clean = df_raw[~to_remove].copy()

print(f"Linhas removidas: {to_remove.sum()} ({to_remove.mean():.2%} dos dados)")
print(f"Linhas mantidas:  {len(df_clean):,}")
df_removed["motivo"].value_counts()
''')

md(r'''
Removemos só **0,4%** das linhas, cada uma com um motivo documentado. Elas ficam guardadas em `df_removed`: numa operação real, seriam tratadas como um mercado "institucional" à parte.

### Transformação log e winsorização

- **Log** nas colunas com cauda longa à direita (`MedInc`, `AveRooms`, `AveBedrms`, `Population`, `AveOccup`). O log transforma razões em distâncias iguais: ir de US\$ 20 mil para US\$ 40 mil de renda é o mesmo passo que ir de US\$ 50 mil para US\$ 100 mil. Isso combina com a forma como o mercado percebe diferenças de renda e tamanho.
- **Sem log** em `HouseAge` e `MedHouseVal`: já são limitadas (1 a 52 anos; US\$ 15 mil a US\$ 500 mil) e o log criaria extremos artificiais do lado baixo.
- **Winsorização** (substituir valores além de um percentil pelo próprio percentil) nos extremos que o log não resolve: percentis 0,5% e 99,5%, e 1% e 99% em `AveBedrms`, cuja faixa central é muito estreita. A linha continua nos dados (uma casa de veraneio continua no topo), mas deixa de estar a 12 desvios padrão da média.
''')

code(r'''
# Ferramenta de checagem: o quão longe da média está o valor mais extremo
def max_abs_z(series):
    """Distância, em desvios padrão, da linha mais extrema até a média."""
    return ((series - series.mean()) / series.std()).abs().max()


# Colunas que recebem log e o percentil de winsorização de cada uma (decisões da seção 3.2)
LOG_COLS = ["MedInc", "AveRooms", "AveBedrms", "Population", "AveOccup"]
CLIP_PCT = {"MedInc": 0.5, "AveRooms": 0.5, "AveBedrms": 1.0, "Population": 0.5, "AveOccup": 0.5}
CLIP_LIMITS = {col: tuple(df_clean[col].quantile([pct / 100, 1 - pct / 100])) for col, pct in CLIP_PCT.items()}


def treat_outliers(df):
    """Aplica as decisões da seção 3.2: winsoriza os extremos e aplica log nas colunas assimétricas."""
    out = df.copy()
    for col, (low, high) in CLIP_LIMITS.items():
        out[col] = out[col].clip(low, high)
    out[LOG_COLS] = np.log(out[LOG_COLS])
    return out


# Aplica o tratamento e compara assimetria e extremos antes e depois
df_treated = treat_outliers(df_clean)

before_after = pd.DataFrame({
    "tratamento": ["log + winsorização" if c in LOG_COLS else "nenhum" for c in df_clean.columns],
    "limites (unidades naturais)": [f"{CLIP_LIMITS[c][0]:,.2f} a {CLIP_LIMITS[c][1]:,.2f}" if c in CLIP_LIMITS
                                    else "-" for c in df_clean.columns],
    "skew_antes": df_raw.skew(),
    "skew_depois": df_treated.skew(),
    "max_z_antes": [max_abs_z(df_raw[c]) for c in df_clean.columns],
    "max_z_depois": [max_abs_z(df_treated[c]) for c in df_clean.columns],
}, index=df_clean.columns)
before_after.round(2)
''')

code(r'''
# Padronização simples (z-score), usada só para comparar as colunas na mesma escala
def standardize(df):
    return (df - df.mean()) / df.std()


# Boxplots de todas as colunas em z-score: antes e depois do tratamento
fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
for ax, data, title in [(axes[0], standardize(df_raw), "Antes (dados brutos)"),
                        (axes[1], standardize(df_treated), "Depois do tratamento")]:
    long = data.melt(var_name="coluna", value_name="z")
    sns.boxplot(data=long, x="z", y="coluna", ax=ax, **boxplot_style())
    ax.set_title(title)
    ax.set_xlabel("z-score (desvios padrão a partir da média)")
    ax.set_ylabel("")
action_title(fig, f"Log e winsorização trazem o valor mais extremo de {br(before_after['max_z_antes'].max())} "
                  f"para {br(before_after['max_z_depois'].max(), 1)} desvios padrão")
finish(fig)

# Flags dos valores no teto, guardadas para a caracterização dos segmentos
cap_flags = pd.DataFrame({
    "HouseAge_no_teto": df_clean["HouseAge"] == df_raw["HouseAge"].max(),
    "MedHouseVal_no_teto": df_clean["MedHouseVal"] == df_raw["MedHouseVal"].max(),
    "MedInc_no_teto": df_clean["MedInc"] == df_raw["MedInc"].max(),
})
cap_flags.sum()
''')

md(r'''
[[INTERP-TREATMENT]]
''')

md(r'''
## 3.3 Normalização (scaling)

**O problema:** as colunas usam unidades muito diferentes. Numa distância, a coluna com os maiores números vence.

**Como medimos isso:** na distância euclidiana, o **peso** de cada coluna é a sua variância dividida pela soma das variâncias. O ideal é que nenhuma coluna domine *por acidente*.
''')

code(r'''
def weight_in_distance(df):
    """Participação (%) de cada coluna na distância euclidiana média (ao quadrado) entre linhas."""
    variances = df.var()
    return 100 * variances / variances.sum()


def apply_scaler(scaler, df):
    """Ajusta um scaler e devolve um DataFrame com as mesmas colunas e índice."""
    return pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)


# Peso de cada coluna na distância: sem scaling e com cada um dos três scalers
scalers = {"StandardScaler": StandardScaler(), "MinMaxScaler": MinMaxScaler(), "RobustScaler": RobustScaler()}
weights = pd.DataFrame({"sem scaling (brutos)": weight_in_distance(df_raw),
                        "sem scaling (tratados)": weight_in_distance(df_treated)})
for name, scaler in scalers.items():
    weights[name] = weight_in_distance(apply_scaler(scaler, df_treated))
weights.round(1)
''')

code(r'''
# Gráfico de barras com o peso de cada coluna para cada scaler
fig, ax = plt.subplots(figsize=(10, 5))
cols = df_treated.columns[::-1]
y = np.arange(len(cols))
bar_h = 0.26
for i, (name, color) in enumerate(zip(scalers, [BLUE, ORANGE, AQUA])):
    ax.barh(y + (1 - i) * bar_h, weights[name].reindex(cols), height=bar_h * 0.9, color=color, label=name)
ax.axvline(100 / len(cols), color=GRAY, linewidth=1)
ax.text(100 / len(cols), len(cols) - 0.4, " peso igual (11,1%)", color=INK_2, fontsize=8)
ax.set_yticks(y, cols)
ax.set_title("Peso de cada coluna nas distâncias, depois do tratamento de outliers")
ax.set_xlabel("% da distância média ao quadrado")
ax.legend(loc="lower right")
action_title(fig, "Só o StandardScaler dá o mesmo peso a todas as colunas")
finish(fig)
''')

md(r'''
[[INTERP-SCALING]]
''')
