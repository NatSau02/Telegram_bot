import dp as dp
import requests
import telebot
from telebot import types


bot = telebot.TeleBot("1744483561:AAGwpeLeGDWRlduqOUDpbYom9IMN4GCZ8DM")

name = ''
age = 0
surname = ''


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')


def get_name(message):  # получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    while age == 0:  # проверяем что возраст изменился
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    if age <= 20:
        question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
    elif age % 10 == 1:
        question = 'Тебе ' + str(age) + ' год, тебя зовут ' + name + ' ' + surname + '?'
    elif age % 10 > 1 and age % 10 < 5:
        question = 'Тебе ' + str(age) + ' годa, тебя зовут ' + name + ' ' + surname + '?'
    else:
        question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        file = open('im1.png', 'rb')
        bot.send_photo(call.message.chat.id, file)
        bot.send_message(call.message.chat.id, 'Запомню : )')
    elif call.data == "no":
        file = open('im2.png', 'rb')
        bot.send_photo(call.message.chat.id, file)
        bot.send_message(call.message.chat.id, 'Ну вот, ошибся : (')


bot.polling(none_stop=True)
