INTERP = {}

INTERP["[[INTERP-PROFILE]]"] = r'''
**O achado mais importante:** **S3, S4 e S5 têm praticamente o mesmo preço mediano (US\$ 206 mil a US\$ 216 mil), mas são mercados completamente diferentes:**

| | S3 | S4 | S5 |
|---|---|---|---|
| Renda mediana | US\$ 30 mil | **US\$ 50 mil** | US\$ 39 mil |
| Pessoas por domicílio | **2,1** | 3,0 | 2,7 |
| Cômodos por domicílio | 4,1 | **6,3** | 5,2 |
| Idade das casas | 23 anos | **16 anos** | **38 anos** |
| Distância da costa | **7 km** | 25 km | 11 km |
| Anos de renda por casa | **7,0** | 4,2 | 5,3 |

Uma segmentação por **faixa de preço**, como a que a empresa usa hoje, colocaria esses três grupos no mesmo balde. Os dados mostram três clientes distintos:

- **S3:** quem mora em apartamentos pequenos perto do mar e paga caro por isso;
- **S4:** famílias de renda alta em casas novas e grandes no subúrbio;
- **S5:** classe média em bairros antigos e consolidados.

**Outros destaques:**

- **S6** tem renda 2,5 vezes maior que S1 e casas 4,9 vezes mais caras. **38% dos seus block groups estão no teto de US\$ 500 mil**, então o preço real é ainda maior.
- **S1** é o mercado mais acessível: a casa custa 3,6 anos de renda, contra 7,0 em S3.
- **S2** tem os domicílios mais cheios (3,8 pessoas) e a menor renda per capita (US\$ 6.200), no entorno mais denso do estado (3.927 hab./km²).
- **S4** concentra o crescimento: **23% dos seus block groups têm casas de até 10 anos**, contra 0% em S5.
'''

