DESCONTO_MINIMO = 30
PRECO_MAXIMO = 500
CATEGORIAS_PERMITIDAS = {"informatica"}


def oferta_valida(produto):
    desconto_ok = produto["desconto"] >= DESCONTO_MINIMO
    preco_ok = produto["preco"] <= PRECO_MAXIMO
    categoria_ok = produto["categoria"] in CATEGORIAS_PERMITIDAS

    return desconto_ok and preco_ok and categoria_ok
