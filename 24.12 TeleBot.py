import random

import requests
import telebot
from telebot import types

from bs4 import BeautifulSoup

bot = telebot.TeleBot('TOKEN')
url = 'https://xn--80af2bld5d.xn--p1ai/studlife/home/10565/'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    facts_lst = []
    facts_div = soup.find_all('div', class_='col col-mb-12 col-12')
    for fact in facts_div:
        for p in fact.find_all('p'):
            text = p.get_text(strip=True)

            if text and 'Факт' not in text:
                facts_lst.append(text)
# print(facts_lst)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Помощь', callback_data='help')
    button2 = types.InlineKeyboardButton('Об авторе', callback_data='about')
    button3 = types.InlineKeyboardButton('Интересный факт', callback_data='fact')

    keyboard.add(button1, button2, button3)
    bot.send_message(message.chat.id, 'Приветствую! Я просто реагирую на фото и голосовые сообщения. А еще могу прислать случайный интересный факт', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'help':
        bot.send_message(call.message.chat.id, 'Чтобы получить реакцию, пришли мне фото или же запиши голосовое сообщение')
    elif call.data == 'about':
        bot.send_message(call.message.chat.id, 'Создано в учебных целях. Автор @danna_s_o')
    elif call.data == 'fact':
        bot.send_message(call.message.chat.id, text=random.choice(facts_lst))

        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Да', callback_data='fact')
        button2 = types.InlineKeyboardButton('Нет', callback_data='end')

        keyboard.add(button1, button2)
        bot.send_message(call.message.chat.id, 'Хотите еще?', reply_markup=keyboard)

    elif call.data == 'end':
        bot.send_message(call.message.chat.id, 'Хорошо. Если понадоблюсь, можете вызвать через /start')


stickers_url = ['https://media.stickerswiki.app/myfavoritecats_by_fstikbot/70482.160.gif',
                'https://media.stickerswiki.app/stellarcats/1522762.160.gif',
                'https://media.stickerswiki.app/cgifs/62634.160.gif',
                'https://media.stickerswiki.app/cats2_libertarian/47874.160.gif',
                'https://media.stickerswiki.app/ktmrdogs2/1913412.160.gif',
                'https://media.stickerswiki.app/swinki1/2437827.160.gif',
                'https://media.stickerswiki.app/lolanimals2/134116.160.webp']


@bot.message_handler(content_types=['photo', 'voice'])
def handle_message(message):
    if message.photo:
        bot.send_sticker(message.chat.id, sticker=random.choice(stickers_url))

    elif message.voice:
        bot.send_message(message.chat.id, 'Спасибо за аудиосообщение! Хоть я его и не понимаю, но пришлите еще')



bot.polling()