INTERP["[[INTERP-SEGMENT-CARDS]]"] = r'''
Os números a seguir são medianas dos block groups de cada segmento.

---

### S1 · Interior acessível
**18,4% dos domicílios (1,9 milhão) · casas de US\$ 91 mil · renda de US\$ 26 mil**

- **Quem mora:** famílias de renda baixa a média, com 2,8 pessoas por domicílio.
- **Onde:** Vale Central e norte do estado, a **110 km da costa** (64% no interior profundo). Cidades de referência: Bakersfield, Fresno, Redding e Chico. O entorno é rural ou de cidades médias (395 hab./km²).
- **Imóvel:** casas de tamanho médio (5,3 cômodos), com 24 anos de idade mediana.
- **Preço:** o mais baixo do estado e o **mais acessível** (3,6 anos de renda). Preços concentrados entre US\$ 70 mil e US\$ 117 mil.
- **Em uma frase:** a casa própria acessível, longe do mar.

### S2 · Famílias urbanas populares
**14,0% dos domicílios (1,4 milhão), mas 5,5 milhões de pessoas · casas de US\$ 145 mil · renda de US\$ 24 mil**

- **Quem mora:** famílias grandes (**3,8 pessoas por domicílio**, a maior) e a menor renda per capita do estado (US\$ 6.200 por pessoa).
- **Onde:** **64% em Los Angeles County** (Los Angeles, Huntington Park, Inglewood), no entorno **mais denso** do estado (3.927 hab./km²), a 12 km de uma grande cidade.
- **Imóvel:** moradias pequenas (4,1 cômodos) e antigas (35 anos). Quase nenhuma construção nova (1,3%).
- **Preço:** US\$ 145 mil, ou 5,7 anos de renda. Comprar é difícil para quem mora lá.
- **Em uma frase:** muita gente em pouco espaço, nos bairros populares das metrópoles.

### S3 · Urbano compacto costeiro
**17,1% dos domicílios (1,8 milhão) · casas de US\$ 206 mil · renda de US\$ 30 mil**

- **Quem mora:** domicílios **pequenos (2,1 pessoas, o menor)**: solteiros, casais sem filhos, jovens profissionais e aposentados.
- **Onde:** a **7 km do mar** (43% a menos de 5 km), em Los Angeles (27%), na Baía de San Francisco (24%) e em San Diego (17%). Cidades de referência: San Diego, Santa Monica e Culver City.
- **Imóvel:** apartamentos e moradias compactas (4,1 cômodos, com a maior proporção de quartos sobre cômodos). Este segmento tem mais domicílios por block group que qualquer outro: são prédios.
- **Preço:** **o menos acessível: 7,0 anos de renda.** Quem mora ali, em boa parte, aluga.
- **Em uma frase:** morar pequeno perto do mar, pagando caro pela localização.

### S4 · Subúrbios familiares em expansão
**23,6% dos domicílios (2,4 milhões, o maior segmento) · casas de US\$ 215 mil · renda de US\$ 50 mil**

- **Quem mora:** famílias de renda média-alta (3,0 pessoas por domicílio).
- **Onde:** subúrbios a **25 km da costa** e 46 km de uma grande cidade, em todas as regiões (Baía, San Diego, Inland Empire, Central Coast). Cidades de referência: Santa Clarita, Poway, Simi Valley e Santa Rosa. O entorno é de baixa densidade (1.026 hab./km²).
- **Imóvel:** casas **grandes (6,3 cômodos) e novas (16 anos, a menor idade)**. **23% dos block groups têm casas de até 10 anos.**
- **Preço:** US\$ 215 mil, mas acessível para os moradores (4,2 anos de renda).
- **Em uma frase:** a casa grande e nova da família que trocou a cidade pelo subúrbio, onde o mercado está crescendo.

### S5 · Classe média urbana consolidada
**16,7% dos domicílios (1,7 milhão) · casas de US\$ 216 mil · renda de US\$ 39 mil**

- **Quem mora:** classe média (2,7 pessoas por domicílio).
- **Onde:** bairros tradicionais de Los Angeles (42%) e da Baía de San Francisco (34%), a 11 km do mar, em entorno denso (2.936 hab./km²). Cidades de referência: San Francisco, Daly City e Culver City.
- **Imóvel:** casas de tamanho médio (5,2 cômodos) e **as mais antigas (38 anos)**. **Nenhum block group com casas novas**: é um estoque totalmente consolidado.
- **Preço:** US\$ 216 mil, ou 5,3 anos de renda.
- **Em uma frase:** o bairro tradicional de casas antigas, onde o negócio é revenda e reforma.

### S6 · Alto padrão costeiro
**10,2% dos domicílios (1,0 milhão), mas 21% do valor do estoque · casas de US\$ 444 mil ou mais · renda de US\$ 64 mil**

- **Quem mora:** a maior renda (US\$ 64 mil por domicílio; US\$ 25 mil per capita, quatro vezes a de S2).
- **Onde:** **a 5,5 km do mar** (47% a menos de 5 km), na Baía de San Francisco (38%), em Los Angeles (35%) e em Orange County (12%). Cidades de referência: Santa Monica, San Rafael e Redondo Beach.
- **Imóvel:** **as maiores casas (6,5 cômodos)**, com 33 anos de idade mediana.
- **Preço:** mediana de US\$ 444 mil, e **38% no teto de US\$ 500 mil**: o preço real é maior do que os dados mostram.
- **Em uma frase:** o litoral de luxo das metrópoles.
'''

INTERP["[[INTERP-MACRO]]"] = r'''
**Três macro-segmentos**, úteis para a comunicação institucional e para a estrutura das equipes:

| Macro-segmento | Segmentos | Domicílios | O que os une |
|---|---|---|---|
| **1. Casas fora dos centros** | S1 e S4 | 42% | casas espaçosas, longe do mar e dos centros; a diferença é a renda |
| **2. Núcleo urbano** | S2, S3 e S5 | 48% | bairros densos e consolidados das metrópoles; a diferença é o perfil do domicílio |
| **3. Alto padrão** | S6 | 10% | um mercado à parte, distante de todos os outros |

**Os níveis de granularidade ficam claros:**

- **3 macro-segmentos** para a estratégia corporativa;
- **6 segmentos** para marketing e alocação de equipes;
- **subsegmentos** (abaixo) para campanhas locais.
'''

