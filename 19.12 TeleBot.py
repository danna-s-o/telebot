from mailbox import Message

import requests
import telebot
from telebot import types
from bs4 import BeautifulSoup


bot = telebot.TeleBot('7219412263:AAHJIiB7SgH0QM59_y8FtpxWOmH3cI4PJUE')

url = 'https://govzalla.com/%D0%BB%D0%B0%D0%BC%D0%B0%D0%B7%D0%B0%D0%BD-%D1%85%D0%B5%D0%BD%D0%B0%D1%88-%D0%B2%D1%80%D0%B5%D0%BC%D1%8F-%D0%BC%D0%BE%D0%BB%D0%B8%D1%82%D0%B2'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    time_of_namaz = {}
    blocks = soup.find_all('div', class_='col-6 col-md-4 col-lg-3 col-xl-2')
    if blocks:
        for block in blocks:
            time = block.find('h4')
            label = block.find('div', class_='label')
            time_of_namaz[label.text.strip()] = time.text.strip()
    # print(time_of_namaz)


@bot.message_handler(commands=['start'])
def start(message: Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bytton1 = types.KeyboardButton('Фаджр')
    bytton2 = types.KeyboardButton('Зухр')
    bytton3 = types.KeyboardButton('Аср')
    bytton4 = types.KeyboardButton('Магриб')
    bytton5 = types.KeyboardButton('Иша')
    keyboard.add(bytton1, bytton2, bytton3, bytton4, bytton5)
    bot.send_message(message.chat.id, 'Выберите намаз', reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def message_handler(message: Message):
    match message.text:
        case 'Фаджр':
            bot.reply_to(message, f'Время Фаджр намаза: {time_of_namaz['Фаджр']}')
        case 'Зухр':
            bot.reply_to(message, f'Время Зухр намаза: {time_of_namaz['Зухр']}')
        case 'Аср':
            bot.reply_to(message, f'Время Аср намаза: {time_of_namaz['Аср']}')
        case 'Магриб':
            bot.reply_to(message, f'Время Магриб намаза: {time_of_namaz['Магриб']}')
        case 'Иша':
            bot.reply_to(message, f'Время Иша намаза: {time_of_namaz['Иша']}')



bot.polling()