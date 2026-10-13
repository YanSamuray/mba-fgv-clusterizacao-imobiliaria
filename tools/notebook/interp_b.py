INTERP = {}

INTERP["[[INTERP-K-CHOICE]]"] = r'''
**Escolhemos k = 6 segmentos.** Nenhum critério sozinho decide; o k vem da leitura conjunta dos quatro painéis e da utilidade para o negócio:

| Critério | O que mostra | Leitura |
|---|---|---|
| **Cotovelo (inércia)** | a curva dobra entre k = 4 e k = 6; o ponto de dobra calculado é k = 5 | a partir de 6, cada novo cluster reduz pouco a inércia |
| **Silhouette** | máxima em k = 3 (0,21), e cai devagar até k = 6 (0,18); depois cai mais rápido | k = 3 a 6 têm qualidade parecida; acima de 6, piora |
| **Davies-Bouldin** | praticamente plano entre k = 3 e k = 6 (1,50 a 1,53) | não diferencia esses valores |
| **Estabilidade (ARI)** | alta em k = 3, 4 e **6** (≥ 0,92); **k = 5 é instável** (o pior caso cai para 0,57) e de k = 7 em diante a estabilidade cai | k = 6 é o **maior número de segmentos que continua estável** |

**Por que não k = 3 ou 4**, que têm a melhor silhouette? Porque são grandes demais para orientar ações: o menor segmento teria 31% (k = 3) ou 23% (k = 4) do mercado. Com 6, o negócio separa perfis que exigem estratégias diferentes (por exemplo, o alto padrão e os apartamentos compactos), sem perder qualidade nem estabilidade. O menor segmento tem 11% do mercado, ou seja, nenhum é pequeno demais para ter uma equipe própria.

**Por que não k = 5**, que é o cotovelo calculado? Porque é instável: em algumas reamostragens os segmentos mudam bastante. Uma estratégia não pode depender de uma segmentação que muda com a amostra.
'''

INTERP["[[INTERP-DBSCAN]]"] = r'''
**O DBSCAN não encontra segmentos neste mercado:**

- **No eps do joelho (1,19):** um único grupo com **97,5%** dos block groups, mais 2,5% de ruído.
- **Com eps maior:** o grupo único só aumenta.
- **Com eps 25% menor (0,89):** 10,5% viram ruído e o "segundo grupo" tem só 41 block groups (0,2%).

Isso confirma o que a densidade no plano do PCA já mostrava: **não há regiões densas separadas por vazios**. O mercado é um contínuo, e o DBSCAN foi feito para outro tipo de estrutura. Ele serve aqui como **diagnóstico** (confirma o contínuo e aponta os atípicos), e não como segmentação.
'''

INTERP["[[INTERP-DBSCAN-NOISE]]"] = r'''
**Quem são os 2,5% de "ruído"?** São block groups com uma **combinação rara** de características:

- renda baixa (US\$ 21,6 mil vs. US\$ 35,6 mil nos demais);
- moradias pequenas (3,7 vs. 5,2 cômodos);
- casas caras (US\$ 231 mil vs. US\$ 179 mil);
- perto do mar (7,6 vs. 19 km).

É o perfil de bairros de aluguel, de estudantes ou de aposentados no litoral, onde quem mora não é quem poderia comprar. Esses bairros continuam na segmentação final: o K-Means vai colocá-los no segmento mais próximo.
'''

INTERP["[[INTERP-GMM]]"] = r'''
- **Ward:** sobre a amostra de 5.000, a silhouette cai de 0,175 (3 grupos) para cerca de 0,12 (5 a 7 grupos). Com 6 grupos, os tamanhos ficam equilibrados (10% a 23%).
- **GMM: o BIC e o AIC diminuem continuamente até 12 componentes**, sem um mínimo claro. Com 20 mil linhas, cada componente a mais sempre melhora um pouco o ajuste. O GMM descreve o *formato* da nuvem contínua com cada vez mais elipses, em vez de revelar grupos naturais. Por isso, usamos o mesmo k = 6 para a comparação.
- **Pertencimento incerto:** com 6 componentes, **11,2% dos block groups** têm probabilidade máxima abaixo de 0,6. São os bairros "em transição" entre dois segmentos, uma informação que só o GMM entrega.
'''

INTERP["[[INTERP-COMPARISON]]"] = r'''
**Escolhemos o K-Means**, que vence ou empata em todos os critérios técnicos e de negócio:

- **Qualidade:** tem a melhor silhouette (0,184), o melhor Davies-Bouldin (1,53) e o melhor Calinski-Harabasz (4.479).
- **Ward chega muito perto** (0,182 de silhouette) e concorda bastante com o K-Means (**ARI de 0,75**): dois métodos diferentes encontram essencialmente os mesmos segmentos, o que reforça a confiança no resultado.
- **GMM fica bem atrás** (silhouette 0,09, ARI de 0,33): as elipses flexíveis se sobrepõem num mercado contínuo, e os grupos ficam menos nítidos.
- **DBSCAN não segmenta** (um único grupo); por isso as métricas aparecem vazias (NaN). Com eps menor, a silhouette de 0,15 é enganosa, porque vem de um grupo com 89% dos dados e outro com 0,2%.
- **Negócio:** o K-Means dá um **centróide** (perfil médio) por segmento, fácil de virar persona. Também classifica novos bairros instantaneamente (seção 9.7) e é estável (seção 7.3).

**GMM e Ward não são descartados:** eles voltam no ensemble (seção 8.5) para identificar os bairros de transição.
'''

