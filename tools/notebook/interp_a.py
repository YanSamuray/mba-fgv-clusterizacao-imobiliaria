INTERP = {}

INTERP["[[INTERP-DESCRIBE]]"] = r'''
**O que a tabela mostra:**

- **Renda (`MedInc`):** a mediana é US\$ 35 mil por ano, mas a média (US\$ 38,7 mil) é puxada para cima por poucos bairros muito ricos (skew 1,6). O máximo de 15,0 é suspeito: é um teto do Censo (seção 2.6).
- **Valor das casas (`MedHouseVal`):** mediana de US\$ 180 mil, indo de US\$ 15 mil a exatamente US\$ 500 mil, outro teto.
- **Idade das casas (`HouseAge`):** a única variável simétrica (skew 0,06), de 1 a 52 anos. O 52 também é um teto.
- **`AveRooms`, `AveBedrms`, `AveOccup` e `Population`:** valores típicos razoáveis (5,2 cômodos e 2,8 pessoas por domicílio), mas máximos absurdos: 142 cômodos, 34 quartos e **1.243 pessoas por domicílio**. As assimetrias de 21, 31 e 98 indicam caudas extremas, que investigamos na seção 2.6.
'''

INTERP["[[INTERP-HIST]]"] = r'''
- **Renda e valor** têm cauda longa à direita: a maioria dos bairros é de classe média ou baixa, com poucos bairros muito ricos. O valor das casas mostra um **pico artificial em US\$ 500 mil**, que é o teto.
- **`HouseAge`** tem um pico em 52 anos, também artificial.
- **`AveRooms`, `AveBedrms`, `AveOccup` e `Population`** aparecem "espremidos" à esquerda: alguns valores gigantes esticam o eixo e escondem a distribuição real.
- **Latitude e longitude** são bimodais: os dois picos são as regiões de **Los Angeles** (~34°N) e da **Baía de San Francisco** (~38°N). A população se concentra em duas grandes metrópoles.
'''

INTERP["[[INTERP-CORR]]"] = r'''
- **Latitude × longitude (−0,93):** é só o formato diagonal do estado. Não há informação de mercado aqui.
- **`AveRooms` × `AveBedrms` (0,85):** casas com mais cômodos têm mais quartos. As duas dizem quase a mesma coisa, então manter as duas no clustering contaria "tamanho da casa" duas vezes.
- **Renda × valor (0,69):** a relação mais importante para o negócio. Bairros ricos têm casas caras, mas **a correlação está longe de 1**: há bairros com a mesma renda e preços muito diferentes. É justamente essa diferença (localização, tipo de imóvel) que a segmentação precisa capturar.
- As demais correlações são fracas (|r| < 0,35). As variáveis trazem, em geral, informações diferentes entre si.
'''

INTERP["[[INTERP-MAPS]]"] = r'''
Os preços altos formam uma **faixa estreita ao longo do litoral**, concentrada na Baía de San Francisco e no eixo Los Angeles–Orange County–San Diego. Já o **Vale Central** (o "corredor" no meio do estado) e o interior têm preços baixos.

O mapa de renda se parece com o de preços, mas não é igual: há bairros de renda alta no interior (subúrbios de Sacramento, por exemplo) sem os preços do litoral. **A proximidade do oceano parece valer por si só**, além da renda dos moradores. Transformamos essa observação em uma feature na seção 4.
'''

INTERP["[[INTERP-REGION]]"] = r'''
- **Todos os 20.640 block groups receberam um condado e uma região**, nenhum ficou sem classificação.
- **Diferença de preço de 3,5 vezes entre regiões:** a mediana vai de US\$ 254 mil na Baía de San Francisco a US\$ 72 mil no sul do Vale de San Joaquin.
- **Renda e preço não andam juntos:** Orange County tem a maior renda (US\$ 46,4 mil), mas a Baía de San Francisco tem o maior preço. A Central Coast tem o mesmo preço mediano de Orange County (US\$ 231 mil) com uma renda bem menor (US\$ 37,8 mil).
- **O teto de US\$ 500 mil é um fenômeno das metrópoles:** atinge 8,5% dos block groups da Baía, 7,3% de Los Angeles e 6,2% de Orange County, e praticamente zero no interior.
- **Los Angeles County sozinho tem 28% dos block groups** (5.857). Qualquer segmentação será fortemente influenciada pelo mercado de Los Angeles.
'''

