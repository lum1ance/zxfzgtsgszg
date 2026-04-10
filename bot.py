import os
import logging
import signal
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN")

# Глобальная переменная для контроля состояния
application = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Бот подключен!\n"
        "Доступные команды:\n"
        "/id — показать ID\n"
        "!ид — показать ID\n\n"
        "ℹ️ В бизнес-чатах попросите собеседника написать команду"
    )

async def get_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_id_info(update)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    
    # Логируем входящие сообщения для отладки
    logger.info(f"Получено сообщение: '{message_text}' от {update.effective_user.first_name} в чате {update.effective_chat.id}")
    
    if message_text == "!ид":
        await show_id_info(update)

async def show_id_info(update: Update):
    """Показывает информацию об ID"""
    try:
        chat_type = update.message.chat.type
        user = update.effective_user
        chat = update.effective_chat
        
        response = f"📊 **Информация о пользователе:**\n"
        response += f"👤 Имя: {user.first_name}\n"
        response += f"🆔 User ID: `{user.id}`\n"
        
        if user.username:
            response += f"📛 Username: @{user.username}\n"
        
        response += f"\n💬 **Информация о чате:**\n"
        response += f"🆔 Chat ID: `{chat.id}`\n"
        response += f"📝 Тип чата: {chat_type}\n"
        
        # Если есть отвеченное сообщение
        if update.message.reply_to_message:
            reply_user = update.message.reply_to_message.from_user
            response += f"\n↩️ **Ответ на сообщение от:**\n"
            response += f"👤 {reply_user.first_name}\n"
            response += f"🆔 Reply User ID: `{reply_user.id}`"
        
        await update.message.reply_text(response, parse_mode="Markdown")
        logger.info(f"Отправлен ответ с ID пользователя {user.id}")
        
    except Exception as e:
        logger.error(f"Ошибка в show_id_info: {e}")
        await update.message.reply_text(f"❌ Произошла ошибка: {str(e)}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Error handling update: {context.error}")

def signal_handler(sig, frame):
    """Корректное завершение при сигнале"""
    logger.info("Получен сигнал завершения, останавливаем бота...")
    if application:
        application.stop()
    sys.exit(0)

def main():
    global application
    
    if not TOKEN:
        logger.error("❌ BOT_TOKEN не найден!")
        sys.exit(1)
    
    logger.info("🤖 Запуск бота...")
    
    # Регистрируем обработчики сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Создаём приложение с уникальным идентификатором
        application = Application.builder() \
            .token(TOKEN) \
            .concurrent_updates(True) \
            .build()
        
        # Регистрируем команды
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("id", get_id_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)
        
        logger.info("✅ Бот настроен, начинаем polling...")
        
        # Запускаем с drop_pending_updates чтобы игнорировать старые сообщения
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
            stop_signals=None  # Мы сами обрабатываем сигналы
        )
    
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
