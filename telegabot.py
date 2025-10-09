import telebot
from telebot import types
from random import *
userdata={}
bot = telebot.TeleBot('8387480130:AAFnB0jD6xSvyowGlINLGNhfvjCmI7U2b30')
def init_user(chat_id):
    if chat_id not in userdata:
        userdata[chat_id] = {
            'waitingAnswerP': False,
            'waitingAnswerG': False,
            'start': True
        }
@bot.message_handler(commands=['start'])
def start(message):
    init_user(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Поздороваться👋")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "Здорова! ✨ От меня ты можешь получить как желания ✨, так и гнилания! 🤢\nТак же можешь добавить свои! 💥", reply_markup=markup)
 
@bot.message_handler(content_types=['text'])
def handle_text(message):
    init_user(message.chat.id)
    if userdata[message.chat.id]['waitingAnswerP']:
        with open('goodwords.txt', 'a', encoding='utf-8') as file:
            file.write(f'{message.text}\n')
        userdata[message.chat.id]['waitingAnswerP']=False
        userdata[message.chat.id]['start']=True
        bot.send_message(message.from_user.id, "Пожелание добавлено")
    if userdata[message.chat.id]['waitingAnswerG']:
        with open('badwords.txt', 'a', encoding='utf-8') as file:
            file.write(f'{message.text}\n')
        userdata[message.chat.id]['waitingAnswerG']=False
        userdata[message.chat.id]['start']=True
        bot.send_message(message.from_user.id, "Гнилание добавлено")
    if message.text == 'Поздороваться👋' or userdata[message.chat.id]['start'] or message.text == 'Вернуться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Пожелание 👼')
        btn2 = types.KeyboardButton('Гнилание 😈')
        btn3 = types.KeyboardButton('Добавить')
        markup.add(btn1,btn2,btn3)
        userdata[message.chat.id]['start']=False
        bot.send_message(message.from_user.id, "Выбери, что хочешь", reply_markup=markup)
    if message.text == 'Пожелание 👼':
        with open('goodwords.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            random_number = randint(0, len(lines)-1)  
        bot.send_message(message.from_user.id, lines[random_number])
    if message.text == 'Гнилание 😈':
        with open('badwords.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            random_number = randint(0, len(lines)-1)  

        bot.send_message(message.from_user.id, lines[random_number])
    if message.text == 'Добавить':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn4=types.KeyboardButton('Добавить пожелание 👼')
        btn5=types.KeyboardButton('Добавить гнилание 😈')
        markup.add(btn4,btn5)
        bot.send_message(message.from_user.id, "Выбери, что хочешь добавить", reply_markup=markup)
    if message.text == 'Добавить пожелание 👼':
        bot.send_message(message.from_user.id, "Напиши пожелание")
        userdata[message.chat.id]['waitingAnswerP']=True
    if message.text == 'Добавить гнилание 😈':
        bot.send_message(message.from_user.id, "Напиши гнилание")
        userdata[message.chat.id]['waitingAnswerG']=True
    
    
        

 

bot.polling(none_stop=True, interval=0)