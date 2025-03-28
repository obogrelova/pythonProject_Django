import asyncio
import logging
from telegram import Update
from telegram.ext import CommandHandler, Application, ContextTypes
from config import TELEGRAM_BOT_TOKEN, ADMIN_CHAT_ID

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=f'Your chat ID: {chat_id}')

async def send_message_to_admin(text: str, application: Application):
    try:
        await application.bot.send_message(ADMIN_CHAT_ID, text)
    except Exception as e:
        logging.error(f'Ошибка при отправке сообщения: {e}')

async def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))

    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())