INTERP = {}

INTERP["[[INTERP-BUSINESS-QA]]"] = r'''
As perguntas sugeridas para a análise de negócio, respondidas com os resultados das seções 8 e 9:

| Pergunta | Resposta | Evidência |
|---|---|---|
| **Qual cluster oferece o melhor ROI potencial?** | **S3** para compra e valorização; **S4** para lançamentos | S3 tem a maior proporção de subvalorizados (cerca de 16%): comprar 20% abaixo do valor esperado significa um ganho de pelo menos 25% se o preço convergir para os fundamentos (1 ÷ 0,8 − 1). S4 tem o maior mercado e 23% de casas novas: demanda comprovada para lançamentos |
| **Onde estão as áreas subvalorizadas?** | S3 (San Diego, Burbank, Culver City) e S1 (Redding, Bakersfield, Yuba City) | Mapa da seção 9.2 e coluna `subvalorizado` do arquivo exportado |
| **Quais segmentos estão em crescimento?** | **S4**, muito à frente de S1 e S3 | 23% dos block groups de S4 com casas de até 10 anos, contra 8% em S1 e S3 e 0% em S5 |
| **Existe espaço para preço premium?** | Sim, em **S6** e nos apartamentos à beira-mar de **S3.2** | S6 tem a menor dispersão de preço do mercado (IQR de 30% da mediana) e 38% no teto: o preço alto é a regra, e não a exceção. S3.2 custa 10 anos de renda dos moradores: quem compra é o investidor |
| **Onde aplicar descontos estratégicos?** | Nos block groups **sobrevalorizados** (sobretudo em S3, cerca de 14%) e em **S1** | Imóveis acima do valor esperado demoram mais a vender: um preço realista reduz o tempo de venda. Em S1, o mais sensível a preço (3,6 anos de renda), descontos e financiamento aceleram a conversão |
| **Que amenidades cada segmento valoriza?** | S4: quartos extras, quintal, garagem, escolas. S3: localização, transporte, lazer, plantas compactas. S2: mais quartos por custo baixo. S5: modernização. S6: vista, privacidade, segurança | Inferido do perfil (tamanho da família, cômodos, densidade, distância do mar). **São hipóteses a validar** com pesquisa junto aos clientes |
| **Qual o risco de cada cluster?** | **Maior em S3**, menor em S6 e S5 | S3 tem a maior dispersão de preço (IQR de 57% da mediana), a maior fatia de sub e sobrevalorizados e 10% de bairros contestados pelo ensemble: maior risco e maior retorno. S6 e S5 têm os preços mais previsíveis (dispersão de 30% e 42%) |
| **Há oportunidades de *cross-selling* e de retenção?** | Sim, ao longo da **jornada do cliente** | O solteiro ou casal de S3 (2,1 pessoas, apartamento) tende a virar a família de S4 (3,0 pessoas, casa grande): o programa de troca de imóvel retém o cliente de S3 e o leva para S4. Em S5, a venda de serviços de reforma; em S6, a gestão patrimonial; em S3.2, a gestão de aluguel |
'''
