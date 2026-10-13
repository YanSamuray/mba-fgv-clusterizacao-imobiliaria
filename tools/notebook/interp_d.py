INTERP = {}

INTERP["[[ENSEMBLE-TEXT]]"] = r'''
**A segmentação do K-Means é confirmada pela maioria dos algoritmos em 93,5% dos block groups:**

- **51,4% formam o núcleo estável:** os três algoritmos concordam.
- **42,1% são confirmados pela maioria:** quase sempre é o GMM que discorda, sozinho. Isso é coerente com a sua silhouette baixa (seção 6.6). O Ward concorda com o K-Means em 78% a 99% dos block groups de cada segmento.
- **Só 6,5% são contestados**, com GMM e Ward discordando do K-Means. Estes são os **bairros de transição**.

**Por segmento:**

- **S6, S1 e S2 são os mais sólidos:** de 1% a 2% contestados, e núcleos estáveis de 77%, 69% e 59%.
- **S4, S5 e S3 têm as fronteiras mais difusas:** cerca de 10% a 12% contestados.
- **S4 tem só 10% de núcleo estável:** o GMM o divide de outra forma (concorda em apenas 14%), mas o Ward concorda em 84%. **S4 é amplo e merece sub-segmentação**, assim como S3.

**Uso prático:** os bairros contestados são os primeiros a **migrar de segmento** quando o bairro muda, por exemplo com uma valorização ou com a chegada de novas famílias. Eles devem receber comunicação mista e monitoramento a cada atualização dos dados. A coluna `concordancia_algoritmos` do arquivo exportado identifica cada um deles.
'''

INTERP["[[PRIORITY-TEXT]]"] = r'''
**Ranking de atratividade:**

1. **S4 · Subúrbios familiares em expansão (0,85):** lidera três dos quatro critérios. É o maior mercado em clientes e em valor, e o que mais cresce (23% de casas novas). É a **prioridade número 1 de investimento**.
2. **S3 · Urbano compacto costeiro (0,62):** a maior oportunidade de preço (16% subvalorizados), com valor de estoque relevante. É a **prioridade para investidores e captação**.
3. **S1 · Interior acessível (0,41):** grande em clientes, com boa oportunidade de preço (cerca de 12%), mas o menor valor de estoque. É um **mercado de volume**.
4. **S5 · Classe média urbana consolidada (0,35):** valor alto, mas sem crescimento (0% de casas novas). É um mercado de **revenda**.
5. **S6 · Alto padrão costeiro (0,22):** pequeno em clientes e sem subvalorização visível, mas com **o segundo maior valor de estoque**. A prioridade é **margem**, e não expansão.
6. **S2 · Famílias urbanas populares (0,19):** baixo crescimento e baixo valor. É um mercado de **acesso à moradia**, que pede um modelo de negócio próprio (aluguel e financiamento).

No gráfico, o quadrante superior direito (crescimento e oportunidade acima da mediana) reúne **S3, S1 e S4**. S4 está no limite da oportunidade de preço, mas isolado à direita: é a maior fronteira de crescimento. **S2, S5 e S6** ficam no quadrante inferior esquerdo, onde a estratégia é de manutenção e margem, e não de expansão.
'''

INTERP["[[ALLOCATION-TEXT]]"] = r'''
**Proposta para um orçamento anual de US\$ 10 milhões e 100 corretores:**

| Segmento | Orçamento | Corretores | Onde posicionar as equipes |
|---|---|---|---|
| S4 · Subúrbios familiares em expansão | US\$ 3,2 milhões (32%) | 32 | Santa Clarita, Poway, Simi Valley, Santa Rosa |
| S3 · Urbano compacto costeiro | US\$ 1,9 milhão (19%) | 19 | San Diego, Santa Monica, Culver City, Burbank |
| S1 · Interior acessível | US\$ 1,7 milhão (17%) | 17 | Bakersfield, Fresno, Redding, Chico |
| S5 · Classe média urbana consolidada | US\$ 1,4 milhão (14%) | 14 | San Francisco, Daly City, Culver City, Burbank |
| S2 · Famílias urbanas populares | US\$ 1,0 milhão (10%) | 10 | Los Angeles, Huntington Park, Inglewood |
| S6 · Alto padrão costeiro | US\$ 0,7 milhão (7%) | 8 | Santa Monica, San Rafael, Redondo Beach, Culver City |

- **S4 recebe 32% do orçamento com 24% dos domicílios:** é o segmento mais atrativo e recebe um reforço proporcional.
- **S6 recebe 7% com 10% dos domicílios**, porque o marketing de alto padrão é de **relacionamento** (indicações, eventos, corretores especializados) e custa menos por cliente que o marketing de massa. A receita, porém, é alta: cada um dos 8 corretores de S6 trabalha com imóveis de cerca de US\$ 450 mil ou mais.
- **A regra é transparente e ajustável.** Se a diretoria quiser privilegiar a margem em vez do crescimento, basta mudar os pesos do índice, e o código recalcula toda a alocação.
'''

