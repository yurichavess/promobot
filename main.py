import argparse
import asyncio
import logging
import os

from app.database.db import criar_tabelas, ja_foi_enviado, marcar_como_enviado
from app.filters.filters import oferta_valida
from app.marketplace.collector import buscar_produtos
from app.openai.copywriter import gerar_copy
from app.scheduler.scheduler import iniciar_scheduler
from app.telegram.sender import enviar_mensagem


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("promobot")

# Pausa entre envios para respeitar o limite do Telegram em canais.
PAUSA_ENTRE_ENVIOS = float(os.getenv("SEND_DELAY_SECONDS", "3"))


async def processar_produto(produto):
    """Processa um produto. Retorna 'enviado', 'duplicado' ou 'ignorado'."""
    titulo = produto.get("titulo", "<sem titulo>")

    # Filtro primeiro: é barato e evita consultar o banco à toa.
    if not oferta_valida(produto):
        logger.info("Oferta ignorada: %s", titulo)
        return "ignorado"

    if ja_foi_enviado(produto):
        logger.info("Produto ja enviado: %s", titulo)
        return "duplicado"

    # gerar_copy é síncrona (cliente OpenAI), então roda em outra thread
    # para não travar o event loop.
    mensagem = await asyncio.to_thread(gerar_copy, produto)
    await enviar_mensagem(mensagem)
    marcar_como_enviado(produto)

    logger.info("Promocao enviada: %s", titulo)
    return "enviado"


async def executar_fluxo():
    criar_tabelas()
    produtos = buscar_produtos()

    resumo = {"enviado": 0, "duplicado": 0, "ignorado": 0, "erro": 0}

    for produto in produtos:
        try:
            status = await processar_produto(produto)
        except Exception:
            # Um produto com problema não pode derrubar o ciclo inteiro.
            logger.exception(
                "Erro ao processar produto: %s", produto.get("titulo", "<sem titulo>")
            )
            resumo["erro"] += 1
            continue

        resumo[status] += 1

        if status == "enviado":
            await asyncio.sleep(PAUSA_ENTRE_ENVIOS)

    logger.info(
        "Ciclo finalizado | enviados: %(enviado)d, duplicados: %(duplicado)d, "
        "ignorados: %(ignorado)d, erros: %(erro)d",
        resumo,
    )


def parse_args():
    parser = argparse.ArgumentParser(description="Promobot")
    parser.add_argument(
        "--scheduler",
        action="store_true",
        help="Mantem o bot rodando e busca promocoes em intervalos.",
    )
    return parser.parse_args()


async def main():
    args = parse_args()

    if args.scheduler:
        await iniciar_scheduler(executar_fluxo)
        return

    await executar_fluxo()


if __name__ == "__main__":
    asyncio.run(main())