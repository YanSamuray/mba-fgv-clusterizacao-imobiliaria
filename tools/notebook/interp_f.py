"""Caixas de destaque ao fim de cada seção: acrescentadas ao último texto de interpretação da seção."""


def callout(*items):
    """Uma caixa de citação com até três destaques: (tipo, texto)."""
    return "\n>\n".join(f"> **{kind}** · {body}" for kind, body in items)


CALLOUTS = {
    "[[INTERP-EDA-CONCLUSION]]": callout(
        ("Insight", "O mercado tem pelo menos duas faces: no litoral, a casa custa 5,6 a 5,8 anos de renda; no "
                    "interior, 3,6. E, para a mesma renda, o preço varia muito."),
        ("Decisão", "Remover só o que não é residencial, transformar as caudas longas e criar variáveis de "
                    "localização sem usar as coordenadas diretamente."),
        ("Para o negócio", "Renda e região não bastam para descrever um cliente: é preciso combinar mais dimensões."),
    ),
    "[[INTERP-SCALING]]": callout(
        ("Decisão", "85 linhas removidas (0,4%), cada uma com um motivo; log e winsorização leve no restante; "
                    "StandardScaler, para que cada variável pese o mesmo na distância."),
        ("Para o negócio", "Nenhum bairro real é descartado por ser extremo: casas de veraneio e bairros de luxo "
                           "continuam na análise."),
    ),
    "[[INTERP-SELECTION]]": callout(
        ("Insight", "A proximidade do mar é o segundo maior motor de preço, depois da renda (correlação de −0,50)."),
        ("Decisão", "7 variáveis finais, sem redundância (VIF máximo de 2,9), cobrindo poder aquisitivo, moradia, "
                    "perfil da família e localização."),
        ("Para o negócio", "Cada segmento será descrito em variáveis que a equipe comercial entende."),
    ),
    "[[INTERP-PCA-DENSITY]]": callout(
        ("Insight", "O mercado tem pelo menos quatro dimensões independentes (riqueza, urbano vs. periferia, tamanho "
                    "da família e idade do estoque) e forma uma nuvem contínua, sem grupos isolados."),
        ("Decisão", "Clusterizar sobre as 7 variáveis originais, para manter a interpretação; o PCA fica para a "
                    "visualização."),
    ),
    "[[INTERP-COMPARISON]]": callout(
        ("Decisão", "K-Means com 6 segmentos: as melhores métricas entre os algoritmos testados e o maior número de "
                    "segmentos que continua estável."),
        ("Insight", "O DBSCAN encontra um único grupo: os segmentos são regiões de um contínuo, e não ilhas."),
        ("Para o negócio", "Seis segmentos bastam para diferenciar estratégias, e nenhum é pequeno demais para ter "
                           "uma equipe própria."),
    ),
    "[[INTERP-PCA-CLUSTERS]]": callout(
        ("Insight", "Segmentos muito estáveis (ARI de 0,94; Jaccard acima de 0,93 em todos) e coerentes no mapa, "
                    "sem usar as coordenadas."),
        ("Para o negócio", "Os segmentos são tipos de bairro que se repetem em várias cidades: a mesma estratégia "
                           "vale em Los Angeles, San Francisco e San Diego."),
    ),
    "[[INTERP-ENSEMBLE]]": callout(
        ("Insight", "S3, S4 e S5 custam o mesmo (cerca de US\\$ 210 mil) e são clientes opostos."),
        ("Decisão", "Três níveis de granularidade: 3 macro-segmentos, 6 segmentos e subsegmentos onde o segmento "
                    "esconde mercados diferentes."),
        ("Para o negócio", "Os bairros contestados (6,5%) são os primeiros a mudar de segmento e merecem "
                           "monitoramento."),
    ),
    "[[INTERP-CALLOUT-9]]": callout(
        ("Para o negócio", "S4 recebe cerca de um terço do orçamento e das equipes; S3 vira frente de investimento; "
                           "S6 vira operação de luxo."),
        ("Decisão", "A segmentação está pronta para o CRM: um arquivo com o segmento de cada bairro e uma função "
                    "que classifica bairros novos."),
    ),
}
