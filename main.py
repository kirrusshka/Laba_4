from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import requests

# Функция, которая обрабатывает команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Кнопки в inline-формате
    keyboard = [
        [InlineKeyboardButton("Список стран", callback_data='list_countries')],
        [InlineKeyboardButton("", callback_data='help')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Ответ с кнопками
    await update.message.reply_text(
        "Привет! Я могу предоставить информацию о любой стране. Выберите опцию ниже:",
        reply_markup=reply_markup
    )

# Функция для обработки команды /country
async def get_country_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Пожалуйста, укажите название страны после команды /country.")
        return

    country_name = " ".join(context.args)
    api_url = f"https://restcountries.com/v3.1/name/{country_name}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            country = data[0]
            name = country.get('name', {}).get('common', 'Unknown')
            capital = country.get('capital', ['Unknown'])[0]
            region = country.get('region', 'Unknown')
            population = country.get('population', 'Unknown')
            area = country.get('area', 'Unknown')

            message = (
                f"🌍 Информация о стране:\n"
                f"Название: {name}\n"
                f"Столица: {capital}\n"
                f"Регион: {region}\n"
                f"Население: {population}\n"
                f"Площадь: {area} км²"
            )
        else:
            message = "Не удалось найти информацию о данной стране. Проверьте название."
    except requests.exceptions.RequestException as e:
        message = f"Произошла ошибка при запросе API: {e}"

    await update.message.reply_text(message)

# Функция для обработки команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "Вот как использовать бота:\n\n"
        "1. Чтобы получить информацию о стране, отправьте команду: /country <название_страны>\n"
        "2. Вы также можете воспользоваться кнопкой 'Список стран' для получения подсказок.\n\n"
        "Чтобы вернуться в главное меню, используйте команду /start."
    )
    
    await update.message.reply_text(message)

# Функция обработки нажатий на кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Ответ на нажатие кнопки "Список стран"
    if query.data == 'list_countries':
        await query.edit_message_text(
            "Вы можете ввести команду /country <название_страны> для получения информации о стране.\n"
            "Чтобы вернуться, нажмите 'Назад'.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Назад", callback_data='back')]
            ])
        )
    # Ответ на нажатие кнопки "Команда /help"
    elif query.data == 'help':
        await query.edit_message_text(
            "Вот как использовать бота:\n\n"
            "1. Чтобы получить информацию о стране, отправьте команду: /country <название_страны>\n"
            "2. Вы также можете воспользоваться кнопкой 'Список стран' для получения подсказок.\n\n"
            "Чтобы вернуться, нажмите 'Назад'.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Назад", callback_data='back')]
            ])
        )
    # Ответ на нажатие кнопки "Назад"
    elif query.data == 'back':
        # Возвращаем пользователя в главное меню
        await query.edit_message_text(
            "Привет! Я могу предоставить информацию о любой стране. Выберите опцию ниже:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Список стран", callback_data='list_countries')],
                [InlineKeyboardButton("Подсказка", callback_data='help')]
            ])
        )

# Основная функция, которая настраивает бота
def main() -> None:
    application = Application.builder().token("7585280502:AAEMW9wBbBJ9E6C1PTB4bFvuj8_680Y9oLM").build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("country", get_country_info))
    application.add_handler(CommandHandler("help", help_command))  # Обработчик для команды /help
    application.add_handler(CallbackQueryHandler(button))  # Обработчик нажатий на кнопки

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
