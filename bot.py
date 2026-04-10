import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Бот подключен!\n"
        "Команды:\n"
        "/id — ID пользователя\n"
        "!ид — ID пользователя\n\n"
        "⚠️ Важно: в бизнес-чатах бот видит только сообщения собеседника!"
    )

async def get_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_id_info(update)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    
    if message_text == "!ид":
        await show_id_info(update)

async def show_id_info(update: Update):
    """Показывает информацию об ID"""
    chat_type = update.message.chat.type
    user = update.effective_user
    chat = update.effective_chat
    
    response = f"📊 **Информация:**\n"
    response += f"👤 Пользователь: {user.first_name}\n"
    response += f"🆔 ID пользователя: `{user.id}`\n"
    
    if user.username:
        response += f"📛 Username: @{user.username}\n"
    
    response += f"💬 ID чата: `{chat.id}`\n"
    response += f"📝 Тип чата: {chat_type}\n"
    
    # Если есть отвеченное сообщение
    if update.message.reply_to_message:
        reply_user = update.message.reply_to_message.from_user
        response += f"\n↩️ **Отвечено на сообщение:**\n"
        response += f"👤 {reply_user.first_name}\n"
        response += f"🆔 ID: `{reply_user.id}`"
    
    await update.message.reply_text(response, parse_mode="Markdown")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Error: {context.error}")

def main():
    if not TOKEN:
        logger.error("❌ BOT_TOKEN не найден!")
        return
    
    logger.info("🤖 Запуск бота...")
    
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
