# Напишите программу, которая создает список, заполняет его случайными элементами, и сохраняет этот список в текстовом файле.

import telebot
import random
import os
from config import API_TOKEN

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Используйте команду /generate для создания списка случайных чисел или /view для просмотра сохраненных чисел.")

@bot.message_handler(commands=['generate'])
def generate_random_list(message):
    # Генерация списка случайных чисел
    length = random.randint(5, 15)  # Длина списка от 5 до 15
    random_list = [random.randint(1, 100) for _ in range(length)]  # Случайные числа от 1 до 100
    
    # Сохранение списка в файл
    file_path = 'random_list.txt'
    with open(file_path, 'w') as f:
        f.write(', '.join(map(str, random_list)))  # Запись списка в файл

    # Отправка файла пользователю
    with open(file_path, 'rb') as f:
        bot.send_document(message.chat.id, f)

@bot.message_handler(commands=['view'])
def view_random_list(message):
    file_path = 'random_list.txt'
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        bot.send_message(message.chat.id, f"Содержимое файла:\n{content}")
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл не найден. Пожалуйста, сначала создайте список с помощью команды /generate.")

@bot.message_handler(commands=['delete'])
def delete_file(message):
    file_path = 'random_list.txt'
    if os.path.exists(file_path):
        os.remove(file_path)
        bot.send_message(message.chat.id, "Файл успешно удален.")
    else:
        bot.send_message(message.chat.id, "Файл не найден.")

# Обработка ошибок
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я не понимаю. Пожалуйста, используйте команду /help для получения списка доступных команд.")

if __name__ == '__main__':
    bot.polling(none_stop=True)

