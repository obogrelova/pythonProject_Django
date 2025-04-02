import asyncio
import os
import logging
from aiogram import Bot
from aiogram.types import FSInputFile
from django.conf import settings
from .config import TELEGRAM_BOT_TOKEN, ADMIN_CHAT_ID

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_photo_to_admin(photo_path, caption):
    try:
        await bot.send_photo(ADMIN_CHAT_ID, photo=FSInputFile(photo_path), caption=caption)
    except Exception as e:
        logging.error(f'Ошибка при отправке изображения: {e}')

def send_photo(photo_url, caption):
    photo_path = os.path.join(settings.MEDIA_ROOT, photo_url.replace(settings.MEDIA_URL, ''))

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_in_executor(None, lambda: asyncio.run(send_photo_to_admin(photo_path, caption)))
    except RuntimeError:
        asyncio.run(send_photo_to_admin(photo_path, caption))