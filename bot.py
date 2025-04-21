import os
import django
import nest_asyncio
import asyncio

# Указываем путь к settings.py твоего проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from museum.models import TelegramUser  # теперь можно импортировать!
from asgiref.sync import sync_to_async

# Разрешаем многократное использование цикла событий
nest_asyncio.apply()

# Обработчик контакта
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем контакт, который отправил пользователь
    contact = update.message.contact
    phone_number = contact.phone_number

    # Сохраняем контакт в базе данных (с проверкой или созданием нового пользователя)
    await sync_to_async(TelegramUser.objects.get_or_create)(
        phone=phone_number,
        defaults={'chat_id': update.effective_user.id}
    )

    # Отправляем сообщение с подтверждением
    await update.message.reply_text("✅ Спасибо! Ваш номер сохранён.")

# 📱 normalize_phone как у тебя
def normalize_phone(phone):
    phone = phone.strip()
    if not phone.startswith('+7'):
        phone = '+7' + phone.lstrip('7')
    return phone

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("📱 Отправить мой номер", request_contact=True)]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    # Отправляем сообщение с кнопкой для запроса контакта
    await update.message.reply_text("Привет! Отправь мне свой номер телефона:", reply_markup=markup)

# Запуск бота
async def main():
    TELEGRAM_TOKEN = '7734497840:AAGPU6V5_oaCJE4tUDEmjIgnRBnQ54SF-eU'

    # Строим приложение
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

    print("🚀 Бот запущен...")
    
    # Запускаем приложение в текущем цикле событий
    await app.run_polling()

# Если этот файл выполняется напрямую, запускаем основной цикл
if __name__ == '__main__':
    try:
        # Запуск бота с использованием уже работающего цикла событий
        asyncio.run(main())
    except Exception as e:
        print(f"Ошибка при запуске бота: {str(e)}")
