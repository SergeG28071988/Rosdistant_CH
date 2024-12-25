# Создайте базовый класс "Транспортное средство" с методами для вычисления максимальной скорости и вместимости. Затем создайте производные классы, представляющие разные виды транспорта (например, "Автомобиль" и "Самолет"), и реализуйте соответствующие методы для каждого виде транспорта.
import telebot
from telebot import types
from config import API_TOKEN
import os

# Базовый класс "Транспортное средство"
class Transport:
    def __init__(self, name, max_speed, capacity):
        self.name = name
        self.max_speed = max_speed  # Максимальная скорость
        self.capacity = capacity      # Вместимость

    def get_info(self):
        return f"{self.name}:\nМаксимальная скорость: {self.max_speed} км/ч\nВместимость: {self.capacity} человек"

# Класс-наследник для автомобилей
class Car(Transport):
    def __init__(self, name, max_speed, capacity):
        super().__init__(name, max_speed, capacity)

# Класс-наследник для самолётов
class Airplane(Transport):
    def __init__(self, name, max_speed, capacity):
        super().__init__(name, max_speed, capacity)

# Инициализация бота
bot = telebot.TeleBot(API_TOKEN)

# Функция для сохранения транспорта в файл
def save_transport(transport):
    with open('transports.txt', 'a') as f:
        f.write(f"{transport.__class__.__name__},{transport.name},{transport.max_speed},{transport.capacity}\n")

# Функция для загрузки транспорта из файла
def load_transports():
    transports = []
    if os.path.exists('transports.txt'):
        with open('transports.txt', 'r') as f:
            for line in f:
                transport_type, name, max_speed, capacity = line.strip().split(',')
                if transport_type == 'Car':
                    transports.append(Car(name, int(max_speed), int(capacity)))
                elif transport_type == 'Airplane':
                    transports.append(Airplane(name, int(max_speed), int(capacity)))
    return transports

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Используйте команды:\n/car - добавить автомобиль\n/airplane - добавить самолет\n/list - просмотреть список транспортных средств")

@bot.message_handler(commands=['car'])
def add_car(message):
    msg = bot.reply_to(message, "Введите название автомобиля, максимальную скорость и вместимость через запятую (например: 'Машина,200,5')")
    bot.register_next_step_handler(msg, process_car_info)

def process_car_info(message):
    try:
        name, max_speed, capacity = message.text.split(',')
        car = Car(name.strip(), int(max_speed.strip()), int(capacity.strip()))
        save_transport(car)
        bot.reply_to(message, f"Автомобиль '{car.name}' добавлен!")
    except Exception as e:
        bot.reply_to(message, "Ошибка! Пожалуйста, введите данные в правильном формате.")

@bot.message_handler(commands=['airplane'])
def add_airplane(message):
    msg = bot.reply_to(message, "Введите название самолета, максимальную скорость и вместимость через запятую (например: 'Самолет,900,180')")
    bot.register_next_step_handler(msg, process_airplane_info)

def process_airplane_info(message):
    try:
        name, max_speed, capacity = message.text.split(',')
        airplane = Airplane(name.strip(), int(max_speed.strip()), int(capacity.strip()))
        save_transport(airplane)
        bot.reply_to(message, f"Самолет '{airplane.name}' добавлен!")
    except Exception as e:
        bot.reply_to(message, "Ошибка! Пожалуйста, введите данные в правильном формате.")

@bot.message_handler(commands=['list'])
def list_transports(message):
    transports = load_transports()
    if transports:
        response = "Список транспортных средств:\n"
        for transport in transports:
            response += transport.get_info() + "\n\n"
    else:
        response = "Список транспортных средств пуст."
    bot.send_message(message.chat.id, response)

# Обработка ошибок
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я не понимаю. Пожалуйста, используйте команду /help для получения списка доступных команд.")

if __name__ == '__main__':
    bot.polling(none_stop=True)
