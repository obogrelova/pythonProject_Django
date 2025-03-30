from aiogram import Bot
import logging
import asyncio
from .config import TELEGRAM_BOT_TOKEN, ADMIN_CHAT_ID


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_message_to_admin(text):
    try:
        await bot.send_message(ADMIN_CHAT_ID, text)
    except Exception as e:
        logging.error(f'Ошибка при отправке сообщения: {e}')


async def send_image_to_admin(image_url, caption):
    try:
        await bot.send_photo(ADMIN_CHAT_ID, photo=image_url, caption=caption)
    except Exception as e:
        logging.error(f'Ошибка при отправке изображения: {e}')


def send_message(text):
    asyncio.run(send_message_to_admin(text))


def send_photo(image_url, caption):
    asyncio.run(send_image_to_admin(image_url, caption))