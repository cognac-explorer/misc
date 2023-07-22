import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('cognac-explorer-tg-bot.json', scope)

tg_token = ''
with open("tg_token") as file:
    # Reading from a file
    tg_token = file.read()

client = gspread.authorize(credentials)
spreadsheet = client.open("test_tg_bot")
worksheet = spreadsheet.get_worksheet(0)

EXERCISE, INPUT, START_OVER = range(3)
row = 1


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Squat", "Deadlift"], ["Pull-ups", "Push-ups"]]
    text = "Select exercise which result to save. Send /cancel to stop."

    await update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Select exercise:"
        ),
    )

    return EXERCISE


async def store_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected exercise."""
    user = update.message.from_user
    exercise = update.message.text
    logger.info("Exercise option recieved; %s: %s", user.first_name, exercise)
    m = f"{user.first_name}, send your {exercise} result"
    context.user_data['exercise'] = exercise
    await update.message.reply_text(m)

    return INPUT


async def handle_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input"""
    global row
    user = update.message.from_user
    message = update.message.text
    logger.info("Input result from %s: %s", user.first_name, message)
    # worksheet.update_cell(row=row, col=1, value=message)
    data = [str(datetime.datetime.now()), context.user_data['exercise'], message]
    worksheet.append_row(data)
    row += 1
    reply = f"{user.first_name} your {context.user_data['exercise']} saved"
    await update.message.reply_text(reply)
    # context.user_data[START_OVER] = True
    await start(update, context)
    # return ConversationHandler.END
    return EXERCISE


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! Send /start to start again.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(tg_token).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            EXERCISE: [MessageHandler(filters.Regex("^(Squat|Deadlift|Pull-ups|Push-ups)$"), store_exercise)],
            INPUT: [MessageHandler(filters.TEXT, handle_result)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
