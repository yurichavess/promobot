import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.2")


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def gerar_copy(produto):
    if not OPENAI_API_KEY:
        return gerar_copy_fallback(produto)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.responses.create(
            model=OPENAI_MODEL,
            input=montar_prompt(produto),
        )

        texto = response.output_text.strip()
        return texto or gerar_copy_fallback(produto)
    except Exception as erro:
        print(f"OpenAI indisponivel, usando fallback: {erro}")
        return gerar_copy_fallback(produto)


def montar_prompt(produto):
    preco = formatar_moeda(produto["preco"])
    preco_antigo = formatar_moeda(produto["preco_antigo"])

    return f"""
Crie uma mensagem curta para Telegram divulgando esta promocao.
Use tom direto, chamativo e sem exageros.
Nao invente informacoes.
Inclua o link no final.

Produto: {produto["titulo"]}
Preco antigo: {preco_antigo}
Preco atual: {preco}
Desconto: {produto["desconto"]}% OFF
Categoria: {produto["categoria"]}
Descricao: {produto["descricao"]}
Link: {produto["link"]}
"""


def gerar_copy_fallback(produto):
    preco = formatar_moeda(produto["preco"])
    preco_antigo = formatar_moeda(produto["preco_antigo"])

    return f"""
Produto: {produto["titulo"]}

Preco: de {preco_antigo} por {preco}
Desconto: {produto["desconto"]}% OFF

{produto["descricao"]}

Link: {produto["link"]}
"""
