import telebot
from telebot import types
from random import *
import os
import requests
import json
from time import *
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

token= os.getenv('TOKEN')
bot = telebot.TeleBot(token)
POPULAR_COINS = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum', 
    'SOL': 'solana',
    'DOGE': 'dogecoin'
}
STATES = {
    'MAIN_MENU': 0,
    'ADD_COIN_SELECT': 1,
    'ADD_QUANTITY': 2, 
    'ADD_PRICE': 3,
    'VIEW_PORTFOLIO': 4,
    'DELETE_COIN': 5
}
temp_dict={}
user_states={}
user_temp_data={}
cash_price={}
def get_user_state(chat_id):
    return user_states.get(chat_id, STATES['MAIN_MENU'])
@bot.message_handler(commands=['start'])
def start(message):
    user_states[message.chat.id] = STATES['MAIN_MENU']
    show_main_menu(message.chat.id)
def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('📥 Добавить покупку')
    btn2 = types.KeyboardButton('📊 Мой портфель')
    btn3 = types.KeyboardButton('❌ Удалить запись')
    markup.add(btn1, btn2)
    markup.add(btn3)
    bot.send_message(chat_id, "💰 Привет! Я крипти, давай работать вместе", reply_markup=markup)

@bot.message_handler(func=lambda message: get_user_state(message.chat.id) == STATES['MAIN_MENU'])
def handle_main_menu(message):
    if message.text == '📥 Добавить покупку':
        show_coin_selection(message.chat.id)
    elif message.text == '📊 Мой портфель':
        show_portfolio(message.chat.id)
    elif message.text == '❌ Удалить запись':
        show_delete_options(message.chat.id)

def show_coin_selection(chat_id):
    user_states[chat_id] = STATES['ADD_COIN_SELECT']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    port=get_user_portfolio(chat_id)
    for symbol in POPULAR_COINS.keys():
        markup.add(types.KeyboardButton(symbol))
    for key, value in port.items():
        if key not in POPULAR_COINS.values():
            markup.add(types.KeyboardButton(key.upper()))
            temp_dict[key.upper()]=key

    markup.add(types.KeyboardButton('🔙 Назад'))
    
    bot.send_message(
        chat_id,
        "Выбери криптовалюту или напиши её название (например: bitcoin):",
        reply_markup=markup
    )
@bot.message_handler(func=lambda message: get_user_state(message.chat.id) == STATES['ADD_COIN_SELECT'])
def handle_coin_selection(message):
    chat_id = message.chat.id
    
    if message.text == '🔙 Назад':
        user_states[chat_id] = STATES['MAIN_MENU']
        show_main_menu(chat_id)
        return
    
    coin_id = None
    if message.text in POPULAR_COINS:
        coin_id = POPULAR_COINS[message.text]
    elif message.text in temp_dict:
        coin_id = temp_dict[message.text]
        temp_dict.clear()
    else:
        coin_id = message.text.lower()
    
    if not check_coin_exists(coin_id):
        bot.send_message(chat_id, "❌ Монета не найдена. Проверь название и попробуй снова.")
        return
    
    if chat_id not in user_temp_data:
        user_temp_data[chat_id] = {}
    user_temp_data[chat_id]['coin_id'] = coin_id
    user_temp_data[chat_id]['coin_symbol'] = message.text
    
    user_states[chat_id] = STATES['ADD_QUANTITY']
    bot.send_message(
        chat_id,
        f"Введи количество {message.text} которое ты купил:",
        reply_markup=types.ReplyKeyboardRemove()
    )
@bot.message_handler(func=lambda message: get_user_state(message.chat.id) == STATES['ADD_QUANTITY'])
def handle_quantity_input(message):
    chat_id = message.chat.id
    
    try:
        quantity = float(message.text)
        if quantity <= 0:
            raise ValueError
        
        user_temp_data[chat_id]['quantity'] = quantity
        user_states[chat_id] = STATES['ADD_PRICE']
        
        bot.send_message(
            chat_id,
            f"Введи цену покупки за 1 {user_temp_data[chat_id]['coin_symbol']} (в USD):"
        )
        
    except ValueError:
        bot.send_message(chat_id, "❌ Введи корректное число (например: 0.5 или 100)")

@bot.message_handler(func=lambda message: get_user_state(message.chat.id) == STATES['ADD_PRICE'])
def handle_price_input(message):
    chat_id = message.chat.id
    
    try:
        price = float(message.text)
        if price <= 0:
            raise ValueError
        
        save_purchase(chat_id, user_temp_data[chat_id]['coin_id'], 
                     user_temp_data[chat_id]['quantity'], price)
        
        
        user_states[chat_id] = STATES['MAIN_MENU']
        
        bot.send_message(
            chat_id,
            f"✅ Покупка сохранена!\n"
            f"Монета: {user_temp_data[chat_id]['coin_symbol']}\n"
            f"Количество: {user_temp_data[chat_id]['quantity']}\n"
            f"Цена: ${price:.2f}",
            reply_markup=types.ReplyKeyboardRemove()
        )
        user_temp_data.pop(chat_id, None)
        show_main_menu(chat_id)
        
    except ValueError:
        bot.send_message(chat_id, "❌ Введи корректную цену (например: 45000.50)")