INTERP["[[INTERP-RECURSIVE]]"] = r'''
**S3 esconde dois mercados.** Dentro dele, a silhouette com 2 subsegmentos é de **0,20**, o dobro da silhouette de S3 na segmentação geral (0,10):

| | S3.1 · Compactos novos | S3.2 · Apartamentos à beira-mar |
|---|---|---|
| Block groups | 1.740 | 895 |
| Idade das casas | 19 anos | 33 anos |
| Distância da costa | 9 km | **4 km** |
| Valor mediano | US\$ 186 mil | **US\$ 273 mil** |
| Renda mediana | US\$ 31 mil | US\$ 27 mil |
| Pessoas por domicílio | 2,2 | 1,9 |

- **S3.1:** condomínios e apartamentos mais novos, espalhados pelas regiões metropolitanas, com preço moderado.
- **S3.2:** apartamentos antigos colados ao mar, concentrados em San Francisco, no oeste de Los Angeles e no litoral de San Diego. São caríssimos para a renda de quem mora lá (10 anos de renda): **mercado de aluguel e de investidores**.

**Recomendação:** tratar S3 com **duas ofertas**. Em S3.1, o foco é o primeiro imóvel próprio; em S3.2, o foco é a gestão de aluguel e o investidor.
'''

INTERP["[[INTERP-MARKET]]"] = r'''
- **O mercado total tem 10,3 milhões de domicílios e um estoque estimado em US\$ 2,2 trilhões** (valores de 1990).
- **S4 é o maior mercado** nas duas medidas: 23,6% dos domicílios e 24,5% do valor.
- **S6 tem só 10,2% dos domicílios, mas 20,6% do valor do estoque.** Cada transação vale, em média, mais que o dobro da dos demais segmentos.
- **S1 e S2 juntos têm 32% dos domicílios, mas só 19% do valor.** São mercados de volume, e não de valor.

**Implicação:** a imobiliária precisa decidir entre **volume** (S1, S2, S4) e **valor por transação** (S6, S3, S5). Os segmentos permitem fazer essa escolha de forma explícita.
'''

INTERP["[[INTERP-OPPORTUNITY]]"] = r'''
- **O modelo de valor esperado é confiável:** R² de 0,87 na validação cruzada. A diferença entre preço real e esperado é informativa, e não ruído do modelo.
- **Cerca de 1.700 block groups (8,5%) estão subvalorizados**, com preço 20% ou mais abaixo do que os seus fundamentos indicam.
- **S3 tem a maior oportunidade:** **16% dos seus block groups estão subvalorizados** (cerca de 280 mil domicílios), em San Diego, Burbank e Culver City. É também o segmento com a maior dispersão de preço (IQR de 57% da mediana) e com mais casos sobrevalorizados (14%). Os preços de S3 ainda não se ajustaram aos fundamentos.
- **S1 vem em segundo** (cerca de 12%, em Redding, Bakersfield e Yuba City): cidades do interior com fundamentos melhores que o preço.
- **S4 combina crescimento com oportunidade:** 23% de casas novas e cerca de 8% de subvalorizados.
- **S6 quase não tem subvalorizados (menos de 2%)**, mas isso é em parte um efeito do teto: o preço real de 38% dos seus block groups é desconhecido.

> **Atenção:** "cidade de referência" é a cidade mais próxima numa lista das maiores cidades do estado. Em Los Angeles, nomes como Burbank e Culver City representam bairros vizinhos a essas cidades, e não só os seus limites oficiais.
'''

INTERP["[[INTERP-ENSEMBLE]]"] = r'''
[[ENSEMBLE-TEXT]]
'''

INTERP["[[INTERP-PRIORITY]]"] = r'''
[[PRIORITY-TEXT]]
'''

INTERP["[[INTERP-ALLOCATION]]"] = r'''
[[ALLOCATION-TEXT]]
'''

INTERP["[[INTERP-STRATEGIES]]"] = r'''
[[STRATEGIES-TEXT]]
'''

INTERP["[[INTERP-CONCLUSION]]"] = r'''
[[CONCLUSION-TEXT]]
'''
