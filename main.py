import argparse
import asyncio

from app.database.db import criar_tabelas, ja_foi_enviado, marcar_como_enviado
from app.filters.filters import oferta_valida
from app.marketplace.collector import buscar_produtos
from app.openai.copywriter import gerar_copy
from app.scheduler.scheduler import iniciar_scheduler
from app.telegram.sender import enviar_mensagem


async def executar_fluxo():
    criar_tabelas()
    produtos = buscar_produtos()

    for produto in produtos:
        if ja_foi_enviado(produto):
            print(f"Produto ja enviado!!!: {produto['titulo']}")
            continue

        if not oferta_valida(produto):
            print(f"Oferta ignorada: {produto['titulo']}")
            continue

        mensagem = gerar_copy(produto)
        await enviar_mensagem(mensagem)
        marcar_como_enviado(produto)
        print(f"Promocao enviada: {produto['titulo']}")


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