INTERP["[[INTERP-VISUAL-SEGMENTS]]"] = r'''
**Já é possível enxergar pelo menos dois mercados diferentes:**

- **Interior:** renda mediana de US\$ 28,6 mil e casas de US\$ 102 mil. A casa custa cerca de **3,6 anos de renda**, e a nuvem de pontos fica achatada embaixo, pois mesmo os bairros de renda alta raramente passam de US\$ 300 mil.
- **Metrópoles e costa:** custam **5,6 a 5,8 anos de renda**. Para a mesma renda, a casa vale bem mais, e muitos bairros encostam no teto de US\$ 500 mil.

Dentro das metrópoles, a nuvem é larga: para uma renda de US\$ 40 mil, há bairros de US\$ 150 mil e de US\$ 450 mil. **Renda e região não bastam para descrever o mercado.** Precisamos de mais dimensões (tipo de moradia, densidade, proximidade do mar), e é isso que o clustering vai combinar.
'''

INTERP["[[INTERP-IQR]]"] = r'''
- **21% das linhas** são marcadas em pelo menos uma coluna. É muito: não podemos simplesmente apagar um quinto do mercado.
- **`AveBedrms` tem a maior taxa (6,9%)** porque a sua faixa central é estreita (1,0 a 1,1 quarto por domicílio). Qualquer desvio pequeno já vira outlier.
- **`Population` (5,8%), `MedHouseVal` (5,2%), `AveOccup` (3,4%) e `MedInc` (3,3%)** são marcadas sobretudo no lado alto, pela cauda longa.
- **`HouseAge`, latitude e longitude não têm outliers.**

Nos boxplots, quase todos os outliers estão de um lado só (à direita). Isso é **assimetria natural**, e não erro. A seguir, separamos o que é cauda natural do que é realmente anômalo.
'''

INTERP["[[INTERP-CEILING]]"] = r'''
Três colunas foram **censuradas no limite máximo** do Censo:

| Coluna | Teto | Linhas no teto | O que significa |
|---|---|---|---|
| `HouseAge` | 52 anos | 1.273 (6,2%) | "52 anos ou mais" |
| `MedHouseVal` | US\$ 500 mil | 965 (4,7%) | "US\$ 500 mil ou mais" |
| `MedInc` | US\$ 150 mil | 49 (0,2%) | "US\$ 150 mil ou mais" |

**Esses valores são reais, mas incompletos:** sabemos que o bairro está *pelo menos* no teto. Numa coluna normal, o máximo aparece em uma ou duas linhas (como a latitude). Para o negócio, os bairros no teto de preço são justamente o **mercado de altíssimo padrão**. Eles não devem ser removidos, mas precisam ser marcados, porque o preço real deles é desconhecido.
'''

INTERP["[[INTERP-LOGIQR]]"] = r'''
- **`MedHouseVal` cai de 1.071 para 26 outliers (−98%)** e **`MedInc` de 681 para 277 (−59%):** quase todos eram só a cauda natural de renda e preço.
- **`Population` e `AveOccup` caem cerca de 30%**, mas continuam com centenas de casos: há extremos de verdade.
- **`AveRooms` e `AveBedrms` não melhoram** (+12% e −3%). Os extremos dessas colunas não são "cauda longa": são valores anômalos, como 142 cômodos por domicílio.

**Conclusão:** a transformação log resolve a maior parte do problema de renda e preço. Os casos que sobram em tamanho e ocupação precisam ser entendidos um a um.
'''

