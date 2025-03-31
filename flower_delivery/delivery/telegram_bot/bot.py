from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes
from .config import TELEGRAM_BOT_TOKEN, ADMIN_CHAT_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=f'Your chat ID: {chat_id}')

async def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())