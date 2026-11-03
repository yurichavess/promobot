from app.utils import calcular_desconto


def buscar_produtos():
    produtos = [
        {
            "titulo": "Gabinete Aquario Branco",
            "preco": 299.90,
            "preco_antigo": 499.90,
            "categoria": "informatica",
            "asin": "B08FAKE1276",
            "link": "https://www.amazon.com.br/",
            "descricao": "Gabinete Branco Simples",
        }
    ]

    for produto in produtos:
        produto["desconto"] = calcular_desconto(
            produto["preco"], produto["preco_antigo"]
        )

    return produtos