INTERP["[[INTERP-IF]]"] = r'''
- **O IQR marca 4.328 linhas espalhadas por todo o estado.** Isso confirma que ele confunde cauda natural com anomalia.
- **O Isolation Forest marca 207 linhas**, concentradas em **áreas rurais e de montanha** (Sierra Nevada, Lake Tahoe, deserto).
- **O perfil das anomalias é claro:** quase **3 vezes mais cômodos e quartos** por domicílio, **população 3,5 vezes menor** e casas mais novas (17 vs. 29 anos). A renda é igual à das demais.

São block groups pequenos, de **casas de veraneio**, e não bairros "errados".
'''

INTERP["[[INTERP-OUTLIER-TYPES]]"] = r'''
- **Os detectores estatísticos pegam os extremos, mas não sabem o que eles são.**
  - O IQR marca 100% dos domicílios coletivos, mas também marca 21% de todo o mercado.
  - O Isolation Forest é mais seletivo, mas pega só 43% dos domicílios coletivos e só 2% dos valores no teto.
- **As regras de negócio são precisas e explicáveis:** cada linha marcada tem um motivo que um gestor entende.
  - 37 domicílios coletivos;
  - 51 block groups com menos de 10 domicílios;
  - 3 valores impossíveis;
  - 218 áreas de veraneio;
  - 23 block groups muito grandes;
  - 2.070 linhas com algum valor no teto.
- **Por isso, as decisões da seção 3 seguem estas regras**, e não um corte estatístico cego.
'''

INTERP["[[INTERP-EDA-CONCLUSION]]"] = r'''
1. **Qualidade:** não há nulos nem duplicatas. Os problemas reais são **caudas longas**, **valores no teto** e alguns **block groups que não são residenciais** (prisões, quartéis, block groups minúsculos).
2. **Geografia:** o mercado se divide em **litoral caro** e **interior barato**. A distância do oceano parece ser um motor de preço independente da renda.
3. **Renda e preço:** são a relação central (correlação de 0,69), mas, para a mesma renda, o preço varia muito. Ou seja, **o mercado tem mais de uma dimensão**.
4. **Concentração:** Los Angeles e a Baía de San Francisco somam quase metade dos block groups.
5. **Implicações para o clustering:**
   - remover só o que não é mercado residencial;
   - transformar as caudas longas;
   - padronizar as escalas;
   - criar features que capturem localização e tipo de moradia sem usar latitude e longitude diretamente.
'''

INTERP["[[INTERP-TREATMENT]]"] = r'''
- **Assimetria:** caiu de 98 para 0,06 em `AveOccup`, de 21 para 0,16 em `AveRooms` e de 1,6 para −0,1 em `MedInc`.
- **Extremo máximo (|z|):** caiu de 119 desvios padrão para 2,9 em `AveOccup` e de 55 para 4,2 em `AveRooms`. Nenhuma coluna tem mais um ponto capaz de "puxar" sozinho o centro de um cluster.
- **`AveBedrms` continua com skew 2,9**, porque a sua faixa central é estreita demais. Isso reforça a decisão de não usá-la no clustering (seção 4.4).
- **Flags de teto preservadas:** 1.258 block groups com casas de 52 anos ou mais, 959 com valor de US\$ 500 mil ou mais e 45 com renda de US\$ 150 mil ou mais. Elas servem para descrever os segmentos (seção 8).
'''

INTERP["[[INTERP-SCALING]]"] = r'''
- **Sem scaling, a distância é decidida por uma única coluna:** nos dados brutos, `Population` responde por **100%** da distância (os números dela vão até 35 mil). Depois do log, `HouseAge` passa a dominar com **94%**. Nos dois casos, o algoritmo agruparia por uma só característica.
- **StandardScaler:** dá a cada coluna **exatamente o mesmo peso** (11,1%). Cada variável entra na distância por uma decisão de negócio (a seleção de features), e não pela unidade em que foi medida.
- **MinMaxScaler:** depende do mínimo e do máximo e favorece colunas com distribuição "espalhada" até os limites, como `HouseAge` (18%) e `MedHouseVal` (17%).
- **RobustScaler:** divide pelo IQR e explode a coluna de faixa central estreita (`AveBedrms` chega a 29%).

**Decisão:** usamos o **StandardScaler**, aplicado depois do tratamento de outliers. Ele funciona bem porque as colunas já estão simétricas e sem extremos.
'''

