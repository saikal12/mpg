from asgiref.sync import sync_to_async
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

from telegram_bot.models import UserAccount


@sync_to_async
def create_user_account(user):
    """
    Gets the object and a boolean value whether the user has been created.
    Create the user if can`t get.
    Return user object and bool """
    # returns user object using user chat id
    user_account, created = UserAccount.objects.get_or_create(
        telegram_id=user.id,
        defaults={
            "username": user.username,
        }
    )
    return user_account


async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    # Create or retrieve the user's account in the database.
    user = await create_user_account(user)
    # Define the keyboard with the main menu options.
    keyboard = [
        [KeyboardButton('Add Fuel Entry')],
        [KeyboardButton("View MPG Calculations")],
        [KeyboardButton("Export Data")],
        [KeyboardButton("Help")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    message = (f"Hello {user.username}\n"
               "This bot will help you calculate the mpg.\n")
    await update.message.reply_text((message), reply_markup=reply_markup)

