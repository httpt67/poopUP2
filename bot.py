import os
import logging

from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
WEBAPP_URL = os.getenv("WEBAPP_URL", "").strip()

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not WEBAPP_URL.startswith("https://"):
        await update.message.reply_text(
            "Mini App ещё не настроен: укажи HTTPS-ссылку в WEBAPP_URL."
        )
        return

    keyboard = [[
        KeyboardButton(
            text="💩 Открыть poopUP",
            web_app=WebAppInfo(url=WEBAPP_URL),
        )
    ]]
    await update.message.reply_text(
        "Добро пожаловать в poopUP! Открывай приложение кнопкой ниже.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            is_persistent=True,
        ),
    )


async def app_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not WEBAPP_URL.startswith("https://"):
        await update.message.reply_text("Сначала настрой HTTPS-ссылку WEBAPP_URL.")
        return
    await update.message.reply_text(
        f"Открой Mini App: {WEBAPP_URL}",
        disable_web_page_preview=True,
    )


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN в переменных окружения.")
    if not WEBAPP_URL.startswith("https://"):
        raise RuntimeError("WEBAPP_URL должен быть HTTPS-адресом опубликованного Mini App.")

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("app", app_command))
    logger.info("poopUP bot is running")
    application.run_polling()


if __name__ == "__main__":
    main()
