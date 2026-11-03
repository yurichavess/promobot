def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def calcular_desconto(preco, preco_antigo):
    if not preco_antigo or preco_antigo <= 0 or preco >= preco_antigo:
        return 0

    return round((1 - preco / preco_antigo) * 100)