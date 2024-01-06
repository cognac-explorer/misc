import logging
from telegram_conversation import TelegramConversation


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("Conversation logger")

if __name__ == "__main__":
    telegram_conversation = TelegramConversation(logger=logger)
    telegram_conversation.main()
