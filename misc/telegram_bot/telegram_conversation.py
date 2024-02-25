from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from data_stuff import Record
from utils import render_plot, read_last_n_records, get_gs_client, GSHEET_FILENAME
from config import tg_reply_keyboard


def get_token():
    tg_token = ""
    with open("tg_token") as file:
        tg_token = file.read()
    return tg_token

# conversation stages
EXERCISE, EXERCISE_DATA, EXERCISE_NOTES = range(3)


class TelegramConversation:
    def __init__(self, logger) -> None:
        self.telegram_token = get_token()
        self.logger = logger

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Starts the conversation and asks user about exercise."""
        reply_keyboard = tg_reply_keyboard
        text = "Select exercise which result to save. Send /cancel to stop."

        self.logger.info("Telegram conversation started")
        await update.message.reply_text(
            text,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True,
                input_field_placeholder="Select exercise:",
            ),
        )
        return EXERCISE

    async def get_exercise(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Add exercise to context."""
        self.logger.info("Exercise %s", update.message.text)
        context.user_data["exercise"] = update.message.text
        await update.message.reply_text(
            "Format: {sets num}-{reps num}-{weight}"
        )
        return EXERCISE_DATA

    async def get_exercise_data(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Add exercise data to context."""
        context.user_data["exercise_data"] = update.message.text
        self.logger.info("Exercise data %s", update.message.text)
        await update.message.reply_text(
            f"{update.message.from_user.first_name}, send any notes. Click /no overwise."
        )
        return EXERCISE_NOTES

    async def get_exercise_notes(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Add exercise notes to context."""
        context.user_data["exercise_notes"] = update.message.text
        self.logger.info("Exercise data %s", update.message.text)
        await self.save_data(update, context)
        await self.send_stats(update, context.user_data["exercise"])
        await self.start(update, context)
        return EXERCISE

    async def save_data(self, update, context):
        """Save record to google sheet."""
        record = Record.init_from_tg_bot(context.user_data)
        record.to_gsheet(get_gs_client(), GSHEET_FILENAME)
        self.logger.info("Saved %s", context.user_data)
        await update.message.reply_text("Saved")

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancel conversation."""
        await update.message.reply_text(
            "Bye! Send /start to start again.", reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    async def send_stats(self, update, exercise):
        """Send simple statistic about saved exercise."""
        dates, values = read_last_n_records(exercise, n=5)
        await update.message.reply_photo(render_plot(dates, values))

    def create_conversation(self):
        """Init ConversationHandler."""
        conversation = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                EXERCISE: [MessageHandler(filters.TEXT, self.get_exercise)],
                EXERCISE_DATA: [MessageHandler(filters.TEXT, self.get_exercise_data)],
                EXERCISE_NOTES: [MessageHandler(filters.TEXT, self.get_exercise_notes)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
            allow_reentry=True,
        )
        return conversation

    def main(self):
        application = Application.builder().token(self.telegram_token).build()
        application.add_handler(self.create_conversation())
        application.run_polling()
