from asgiref.sync import sync_to_async
from django.db.models import QuerySet
from telegram import Update
from telegram.ext import CallbackContext

from telegram_bot.commands.start import create_user_account
from telegram_bot.models import MPGCalculation, Refuel
import logging
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Формат сообщений
)
logger = logging.getLogger(__name__)

@sync_to_async
def get_refuels(user):
    logger.info(Refuel.objects.filter(user=user).order_by('-date_upload').first())
    return Refuel.objects.filter(user=user).order_by('-date_upload').first()

async def mpg_calculations(update: Update, context: CallbackContext):
    logger.info('start work calculatoir')
    user = update.effective_user
    user = await create_user_account(user)
    refuel = await get_refuels(user)
    if refuel:
        logger.info(refuel.end_odometer_reading)
    else:
        logger.info("Нет записей в Refuel.")
    # calculates distance
    distance = abs(refuel.end_odometer_reading - refuel.start_odometer_reading)
    logger.info(distance)
    # Amount of last fuel filled
    fuel_used = refuel.start_fuel + refuel.fuel_amount - refuel.remaining_fuel
    logger.info(fuel_used)
    # Divides the distance traveled by the amount of fuel since the last fill-up.
    mpg = distance / fuel_used
    # save in db
    calculation = await sync_to_async(MPGCalculation.objects.create)(
        user=user,
        date=refuel.date,
        fuel_amount=refuel.fuel_amount,
        start_fuel=refuel.start_fuel,
        remaining_fuel=refuel.remaining_fuel,
        start_odometer_reading=refuel.start_odometer_reading,
        end_odometer_reading=refuel.end_odometer_reading,
        location=refuel.location,
        distance=distance,
        fuel_used=fuel_used,
        mpg=mpg
    )
    await update.message.reply_text(
        f"Refuel date: {refuel.date.strftime('%d.%m.%Y')}.\n"
        f"Refuel location: {refuel.location if refuel.location else 'Not specified'}.\n"
        f"Fuel added: {refuel.fuel_amount} gallons.\n"
        f"Starting fuel level: {refuel.start_fuel} gallons.\n"
        f"Remaining fuel after trip: {refuel.remaining_fuel} gallons.\n"
        f"Starting odometer reading: {refuel.start_odometer_reading} miles.\n"
        f"Ending odometer reading: {refuel.end_odometer_reading} miles.\n"
        f"Distance traveled: {distance:.2f} miles.\n"
        f"Fuel used: {fuel_used:.2f} gallons.\n"
        f"MPG: {mpg:.2f} miles per gallon."
    )