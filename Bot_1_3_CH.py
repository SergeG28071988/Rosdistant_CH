# Напишите программу, которая запрашивает у пользователя два числа, затем предлагает пользователю выбрать операцию (сложение, вычитание, умножение или деление) и выводит результат выбранной операции.


from config import API_TOKEN
import telebot
from telebot import types

bot = telebot.TeleBot(API_TOKEN)

# Глобальный словарь для хранения пользовательских данных
user_data = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я калькулятор. Введите /calc для начала.")

@bot.message_handler(commands=['calc'])
def start_calculator(message):
    bot.send_message(message.from_user.id, "Введите первое число:")
    bot.register_next_step_handler(message, get_first_number)

def get_first_number(message):
    try:
        first_number = float(message.text)
        user_data[message.from_user.id] = {'first_number': first_number}  # Сохраняем первое число
        bot.send_message(message.from_user.id, "Введите второе число:")
        bot.register_next_step_handler(message, get_second_number)
    except ValueError:
        bot.send_message(message.from_user.id, "Пожалуйста, введите корректное число.")
        bot.register_next_step_handler(message, get_first_number)

def get_second_number(message):
    user_info = user_data.get(message.from_user.id)  # Получаем данные пользователя
    if not user_info:
        bot.send_message(message.from_user.id, "Ошибка: данные пользователя не найдены.")
        return

    try:
        second_number = float(message.text)
        
        # Предложение операций
        keyboard = types.InlineKeyboardMarkup()
        operations = ['Сложение', 'Вычитание', 'Умножение', 'Деление']
        
        for operation in operations:
            keyboard.add(types.InlineKeyboardButton(text=operation, callback_data=operation))
        
        bot.send_message(message.from_user.id, "Выберите операцию:", reply_markup=keyboard)
        
        # Сохраняем второе число для дальнейшего использования
        user_data[message.from_user.id]['second_number'] = second_number
        
    except ValueError:
        bot.send_message(message.from_user.id, "Пожалуйста, введите корректное число.")
        bot.register_next_step_handler(message, get_second_number)

@bot.callback_query_handler(func=lambda call: call.data in ['Сложение', 'Вычитание', 'Умножение', 'Деление'])
def perform_operation(call):
    user_info = user_data.get(call.from_user.id)  # Получаем данные пользователя
    if not user_info:
        bot.send_message(call.from_user.id, "Ошибка: данные пользователя не найдены.")
        return

    first_number = user_info['first_number']
    second_number = user_info['second_number']
    
    if call.data == 'Сложение':
        result = first_number + second_number
    elif call.data == 'Вычитание':
        result = first_number - second_number
    elif call.data == 'Умножение':
        result = first_number * second_number
    elif call.data == 'Деление':
        if second_number != 0:
            result = first_number / second_number
        else:
            bot.send_message(call.from_user.id, "Ошибка: Деление на ноль!")
            return
    
    bot.send_message(call.from_user.id, f"Результат {call.data}: {result}")

bot.infinity_polling(none_stop=True)

