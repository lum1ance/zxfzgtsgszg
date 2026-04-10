import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

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
        "Доступные команды:\n"
        "/id — показать ваш Telegram ID\n"
        "!ид — тоже показать ID (альтернативная команда)"
    )

async def get_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /id — показывает ID пользователя"""
    await show_user_id(update)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик обычных сообщений"""
    message_text = update.message.text
    
    # Проверяем команду !ид
    if message_text == "!ид":
        await show_user_id(update)
    else:
        # Игнорируем другие сообщения (или можно добавить ответ)
        pass

async def show_user_id(update: Update):
    """Показывает ID пользователя"""
    user_id = update.effective_user.id
    username = update.effective_user.username
    first_name = update.effective_user.first_name
    
    response = f"🆔 Ваш Telegram ID: `{user_id}`"
    if username:
        response += f"\n📛 Username: @{username}"
    response += f"\n👤 Имя: {first_name}"
    
    await update.message.reply_text(response, parse_mode="Markdown")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(f"Exception while handling an update: {context.error}")

def main() -> None:
    """Запуск бота"""
    if not TOKEN:
        logger.error("❌ BOT_TOKEN не найден в переменных окружения!")
        return
    
    logger.info("🤖 Запуск бота...")
    
    try:
        # Создаём приложение
        application = Application.builder().token(TOKEN).build()
        
        # Регистрируем команды
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("id", get_id_command))  # латиница
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)
        
        logger.info("✅ Бот запущен и готов к работе!")
        
        # Запускаем polling
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")
        raise

if __name__ == "__main__":
    main()
