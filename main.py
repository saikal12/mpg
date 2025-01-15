import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
import asyncio

from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from core.settings import BOT_TOKEN
from telegram_bot.commands.add_fuel import get_refuel_handler
from telegram_bot.commands.export_data import export_data
from telegram_bot.commands.help import help_command
from telegram_bot.commands.mpg_calculations import mpg_calculations
from telegram_bot.commands.start import start


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    refuel_handler = get_refuel_handler()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(refuel_handler)
    #application.add_handler(CallbackQueryHandler(handle_selection))
    application.add_handler(CommandHandler("view_calculations", mpg_calculations))
    application.add_handler(CommandHandler("export_data", export_data))
    application.add_handler(CommandHandler("help", help_command))

    #application.add_handler(MessageHandler(filters.Regex('Add Fuel Entry'), get_refuel_handler)) 
    application.add_handler(MessageHandler(filters.Regex('View MPG Calculations'), mpg_calculations)) 
    application.add_handler(MessageHandler(filters.Regex('Export Data'), export_data)) 
    application.add_handler(MessageHandler(filters.Regex('Help'), help_command)) 
    application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())