def show_portfolio(chat_id):
    portfolio = get_user_portfolio(chat_id)
    
    if not portfolio:
        bot.send_message(chat_id, "📭 Твой портфель пуст. Добавь первую покупку!")
        return
    
    total_invested = 0
    total_current = 0
    portfolio_text = "📊 <b>Твой портфель:</b>\n\n"
    
    for coin_id, purchases in portfolio.items():
        total_quantity = sum(p['quantity'] for p in purchases)
        total_invested_coin = sum(p['quantity'] * p['buy_price'] for p in purchases)
        
        current_price = get_current_price(coin_id)
        print(current_price)
        if current_price:
            current_value = total_quantity * current_price
            profit = current_value - total_invested_coin
            profit_percent = (profit / total_invested_coin) * 100
            
            portfolio_text += (
                f"<b>{coin_id.upper()}</b>\n"
                f"Количество: {total_quantity:.6f}\n"
                f"Средняя цена: ${total_invested_coin/total_quantity:.2f}\n"
                f"Текущая цена: ${current_price:.2f}\n"
                f"Инвестировано: ${total_invested_coin:.2f}\n"
                f"Текущая стоимость: ${current_value:.2f}\n"
                f"P&L: ${profit:.2f} ({profit_percent:+.2f}%)\n\n"
            )
            
            total_invested += total_invested_coin
            total_current += current_value
        else:
            portfolio_text += "⚠️ Не удалось получить текущую цену.\n\n"
    
    if total_invested > 0:
        total_profit = total_current - total_invested
        total_profit_percent = (total_profit / total_invested) * 100
        
        portfolio_text += (
            f"<b>Итого:</b>\n"
            f"Общие инвестиции: ${total_invested:.2f}\n"
            f"Текущая стоимость: ${total_current:.2f}\n"
            f"Общий P&L: ${total_profit:.2f} ({total_profit_percent:+.2f}%)"
        )
    
    bot.send_message(chat_id, portfolio_text, parse_mode='HTML')
def show_delete_options(chat_id):
    portfolio = get_user_portfolio(chat_id)
    
    if not portfolio:
        bot.send_message(chat_id, "📭 Твой портфель пуст. Нечего удалять!")
        return
    
    user_states[chat_id] = STATES['DELETE_COIN']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    for coin_id in portfolio.keys():
        markup.add(types.KeyboardButton(coin_id.upper()))
    
    markup.add(types.KeyboardButton('🔙 Назад'))
    
    bot.send_message(
        chat_id,
        "Выбери монету, записи о которой хочешь удалить:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: get_user_state(message.chat.id) == STATES['DELETE_COIN'])
def handle_delete_selection(message):
    chat_id = message.chat.id
    
    if message.text == '🔙 Назад':
        user_states[chat_id] = STATES['MAIN_MENU']
        show_main_menu(chat_id)
        return
    
    coin_id = message.text.lower()
    portfolio = get_user_portfolio(chat_id)
    
    if coin_id not in portfolio:
        bot.send_message(chat_id, "❌ У тебя нет записей об этой монете.")
        return
 
    delete_coin_records(chat_id, coin_id)
    user_states[chat_id] = STATES['MAIN_MENU']
    
    bot.send_message(
        chat_id,
        f"✅ Все записи о {coin_id.upper()} удалены!",
        reply_markup=types.ReplyKeyboardRemove()
    )
    show_main_menu(chat_id)


def check_coin_exists(coin_id):
    """Проверяет существование монеты через API"""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {'ids': coin_id, 'vs_currencies': 'usd'}
        response = requests.get(url, params=params)
        return coin_id in response.json()
    except:
        return False

def get_current_price(coin_id):
    now = time()
    try:
        if str(coin_id) not in cash_price:
            cash_price[str(coin_id)]={}
            
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {'ids': coin_id, 'vs_currencies': 'usd'}
            response = requests.get(url, params=params)
            cash_price[str(coin_id)]['price']=response.json()[coin_id]['usd']
            cash_price[str(coin_id)]['time']=now
            return response.json()[coin_id]['usd']
        else:
            if now-cash_price[str(coin_id)]['time']>30:
                url = "https://api.coingecko.com/api/v3/simple/price"
                params = {'ids': coin_id, 'vs_currencies': 'usd'}
                response = requests.get(url, params=params)
                cash_price[str(coin_id)]['price']=response.json()[coin_id]['usd']
                cash_price[str(coin_id)]['time']=now
                return response.json()[coin_id]['usd']
            else:
                return cash_price[str(coin_id)]['price']
    except:
        return None

def save_purchase(user_id, coin_id, quantity, price):
    try:
        with open('crypto_portfolio.json', 'r') as f:
            data = json.load(f)
    except:
        data = {}
    
    if str(user_id) not in data:
        data[str(user_id)] = {}
    
    if coin_id not in data[str(user_id)]:
        data[str(user_id)][coin_id] = []
    
    data[str(user_id)][coin_id].append({
        'quantity': quantity,
        'buy_price': price,
        'date': datetime.now().isoformat()
    })
    
    with open('crypto_portfolio.json', 'w') as f:
        json.dump(data, f, indent=2)

def get_user_portfolio(user_id):
    try:
        with open('crypto_portfolio.json', 'r') as f:
            data = json.load(f)
        return data.get(str(user_id), {})
    except:
        return {}

def delete_coin_records(user_id, coin_id):
    try:
        with open('crypto_portfolio.json', 'r') as f:
            data = json.load(f)
        
        if str(user_id) in data and coin_id in data[str(user_id)]:
            del data[str(user_id)][coin_id]
            
            if not data[str(user_id)]:
                del data[str(user_id)]
            
            with open('crypto_portfolio.json', 'w') as f:
                json.dump(data, f, indent=2)
            return True
    except:
        pass
    return False


@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    if message.chat.id not in user_states:
        bot.send_message(message.chat.id, "Введи /start чтобы начать")


if __name__ == "__main__":
    print("Бот запущен")
    bot.polling(none_stop=True)