INTERP["[[INTERP-METRICS]]"] = r'''
**Como ler as métricas:**

- **Silhouette de 0,185:** costuma ser classificada como "estrutura fraca". Mas, como vimos, o mercado é um contínuo sem fronteiras naturais, e nesse cenário nenhuma segmentação teria silhouette alta. O que importa é que ela é **muito melhor que o acaso**: com rótulos sorteados, a silhouette é −0,01.
- **Inércia 52% menor que a de rótulos aleatórios:** os segmentos explicam metade da variação do mercado.
- **Davies-Bouldin de 1,53 vs. 122** e **Calinski-Harabasz de 4.479 vs. 1:** os segmentos são muito mais compactos e separados do que uma divisão arbitrária.

**Conclusão:** os segmentos não são "ilhas", mas **regiões bem definidas de um contínuo**. É o tipo de segmentação que se espera em mercados reais, e é útil, desde que se reconheçam as zonas de transição (seção 8.5).
'''

INTERP["[[INTERP-SEPARATION]]"] = r'''
- **Quatro segmentos bem encaixados:** S1, S4 e S5 têm silhouette média de 0,19 a 0,22 e quase nenhum block group mal classificado (0% a 1,6% com silhouette negativa). S2 também (7%).
- **S6 (alto padrão)** tem 11% de silhouette negativa, mas é o segmento **mais distante dos demais**: está a 4,3 e 4,4 unidades de S1 e S2. Os seus vizinhos mais próximos são S5 (2,5) e S4 (2,6), e é na fronteira com eles que ficam os casos ambíguos: bairros bons, mas não de luxo.
- **S3 é o menos nítido:** silhouette de 0,10 e 22% de casos negativos. O seu vizinho mais próximo é S5 (distância de 2,0, a menor entre todos os pares), e a razão separação/coesão é de só 1,04. Por isso, S3 é o candidato natural à **clusterização recursiva** (seção 8.5).
- **Pares mais próximos:** S3–S5 (2,0), S2–S5 (2,3) e S1–S4 (2,4). Faz sentido: são, respectivamente, bairros urbanos com e sem famílias, bairros urbanos populares e de classe média, e interior e subúrbio.
'''

INTERP["[[INTERP-STABILITY]]"] = r'''
**A segmentação é muito estável:**

- O ARI médio entre a segmentação final e 30 reamostragens é de **0,94**, e o pior caso é 0,89.
- **Todos os seis segmentos** têm Jaccard médio acima de 0,93, bem acima do limite de 0,75 para um cluster "estável".
- Mesmo S3, o menos nítido, tem Jaccard mínimo de 0,84.

Para o negócio, isso significa que **os segmentos não são um acaso da amostra**: com outros dados do mesmo mercado, encontraríamos os mesmos grupos. A empresa pode construir estratégias de longo prazo sobre eles.
'''

INTERP["[[INTERP-GEO]]"] = r'''
**Os segmentos fazem sentido no mapa, sem que a localização tenha sido usada diretamente.** Latitude e longitude ficaram fora do clustering, mas os segmentos formam padrões geográficos claros:

- **S1** domina o interior: 86% do sul do Vale de San Joaquin, 66% da Superior California e 58% do norte do Vale.
- **S6** (alto padrão) forma a faixa litorânea da Baía de San Francisco, do oeste de Los Angeles e de Orange County.
- **S2** concentra-se no centro e no sul de Los Angeles: 64% dos seus block groups estão em Los Angeles County.

**Os segmentos são tipos de bairro, e não regiões:**

- **S6 aparece em todas as metrópoles:** 859 block groups na Baía, 808 em Los Angeles, 282 em Orange County, 179 na Central Coast e 129 em San Diego.
- **Toda metrópole tem uma mistura de segmentos:** Los Angeles tem 36% de S2, 30% de S5, 14% de S6 e 12% de S3. Na Baía, predominam S5 (36%), S6 (22%) e S4 (18%).

É exatamente o que pedia o objetivo: **um "bairro rico no litoral" é reconhecido como tal, perto de Los Angeles ou de San Francisco.** Para a imobiliária, isso permite uma estratégia por segmento aplicada em várias cidades, em vez de uma estratégia por cidade.
'''

INTERP["[[INTERP-PCA-CLUSTERS]]"] = r'''
**Leitura do biplot:**

- **S6** fica no extremo direito do PC1, na direção das setas de renda e valor: é o eixo da riqueza.
- **S1** fica embaixo, na direção da seta de distância da costa: interior.
- **S4** fica embaixo e à direita, na direção da seta de cômodos: casas grandes, longe dos centros.
- **S2** fica à esquerda e acima: baixa renda, denso, na direção oposta à das setas de riqueza.
- **S3 e S5 se sobrepõem no plano PC1 × PC2.** Eles se separam na **terceira dimensão** (PC3, pessoas por domicílio) e na idade das casas: S3 tem domicílios pequenos (2,1 pessoas) e casas mais novas; S5 tem famílias (2,7 pessoas) e as casas mais antigas. No gráfico 3D, S3 (verde-água) aparece abaixo de S5 (rosa) no eixo PC3.

As bordas entre as nuvens se tocam: são os **bairros de transição**, coerentes com o mercado contínuo. Mesmo assim, cada segmento ocupa uma região própria, e a posição dos centróides resume bem o perfil de cada um.
'''