INTERP["[[STRATEGIES-TEXT]]"] = r'''
Cada estratégia parte do perfil do segmento (seção 8) e termina num **KPI mensurável**, para que a empresa saiba se funcionou.

| | Posicionamento | Produto e serviço | Precificação | Canais de marketing | KPI principal |
|---|---|---|---|---|---|
| **S1 · Interior acessível** | "a casa própria ao seu alcance" | primeira casa, financiamento facilitado, parcerias com bancos regionais | preço é decisivo: destacar parcela mensal e custo total | rádio e mídia local, portais com filtro de preço, parcerias com empregadores regionais | nº de contratos de 1ª casa; taxa de aprovação de financiamento |
| **S2 · Famílias urbanas populares** | "mais espaço para a sua família" | aluguel, locação com opção de compra, programas de habitação, imóveis com mais quartos | aluguel e parcelas acessíveis; transparência total de custos | comunicação em espanhol e inglês, lideranças comunitárias, redes sociais, WhatsApp | nº de contratos de locação; inadimplência abaixo da meta |
| **S3 · Urbano compacto costeiro** | "viva perto do mar" (moradores) e "renda garantida" (investidores) | **S3.1:** primeiro imóvel compacto; **S3.2:** gestão de aluguel e carteira para investidores | usar o valor esperado (seção 9.2) para captar imóveis subvalorizados | digital (portais, redes sociais), conteúdo para investidores | nº de imóveis subvalorizados captados; rentabilidade de aluguel dos investidores |
| **S4 · Subúrbios familiares em expansão** | "a casa da sua família, num bairro que cresce" | lançamentos, casas novas, parcerias com incorporadoras, troca de imóvel (vender o apartamento e comprar a casa) | preço de lançamento com valorização esperada; pacotes de troca | eventos de lançamento, Google e redes sociais com segmentação por família, escolas | participação nas vendas de lançamentos; tempo médio de venda |
| **S5 · Classe média urbana consolidada** | "o bairro de que você gosta, renovado" | revenda, avaliação de imóvel, reformas e reformas para venda | precificação por comparação com vendas vizinhas; destacar o potencial pós-reforma | marketing de bairro (mala direta, placas, corretor local), indicações | nº de captações de revenda; desconto médio sobre o preço pedido |
| **S6 · Alto padrão costeiro** | "exclusividade à beira-mar" | atendimento personalizado, imóveis fora do mercado aberto (*off-market*), relocação, gestão patrimonial | preço premium; avaliação individual (o teto do Censo esconde o valor real) | indicações, eventos privados, revistas e mídia de luxo, *concierge* | comissão média por transação; satisfação (NPS) dos clientes |

**Investimento:**

- **S4 (crescimento):** comprar terrenos e fazer parcerias com incorporadoras nas cidades com mais lançamentos.
- **S3 (subvalorização):** captar os cerca de 1.700 block groups subvalorizados do arquivo exportado. Os cerca de 280 mil domicílios de S3 em áreas subvalorizadas são o primeiro alvo.
- **S6 (proteção de valor):** manter presença qualificada, sem expansão agressiva.
'''

