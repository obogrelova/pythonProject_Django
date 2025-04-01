import asyncio
import os
import logging
from aiogram import Bot
from aiogram.types import FSInputFile
from django.conf import settings
from .config import TELEGRAM_BOT_TOKEN, ADMIN_CHAT_ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_message_to_admin(text):
    try:
        await bot.send_message(ADMIN_CHAT_ID, text)
    except Exception as e:
        logging.error(f'Ошибка при отправке сообщения: {e}')

async def send_photo_to_admin(photo_path, caption):
    try:
        await bot.send_photo(ADMIN_CHAT_ID, photo=FSInputFile(photo_path), caption=caption)
    except Exception as e:
        logging.error(f'Ошибка при отправке изображения: {e}')

def send_message(text):
    asyncio.run(send_message_to_admin(text))

def send_photo(photo_url, caption):
    photo_path = os.path.join(settings.MEDIA_ROOT, photo_url.replace(settings.MEDIA_URL, ''))

    try:
        loop = asyncio.get_running_loop()
        loop.run_in_executor(None, lambda: asyncio.run(send_photo_to_admin(photo_path, caption)))
    except RuntimeError:
        asyncio.run(send_photo_to_admin(photo_path, caption))