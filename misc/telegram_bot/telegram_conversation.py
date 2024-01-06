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


def get_token():
    tg_token = ""
    with open("tg_token") as file:
        tg_token = file.read()
    return tg_token


EXERCISE, EXERCISE_DATA, EXERCISE_NOTES = range(3)


class TelegramConversation:
    def __init__(self, logger) -> None:
        self.telegram_token = get_token()
        self.logger = logger

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Starts the conversation and asks the user about exercise."""
        reply_keyboard = [["Squat", "Deadlift"], ["Pull-ups", "Push-ups"]]
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
        """Selected exercise and add it to context."""
        self.logger.info("Exercise %s", update.message.text)
        context.user_data["exercise"] = update.message.text
        return EXERCISE_DATA

    async def get_exercise_data(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Handle input"""
        context.user_data["exercise_data"] = update.message.text
        self.logger.info("Exercise data %s", update.message.text)
        await update.message.reply_text(
            f"{update.message.from_user.first_name}, send any notes. Click /no overwise."
        )
        return EXERCISE_NOTES

    async def get_exercise_notes(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Handle input"""
        context.user_data["exercise_notes"] = update.message.text
        self.logger.info("Exercise data %s", update.message.text)
        await self.save_data(update, context)
        await self.start(update, context)
        return EXERCISE

    async def save_data(self, update, context):
        record = Record.init_from_tg_bot(context.user_data)
        record.to_gsheet()
        self.logger.info("Saved %s", context.user_data)
        await update.message.reply_text("Saved")

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancels and ends the conversation."""
        await update.message.reply_text(
            "Bye! Send /start to start again.", reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    def create_conversation(self):
        conversation = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                EXERCISE: [
                    MessageHandler(
                        filters.Regex("^(Squat|Deadlift|Pull-ups|Push-ups)$"),
                        self.get_exercise,
                    )
                ],
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