INTERP["[[INTERP-COAST-VALIDATION]]"] = r'''
**A feature confere com o rótulo independente** (todos os 20.555 block groups foram encontrados no arquivo do Kaggle):

- `ISLAND`: mediana de 0,6 km;
- `NEAR OCEAN` e `NEAR BAY`: entre 3 e 4 km;
- `<1H OCEAN`: 18 km;
- `INLAND`: 79 km.

As faixas quase não se sobrepõem, então a distância calculada mede de fato a proximidade do mar. Ela ainda é melhor que o rótulo: em vez de 5 categorias, temos uma medida contínua, em km, que distingue a primeira quadra da praia de um bairro a 20 km.
'''

INTERP["[[INTERP-COAST-PRICE]]"] = r'''
- **O preço cai continuamente com a distância do mar:**
  - litoral (até 5 km): US\$ 256 mil;
  - costeira (5 a 25 km): US\$ 205 mil;
  - intermediária (25 a 80 km): US\$ 163 mil;
  - interior (mais de 80 km): US\$ 87 mil.

  Correlação de −0,50, a segunda mais forte com o preço depois da renda.
- **A renda cai bem menos:** US\$ 37 mil, US\$ 39 mil e US\$ 36 mil nas três primeiras faixas. Ou seja, **o litoral é mais caro sem que os moradores sejam proporcionalmente mais ricos**: paga-se pela localização.

Para o negócio, `dist_coast_km` captura o principal atributo de localização da Califórnia, e faz isso sem latitude e longitude: um bairro a 3 km do mar em San Diego e outro em San Francisco ficam "próximos" nessa dimensão.
'''

INTERP["[[INTERP-NEW-FEATURES]]"] = r'''
- **Densidade do entorno:** a mediana é de 1.862 pessoas/km², mas vai de menos de 1 (áreas rurais) a quase 13 mil (centros de Los Angeles e San Francisco). No mapa, as manchas escuras desenham exatamente as regiões metropolitanas.
- **Anos de renda por casa:** na mediana, uma casa custa **5 anos** de renda do bairro. Valores acima de 10 indicam bairros caros para quem mora neles: mercado de investidores ou de compradores de fora.
- **Renda per capita:** mediana de US\$ 13 mil por pessoa. É uma medida melhor do poder de compra que a renda do domicílio, porque considera o tamanho da família.
- **Índice de luxo:** a faixa litorânea de alto padrão aparece claramente no mapa, com algumas manchas altas também no interior, como nos subúrbios de Sacramento.
'''

INTERP["[[INTERP-NEW-TREATMENT]]"] = r'''
- **Todas as novas features ficaram quase simétricas** (|skew| ≤ 0,66) **e sem extremos** (|z| máximo ≤ 4,1).
- **Os casos mais graves foram resolvidos:**
  - `rooms_per_person` caiu de skew 17,5 para −0,45 (casas de veraneio);
  - `price_to_income` caiu de 5,3 para 0,4 (bairros com renda muito baixa e preço alto).
- **Mesma lógica das colunas originais.** As novas features passam pelo mesmo tratamento, então nenhuma delas vai dominar a distância só por ter números grandes.
'''

INTERP["[[INTERP-SPEARMAN]]"] = r'''
**Três grupos de colunas redundantes** (|correlação| ≥ 0,8):

| Grupo | Correlação | Quem fica e por quê |
|---|---|---|
| `Population` e `households` | 0,91 | os dois medem o tamanho do block group; nenhum entra (ver VIF e decisão abaixo) |
| `AveRooms` e `bedroom_share` | 0,89 | `AveRooms` fica: "tamanho da moradia" é mais fácil de explicar |
| `MedInc`, `income_per_person` e `luxury_index` | 0,86 a 0,94 | `MedInc` fica: é o dado original; os outros dois são derivados dele |

Removemos `households`, `bedroom_share` e `luxury_index` desta etapa. A matriz também mostra que `dist_big_city_km` e `pop_density_3km` andam juntas (−0,7): perto das grandes cidades, o entorno é denso. O dendrograma também mostra que **`MedHouseVal` fica perto do grupo da renda, mas não dentro dele**: o preço traz informação própria (a localização), o que confirma a análise da seção 2.
'''

