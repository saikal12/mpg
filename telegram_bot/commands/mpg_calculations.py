from asgiref.sync import sync_to_async
from django.db.models import QuerySet
from telegram import Update
from telegram.ext import CallbackContext

from telegram_bot.commands.start import create_user_account
from telegram_bot.models import MPGCalculation, Refuel


@sync_to_async
def get_latest_refuels(user) -> QuerySet:
    return list(Refuel.objects.filter(user=user.id).order_by('-date')[:2])


async def mpg_calculations(update: Update, context: CallbackContext):
    user = update.effective_user
    user = await create_user_account(user)
    refuels = await get_latest_refuels(user)
    if len(refuels) < 2:
        await update.message.reply_text("Not enough data to calculate MPG.")
        return
    # get 2 last refuels
    last_refuel, previous_refuel = refuels
    # calculates distance
    distance = last_refuel.odometer_reading - previous_refuel.odometer_reading
    # Amount of last fuel filled
    fuel_used = previous_refuel.fuel_amount
    # Divides the distance traveled by the amount of fuel since the last fill-up.
    mpg = distance / fuel_used
    # save in db
    calculation = await sync_to_async(MPGCalculation.objects.create)(
        user=user,
        refuel_start=previous_refuel,
        refuel_end=last_refuel,
        distance=distance,
        fuel_used=fuel_used,
        mpg=mpg
    )

    await update.message.reply_text(
        f"Refuel start: {previous_refuel.date.strftime('%d.%m.%Y')}, Refuel end: {last_refuel.date.strftime('%d.%m.%Y')}.\n"
        f"Distance calculation: {calculation.distance} miles.\n"
        f"Fuel used: {calculation.fuel_used} gallons.\n"
        f"MPG: {calculation.mpg:.2f} miles per gallon."
    )