import logging
from os import getenv
from typing import Dict

import pandas as pd
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from check_luck import prize_report 
from lottery_request import request_lottery_number

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

TOKEN = getenv("ST_Lottery_Check_Bot_API_Key")
url="https://thai-lottery1.p.rapidapi.com/index3"

reply_keyboard = [
    ["Date"],
    ["Lottery_Number"],
    ["Done"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    await update.message.reply_text(
        "Hi! My name is Lottery Checker Bot. I will help you check if your lottery number won any prizes."
        " Please provide the date of the lottery draw and the lottery number.",
        reply_markup=markup,
    )

    return CHOOSING


async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(f"Inquire {text.lower()}? ")

    return TYPING_REPLY


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(        
        f"{facts_to_str(user_data)}You can change your opinion or choose DONE to know the result",
        reply_markup=markup,
    )

    return CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info, check lottery number, and end the conversation."""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    lottery_number = user_data.get("Lottery_Number")
    date = user_data.get("Date")
    
    if lottery_number and date:
        # Assuming you have prize_data loaded or fetched from somewhere
        prize_data =  request_lottery_number(url,date)
        prizes_won = prize_report(lottery_number, prize_data)
        
        await update.message.reply_text(
                prizes_won,reply_markup=markup,
            )
        
    else:
        await update.message.reply_text(
            "Please provide both Date and Lottery Number before finishing.",
            reply_markup=markup,
        )

    user_data.clear()
    return ConversationHandler.END
def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^(Date)$"), regular_choice
                ),
                MessageHandler(filters.Regex("^Lottery_Number$"), regular_choice),
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
