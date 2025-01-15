from telegram import Update
from telegram.ext import CallbackContext


async def help_command(update: Update, context: CallbackContext):
    """Handler for help button"""
    message = ("Этот бот поможет вам рассчитать MPG, а также отслеживать и экспортировать данные заправок. "
               "Доступные команды:\n"
               "/add_refuel - Добавить заправку\n"
               "/calculate_mpg - Рассчитать MPG\n"
               "/view_calculations - Просмотреть расчеты MPG\n"
               "/export_data - Экспортировать данные\n"
               "/help - Помощь")
    await update.message.reply_text(message)