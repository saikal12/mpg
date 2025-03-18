from telegram import Update
from telegram.ext import CallbackContext


async def help_command(update: Update, context: CallbackContext):
    """Handler for help button"""
    message = ("This bot will help you calculate MPG\n"
               "Available commands:\n"
               "/add_refuel - Add a refuel entry\n"
               "/calculate_mpg - Calculate MPG\n"
               "/view_calculations - View MPG calculations\n"
               "/export_data - Export data\n"
               "/help - Help")
    await update.message.reply_text(message)