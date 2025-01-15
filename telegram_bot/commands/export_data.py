from tempfile import NamedTemporaryFile

import openpyxl
from asgiref.sync import sync_to_async
from openpyxl.styles import Alignment
from telegram import Update
from telegram.ext import CallbackContext

from telegram_bot.commands.start import create_user_account
from telegram_bot.models import MPGCalculation, Refuel


@sync_to_async
def process_export_data(user):
    # 1. Создание Excel файла
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Fuel entries and MPG calculations"

    # 2. Заполнение данных
    headers = ["Date", "Fuel Volume (in gallons)", "Odometer Reading (in miles)", "Fueling Location"]
    sheet.append(headers)  # Добавляем заголовки

    # Пример данных из базы
    refuels = list(Refuel.objects.filter(user=user.id).order_by('-date'))

    for refuel in refuels:
        sheet.append([
            refuel.date.strftime('%d.%m.%Y'),  # Форматируем дату
            refuel.fuel_amount,
            refuel.odometer_reading,
            refuel.location or "N/A"
        ])

    headers = ["Last refuel", "Previous refuel", "Distance", "Fuel_used", "MPG"]
    sheet.append(headers)

    mpg_calculations = list(MPGCalculation.objects.filter(user=user.id))
    for mpg in mpg_calculations:
        sheet.append([
            mpg.refuel_start.date.strftime('%d.%m.%Y'),
            mpg.refuel_end.date.strftime('%d.%m.%Y'),
            mpg.distance,
            mpg.fuel_used,
            mpg.mpg
        ])

        # Настройка ширины колонок
    for column in sheet.columns:
        max_length = max(len(str(cell.value or "")) for cell in column)
        sheet.column_dimensions[column[0].column_letter].width = max_length + 2
    return workbook


async def export_data(update: Update, context: CallbackContext):
    user = update.effective_user
    user = await create_user_account(user)
    workbook = await process_export_data(user)



    # 3. Сохранение файла
    with NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        workbook.save(temp_file.name)
        temp_file.seek(0)

        # 4. Отправка файла пользователю
        await update.message.reply_document(
            document=open(temp_file.name, "rb"),
            filename="Refuel_Report.xlsx",
            caption="Ваш отчет о заправках."
        )