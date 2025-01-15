import re
from datetime import datetime, date
from django.utils import timezone

from asgiref.sync import sync_to_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, MessageHandler,
                          filters)

from telegram_bot.commands.start import create_user_account
from telegram_bot.models import Refuel
from datetime import timedelta
# States for adding a refuel
FUEL, ODOMETER, DATE, LOCATION = range(4)


def get_date_buttons():
    """
    Returns an inline keyboard markup with
    buttons for selecting yesterday, today, or cancelling.
    """
    today = datetime.today()
    yesterday = today - timedelta(days=1)

    # Buttons to select date
    keyboard = [
        [InlineKeyboardButton("Yesterday", callback_data=f"date_{yesterday.strftime('%d.%m.%Y')}")],
        [InlineKeyboardButton("Today", callback_data=f"date_{today.strftime('%d.%m.%Y')}")],
        [InlineKeyboardButton("Cancel", callback_data="cancel")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_location_buttons():
    """
    Returns an inline keyboard markup with 'Skip' 
    and 'Cancel' buttons for location input.
    """
    keyboard = [
        [InlineKeyboardButton("Skip", callback_data="skip_location")],
        [InlineKeyboardButton("Cancel", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_cancel_button():
    """
    Returns an inline keyboard
    markup with a 'Cancel' button.
    """
    keyboard = [
        [InlineKeyboardButton("Cancel", callback_data="cancel")]
    ]

    return InlineKeyboardMarkup(keyboard)


async def start_add_refuel(update: Update, context: CallbackContext):
    """Starts the process of adding a refuel entry, prompting the user for the amount of fuel."""
    await update.message.reply_text(
        "You want to add a gas station! Let's start with how much gas did you put in? (in gallons)", 
        reply_markup=get_cancel_button()
    )
    return FUEL


async def fuel(update: Update, context: CallbackContext):
    """Handles the user's input for the amount of fuel and validates it."""

    # Extract the callback query from the update
    query = update.callback_query
    # if data from callback
    if query:
        data = query.data
        # If the user cancels the action
        if data == "cancel":
            await query.answer("Action canceled.")
            await query.edit_message_text("Action canceled.")
            # Clear the user's data
            context.user_data.clear()
            # End the conversation
            return ConversationHandler.END
    # Extract the user's message as text
    fuel_input = update.message.text

    # Validation: check that the entered number is positive (using regular expressions)
    if not re.match(r"^\d+(\.\d+)?$", fuel_input):  # Check for a number with a float point
        await update.message.reply_text("Please enter a valid number for the fuel volume (e.g., 5.5 or 10).")
        # Return to the fuel input step
        return FUEL
    
    # Store fuel_input in user data
    context.user_data['fuel'] = float(fuel_input)
    await update.message.reply_text("Enter your current odometer reading (in miles).", reply_markup=get_cancel_button())
    return ODOMETER  # Move to the next step, ODOMETER


async def odometer(update: Update, context: CallbackContext):
    """Handles the user's input for the odometer reading and validates it."""

    # Extract the callback query from the update
    query = update.callback_query

    # if data from callback
    if query:
        data = query.data
        # If the user cancels the action
        if data == "cancel":
            await query.answer("Action canceled.")
            await query.edit_message_text("Action canceled.")
            # clear the users data and send conversation 
            context.user_data.clear()
            return ConversationHandler.END
    # if data from message
    odometer_input = update.message.text
    # Validation: check that the entered number is positive (using regular expressions)
    if not re.match(r"^\d+(\.\d+)?$", odometer_input):
        await update.message.reply_text("Please enter a valid number for the odometer reading (e.g., 15000 or 12345.67).")
        # Return to the odometer input step
        return ODOMETER 
    context.user_data['odometer'] = float(odometer_input)
    await update.message.reply_text("Enter the date of refueling (dd.mm.yyyy).", reply_markup=get_date_buttons())
    return DATE  # Move to the next step, DATE


async def date(update: Update, context: CallbackContext):
    """Handles the user's input for the date of refueling and validates it."""
    # Extract the callback query from the update
    query = update.callback_query
    # Check if there's a callback query
    if query:
        data = query.data
        if data == "cancel":
            await query.answer("Action canceled.")
            await query.edit_message_text("Action canceled.")
            context.user_data.clear()
            return ConversationHandler.END
        # Check if the callback data starts with "date_"
        if data.startswith("date_"):
            # Extract the date from the callback data
            selected_date = data.split("_")[1]
            # Store the selected date in user data
            context.user_data['date'] = selected_date
            await query.answer()
            # Inform the user of the selected date
            await query.edit_message_text(f"You selected: {selected_date}")
            await query.message.reply_text(
                "Please provide your location or skip:",
                reply_markup=get_location_buttons()
            )
            return LOCATION  # Move to the next step, LOCATION
    
        # Extract the user's message as text
    if update.message:
        try:
            date_text = update.message.text
            # Try to parse the date text into a datetime object
            datetime.strptime(date_text, "%d.%m.%Y")
            # Store the parsed date in user data
            context.user_data['date'] = date_text
            await update.message.reply_text(
                    "Please provide your location or skip:",
                    reply_markup=get_location_buttons()
                )
            return LOCATION  # Move to the next step, LOCATION
        except ValueError:
            await update.message.reply_text("Invalid date format. Try again.")
            return DATE  # Move to the next step, DATE
    else:
        await update.message.reply_text("Error: No message received.")
        return DATE


async def location(update: Update, context: CallbackContext):
    """Handles the user's input for location and saves the refuel entry."""
    # Extract the callback query from the update
    query = update.callback_query
    # Check if there's a callback query
    if query:
        data = query.data
        if data == "cancel":
            await query.answer("Action canceled.")
            await query.edit_message_text("Action canceled.")
            # Clear the user's data and End the conversation
            context.user_data.clear()
            return ConversationHandler.END
        # Check if the callback data is skip
        if query.data == "skip_location":
            # Store the Not specified in user data
            context.user_data['location'] = "Not specified"
            await query.answer()
            await query.edit_message_text("Location skipped.")
            #Save to db
            refuel = await save_to_db(update, context) 

            if refuel:
                await query.message.edit_text("Refueling saved!")
            return ConversationHandler.END
    # Store the location in user data
    location_text = update.message.text
    context.user_data['location'] = location_text
    refuel = await save_to_db(update, context)

    if refuel:
        await update.message.reply_text("Refueling saved!")
        return ConversationHandler.END


async def save_to_db(update: Update, context: CallbackContext):
    """Saves the refuel entry to the database."""
    user = update.effective_user
    # get useraccount object
    user = await create_user_account(user)

    fuel = context.user_data['fuel']
    odometer = context.user_data['odometer']
    refuel_date = context.user_data['date']
    location = context.user_data['location']
    refuel_date = datetime.strptime(refuel_date, "%d.%m.%Y")
    if refuel_date.tzinfo is None:
        refuel_date = timezone.make_aware(refuel_date, timezone.get_current_timezone()) 

    # Saving data to the database
    refuel = await sync_to_async(Refuel.objects.create)(
        user=user,
        fuel_amount=float(fuel),
        odometer_reading=float(odometer),
        date=refuel_date,
        location=location
    )
    return refuel 


async def cancel(update: Update, context: CallbackContext):
    context.user_data.clear()
    await update.message.reply_text("Addition of filling cancelled.")
    return ConversationHandler.END


def get_refuel_handler():
    """ Returns the ConversationHandler for managing the refuel process."""
    return ConversationHandler(
        entry_points=[
            CommandHandler("add_refuel", start_add_refuel),
            MessageHandler(filters.Regex('Add Fuel Entry'), start_add_refuel)],
        states={
            FUEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, fuel),
                   CallbackQueryHandler(fuel, pattern="^cancel")],
            ODOMETER: [MessageHandler(filters.TEXT & ~filters.COMMAND, odometer),
                       CallbackQueryHandler(odometer, pattern="^cancel")],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, date),
                   CallbackQueryHandler(date, pattern="^date_|^cancel$")],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, location),
                       CallbackQueryHandler(location, pattern="^skip_location|^cancel")]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

