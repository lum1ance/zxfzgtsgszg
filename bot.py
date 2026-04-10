import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем токен из переменных окружения
TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветственное сообщение при /start"""
    await update.message.reply_text(
        "👋 Привет! Я бот для обработки личных сообщений.\n"
        "Доступная команда:\n"
        "!ид — показать ваш Telegram ID"
    )

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда !ид — показывает ID пользователя"""
    user_id = update.effective_user.id
    username = update.effective_user.username
    first_name = update.effective_user.first_name

    response = f"🆔 Ваш Telegram ID: `{user_id}`"
    if username:
        response += f"\n📛 Username: @{username}"
    response += f"\n👤 Имя: {first_name}"

    await update.message.reply_text(response, parse_mode="Markdown")

def main():
    """Запуск бота"""
    if not TOKEN:
        logger.error("❌ BOT_TOKEN не найден в переменных окружения!")
        return

    logger.info("🤖 Запуск бота...")

    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Регистрируем команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ид", get_id))  # команда /ид
    # Также можно использовать !ид через MessageHandler, но проще через /

    logger.info("✅ Бот запущен и готов к работе!")

    # Запускаем polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
