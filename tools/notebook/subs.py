PAIR_DROPS = '["households", "bedroom_share", "luxury_index"]'

DECISIONS = r'''{
    "MedInc":              ("manter", "renda dos moradores: o centro do eixo de riqueza"),
    "MedHouseVal":         ("manter", "nível de preço: a variável central para o negócio"),
    "HouseAge":            ("manter", "idade do estoque de imóveis: informação única"),
    "AveRooms":            ("manter", "tamanho da moradia: casas vs. apartamentos"),
    "AveOccup":            ("manter", "tamanho do domicílio: famílias vs. pessoas sozinhas"),
    "dist_coast_km":       ("manter", "proximidade do oceano: principal motor de preço na Califórnia"),
    "pop_density_3km":     ("manter", "entorno urbano vs. rural"),
    "AveBedrms":           ("remover", "quase constante e coberta por AveRooms"),
    "Population":          ("remover", "tamanho do block group é um artefato do Censo, não um perfil de bairro"),
    "dist_big_city_km":    ("remover", "sobreposta à densidade; mantida para descrição"),
    "income_vs_neighbors": ("remover", "contraste local, não um perfil de bairro; mantida para descrição"),
    "income_per_person":   ("remover", "combinação de MedInc e AveOccup (VIF); mantida para descrição"),
    "price_to_income":     ("remover", "combinação de MedHouseVal e MedInc (VIF); mantida para descrição"),
    "rooms_per_person":    ("remover", "combinação de AveRooms e AveOccup (VIF)"),
    "bedroom_share":       ("remover", "quase duplicata de AveRooms"),
    "households":          ("remover", "quase duplicata de Population"),
    "luxury_index":        ("remover", "resume renda, valor e cômodos (contagem dupla); usado para descrição"),
}'''

K_FINAL = "6"

SEGMENT_NAMES = r'''{
    1: "Interior acessível",
    2: "Famílias urbanas populares",
    3: "Urbano compacto costeiro",
    4: "Subúrbios familiares em expansão",
    5: "Classe média urbana consolidada",
    6: "Alto padrão costeiro",
}'''

SUBS = {"[[PAIR_DROPS]]": PAIR_DROPS, "[[DECISIONS]]": DECISIONS, "[[K_FINAL]]": K_FINAL,
        "[[SEGMENT_NAMES]]": SEGMENT_NAMES}
