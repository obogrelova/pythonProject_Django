import asyncio
import logging
from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes
from aiogram import Bot
import config

bot = Bot(token=TOKEN)

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=f'Your chat ID: {chat_id}')

async def send_message_to_admin(text):
    try:
        await bot.send_message(ADMIN_CHAT_ID, text)
    except Exception as e:
        logging.error(f'Ошибка при отправке сообщения: {e}')

def send_message(text):
    asyncio.run(send_message_to_admin(text))

async def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())