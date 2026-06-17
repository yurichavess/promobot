import os

from aiogram import Bot


try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


def criar_bot():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN nao encontrado. Verifique o arquivo .env.")

    return Bot(token=TOKEN)


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


async def enviar_mensagem(mensagem):
    if not CHANNEL_ID:
        raise RuntimeError("CHANNEL_ID nao encontrado. Verifique o arquivo .env.")

    bot = criar_bot()

    try:
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=mensagem,
        )
    finally:
        await bot.session.close()
