import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
import asyncio

from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

from core.settings import BOT_TOKEN
from telegram_bot.commands.add_fuel import get_refuel_handler
from telegram_bot.commands.export_data import export_data
from telegram_bot.commands.help import help_command
from telegram_bot.commands.mpg_calculations import mpg_calculations
from telegram_bot.commands.start import start

import logging
from telegram import Update

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Формат сообщений
)
logger = logging.getLogger(__name__)  # Создаём логгер

async def error_handler(update: Update, context: CallbackContext):
    logger.error(f"Ошибка: {context.error}")

def main():
    logger.info("Запуск бота...")
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_error_handler(error_handler)
    refuel_handler = get_refuel_handler()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(refuel_handler)
    application.add_handler(CommandHandler("view_calculations", mpg_calculations))
    application.add_handler(CommandHandler("export_data", export_data))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Regex('View MPG Calculations'), mpg_calculations)) 
    application.add_handler(MessageHandler(filters.Regex('Export Data'), export_data)) 
    application.add_handler(MessageHandler(filters.Regex('Help'), help_command)) 
    application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())