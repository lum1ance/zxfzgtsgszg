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

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Бот подключен к бизнес-аккаунту!\n"
        "Доступные команды в любом чате:\n"
        "/id — показать ID собеседника\n"
        "!ид — тоже показать ID"
    )

async def get_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_user_id(update)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    
    if message_text == "!ид":
        await show_user_id(update)

async def show_user_id(update: Update):
    user_id = update.effective_user.id
    username = update.effective_user.username
    first_name = update.effective_user.first_name
    
    # Если это бизнес-сообщение, показываем ID отправителя
    if update.message.sender_chat:
        # Сообщение от имени канала/группы
        sender_id = update.message.sender_chat.id
        response = f"🆔 ID отправителя: `{sender_id}`"
    else:
        # Обычное сообщение от пользователя
        response = f"🆔 Telegram ID: `{user_id}`"
        if username:
            response += f"\n📛 Username: @{username}"
        response += f"\n👤 Имя: {first_name}"
    
    # Доп. информация если есть
    if update.message.reply_to_message:
        reply_user = update.message.reply_to_message.from_user
        response += f"\n\n↩️ ID отвеченного: `{reply_user.id}`"
    
    await update.message.reply_text(response, parse_mode="Markdown")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Error: {context.error}")

def main():
    if not TOKEN:
        logger.error("❌ BOT_TOKEN не найден!")
        return
    
    logger.info("🤖 Запуск бота для Business...")
    
    try:
        application = Application.builder().token(TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("id", get_id_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)
        
        logger.info("✅ Бот запущен!")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        raise

if __name__ == "__main__":
    main()