INTERP["[[CONCLUSION-TEXT]]"] = r'''
### 1. Qualidade dos clusters

A segmentação final tem **6 segmentos obtidos com o K-Means** sobre 7 features padronizadas, e a qualidade foi avaliada por quatro lentes:

- **Métricas internas:** silhouette de 0,185, contra −0,01 com rótulos aleatórios; inércia 52% menor que a do acaso; Davies-Bouldin de 1,53.
- **Estabilidade:** ARI de 0,94 em 30 reamostragens bootstrap, e Jaccard acima de 0,93 em todos os segmentos.
- **Concordância entre métodos:** o Ward encontra praticamente os mesmos segmentos (ARI de 0,75), e a maioria dos algoritmos confirma o segmento de 93,5% dos block groups.
- **Coerência geográfica:** sem usar latitude e longitude, os segmentos formam padrões claros no mapa e aparecem em várias metrópoles.

A silhouette moderada **não é um defeito da segmentação**, mas uma característica do mercado, e a teoria explica por quê:

- **Silhouette num contínuo:** a silhouette compara a distância média de um ponto ao próprio cluster (*a*) com a distância ao cluster vizinho (*b*). Num mercado contínuo, os bairros da borda ficam quase à mesma distância dos dois segmentos (*a* ≈ *b*), o que puxa a média para baixo, por melhor que seja a partição.
- **O DBSCAN confirmou a falta de vazios:** ele procura regiões densas separadas por regiões vazias e encontrou um único grupo. O PCA também mostrou uma única nuvem.
- **O K-Means era o algoritmo adequado:** ele minimiza a variância dentro dos grupos e supõe grupos compactos de tamanhos parecidos. Por isso preparamos os dados para isso (log, winsorização e padronização), e os segmentos ficaram equilibrados (11% a 20% dos block groups).
- **Estabilidade:** pelo critério de Hennig (Jaccard acima de 0,75), todos os segmentos são estáveis.

**Os clusters fazem sentido e são acionáveis:**

- cada segmento tem pelo menos 10% dos domicílios;
- cada um tem um nome de negócio, uma localização (cidades de referência) e uma estratégia própria com KPI;
- um bairro novo pode ser classificado automaticamente.

Os 6,5% de bairros contestados ficam identificados para tratamento à parte.

### 2. Principais insights de negócio

1. **Preço não define o cliente.** S3, S4 e S5 têm o mesmo preço mediano (cerca de US\$ 210 mil), mas são mercados opostos: apartamentos compactos perto do mar, casas novas de famílias no subúrbio e casas antigas da classe média. A segmentação atual por faixa de preço mistura esses três clientes.
2. **A proximidade do mar vale por si só.** O preço cai de US\$ 256 mil (até 5 km) para US\$ 87 mil (mais de 80 km), enquanto a renda dos moradores quase não muda.
3. **O crescimento está nos subúrbios.** S4 tem 23% de casas novas e é o maior mercado do estado em domicílios (24%) e em valor (25%).
4. **O alto padrão é pequeno em clientes e enorme em valor.** S6 tem 10% dos domicílios e 21% do valor do estoque.
5. **Há oportunidades de preço concentradas.** 16% dos block groups de S3 e 12% dos de S1 valem 20% ou mais abaixo do que os seus fundamentos indicam.
6. **Os segmentos são tipos de bairro, e não cidades.** Toda metrópole tem uma mistura de segmentos, então a estratégia deve ser por segmento, aplicada em várias cidades.

### 3. Limitações

- **Dados de 1990:** os perfis e os valores absolutos mudaram muito desde então. A *metodologia* continua válida, mas os números precisam ser atualizados.
- **Unidade de análise:** cada linha é um block group (a mediana de uma vizinhança), e não um cliente ou um imóvel. Dentro de um bairro há diversidade que não vemos.
- **Valores no teto:** 38% de S6 está no teto de US\$ 500 mil. O preço real e a subvalorização desse segmento são desconhecidos.
- **Sem série histórica:** o "crescimento" é aproximado pela idade das casas, e não por uma variação de preços ou de população.
- **Escolhas de modelagem:** a seleção das features, o número de segmentos e o índice de atratividade envolvem julgamento de negócio, documentado em cada etapa. Outras escolhas razoáveis levariam a segmentos parecidos, mas não idênticos.
- **Modelo de valor esperado:** é correlacional (R² de 0,87). "Subvalorizado" significa "barato para os fundamentos medidos", e pode haver fatores não medidos (como escolas e segurança).

### 4. Próximos passos

1. **Atualizar os dados** com a American Community Survey mais recente e aplicar a mesma pipeline (a função `assign_segment` já está pronta).
2. **Incorporar dados internos:** preços de transação, tempo de venda, perfil dos clientes do CRM e qualidade das escolas.
3. **Sub-segmentar S4 e S3**, os segmentos com fronteiras mais difusas, para campanhas locais.
4. **Monitorar a migração entre segmentos** a cada atualização, começando pelos 6,5% contestados.
5. **Testar as estratégias:** campanhas A/B por segmento, medindo os KPIs propostos.

### 5. Aplicabilidade prática

A segmentação está **pronta para uso**:

- **O arquivo** `data/segmentos_california.csv` traz o segmento, o nome, o nível de concordância entre algoritmos e a marcação de subvalorização de cada block group, para cruzar com a base de imóveis e clientes.
- **A função** `assign_segment()` classifica qualquer bairro novo com o mesmo tratamento e o mesmo modelo. Ela reproduz 100% dos segmentos num teste com 500 block groups.
- **O orçamento e as equipes** podem ser recalculados em segundos se a diretoria mudar os pesos.

### Os resultados atendem às expectativas do negócio?

As três metas da introdução foram avaliadas assim:

| Meta | O que os resultados permitem afirmar |
|---|---|
| **Conversão de 12% para 25 a 30%** | Não pode ser medida com dados do Censo: depende de dados de vendas. A segmentação entrega o que essa meta exige: mensagem, canal e produto específicos para seis públicos que hoje recebem a mesma abordagem (por exemplo, S3, S4 e S5, que têm o mesmo preço e perfis opostos). **Validação recomendada:** um piloto com campanhas A/B por segmento, medindo a conversão antes e depois |
| **Tempo de venda 40% menor** | Também depende de dados internos. Os resultados atacam duas causas de demora: imóveis com preço acima dos fundamentos (o modelo de valor esperado identifica os sobrevalorizados) e corretores no lugar errado (a alocação por segmento e cidade) |
| **US\$ 50 a 100 milhões em nichos subexplorados** | **Atendida em ordem de grandeza.** A análise encontrou cerca de 1.700 block groups subvalorizados, com perto de 800 mil domicílios, concentrados em S3 e S1. Captar só 500 imóveis ao preço mediano de S3 (cerca de US\$ 200 mil, em valores de 1990) já representaria cerca de US\$ 100 milhões |

**Conclusão sobre as expectativas:** o modelo cumpre o que um modelo não supervisionado pode cumprir. Ele encontrou segmentos estáveis, interpretáveis e com tamanho e oportunidade quantificados. As metas de conversão e de tempo de venda passam a ter um plano de teste concreto, com os KPIs da seção 9.5.

### 6. Recomendações finais

1. **Substituir a segmentação por cidade e faixa de preço pelos 6 segmentos**, mantendo os 3 macro-segmentos para a comunicação institucional.
2. **Priorizar S4 · Subúrbios familiares em expansão:** cerca de um terço do orçamento e das equipes, com foco em lançamentos e na troca de imóvel.
3. **Criar uma frente de investimento em S3**, usando o modelo de valor esperado para captar imóveis subvalorizados e oferecer gestão de aluguel.
4. **Tratar S6 como uma operação de luxo**: equipe pequena e especializada, foco em margem e relacionamento.
5. **Adaptar o modelo de negócio a S1 e S2:** volume e acessibilidade (financiamento, locação e programas de habitação).
6. **Medir e revisar:** acompanhar os KPIs de cada segmento e reexecutar a segmentação a cada nova base de dados.

### 7. O que aprendemos na disciplina e como isso impacta o nosso trabalho

- **Em aprendizado não supervisionado, as decisões de preparação são o próprio modelo.** Não há um "gabarito" que corrija escolhas ruins. Quais features entram, como os outliers são tratados e qual scaler é usado definem o que significa "parecido". Vimos isso na prática: sem scaling, uma única coluna decidia 94% a 100% da distância.
- **Nenhuma métrica sozinha escolhe o número de clusters.** Cotovelo, silhouette, Davies-Bouldin e estabilidade apontaram valores diferentes. A decisão boa combina as métricas com a utilidade para o negócio, e a estabilidade por bootstrap foi decisiva para descartar o k = 5.
- **Cada algoritmo tem uma ideia diferente do que é um grupo.** Testar K-Means, DBSCAN, Ward e GMM revelou uma característica do próprio mercado (ele é contínuo) que um único algoritmo não teria mostrado.
- **O valor está na tradução para o negócio.** Os segmentos só se tornaram úteis quando viraram nomes, perfis em dólares e quilômetros, mapas, orçamento e KPIs.
- **Impacto no nosso trabalho:** levaremos para as nossas áreas o hábito de documentar cada decisão de dados, de validar a estabilidade antes de recomendar uma ação e de transformar a análise em uma ferramenta reutilizável (o arquivo e a função de classificação), e não em um relatório único.
'''