INTERP["[[INTERP-VIF]]"] = r'''
- **`income_per_person` (540) e `rooms_per_person` (288) têm VIF enorme.** Com o log, eles são exatamente `log(MedInc) − log(AveOccup)` e `log(AveRooms) − log(AveOccup)`: não trazem nada que as colunas originais já não tenham.
- **Esses dois puxam os VIFs de `MedInc`, `AveOccup` e `AveRooms` para cima.** Ao removê-los, os VIFs das três voltam a valores baixos (ver a próxima célula).
- **`price_to_income` (7,4) e `MedHouseVal` (10,6) se explicam mutuamente:** a razão entre preço e renda é quase reconstruída pelas duas colunas originais.
- **Todas as demais têm VIF abaixo de 3:** informação própria.
'''

INTERP["[[INTERP-SELECTION]]"] = r'''
**As 7 features finais**, com VIF máximo de 2,9 (nenhuma redundância relevante), cobrem quatro dimensões de negócio:

| Dimensão | Features |
|---|---|
| **Poder aquisitivo e preço** | `MedInc` (renda) e `MedHouseVal` (valor das casas) |
| **Tipo de moradia** | `AveRooms` (tamanho) e `HouseAge` (idade do estoque) |
| **Perfil do domicílio** | `AveOccup` (pessoas por domicílio: famílias vs. solteiros e casais) |
| **Localização (sem coordenadas)** | `dist_coast_km` (proximidade do mar) e `pop_density_3km` (urbano vs. rural) |

As features que ficaram de fora **não são descartadas**. `income_per_person`, `price_to_income`, `luxury_index`, `dist_big_city_km` e `income_vs_neighbors` voltam na seção 8 para **descrever** os segmentos, sem influenciar a formação deles.
'''

INTERP["[[INTERP-PCA]]"] = r'''
**As quatro dimensões do mercado** (as quatro primeiras somam 86% da variação):

| Componente | Variação | O que mede (maiores loadings) | Leitura de negócio |
|---|---|---|---|
| **PC1** | 31% | renda (+0,60), valor (+0,53) e cômodos (+0,48) | **Riqueza e padrão**: bairros ricos, caros e com casas grandes |
| **PC2** | 30% | densidade (+0,54), idade (+0,46) e valor (+0,32) vs. distância da costa (−0,52) e cômodos (−0,33) | **Urbano consolidado vs. periferia**: centros antigos, densos e perto do mar vs. áreas novas e espaçosas no interior |
| **PC3** | 15% | pessoas por domicílio (+0,88) | **Tamanho da família** |
| **PC4** | 10% | idade das casas (+0,82) | **Idade do estoque** |

**Decisão:** os dois primeiros componentes explicam só 61% da variação, e são precisos 4 dos 7 para chegar a 86%. **O mercado tem várias dimensões independentes**: não dá para resumi-lo a um eixo "rico vs. pobre".

Por isso, **clusterizamos sobre as 7 features padronizadas**, e não sobre os componentes. Assim, cada segmento continua descrito em variáveis que um gestor entende. O PCA serve para **visualizar** os clusters (seção 7.5).
'''

INTERP["[[INTERP-PCA-DENSITY]]"] = r'''
A nuvem é **uma única massa contínua**, mais densa no centro, sem "ilhas" separadas por espaços vazios. Isso já antecipa uma característica importante: **o mercado imobiliário é um contínuo.** Os bairros vão mudando gradualmente de perfil, sem fronteiras naturais nítidas.

Para o clustering, isso significa que os segmentos serão **partições úteis de um contínuo**, e não grupos isolados. Por isso:

- esperamos valores **moderados** de silhouette;
- algoritmos de densidade, como o DBSCAN, devem ter dificuldade;
- a qualidade da segmentação deve ser julgada também pela **estabilidade** e pela **utilidade para o negócio**.
'''
