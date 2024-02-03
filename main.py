import telebot
import config

from telebot import types
from api import get_exchangerate

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    help_button = types.KeyboardButton('🆘 Помощь')
    start_button = types.KeyboardButton('🌎 Посмотреть курс валют')
    exchange_button = types.KeyboardButton('🔄 Конвертировать валюту')
    keyboard.add(start_button, exchange_button, help_button)
    sticker = open('img/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id, f"Добро пожаловать, <b>{message.from_user.first_name}</b>! \n Я - <b>{bot.get_me().first_name}</b>, создан чтобы помочь узнать курсы валют!", parse_mode="html", reply_markup=keyboard)
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, 'Если у вас возникли какие-либо вопросы, обратитесь к администратору: @Mulpe')
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    if message.chat.type == 'private':
        if message.text == '🆘 Помощь' or message.text.lower() == 'помощь':
            bot.send_message(message.chat.id, 'Если у вас возникли какие-либо вопросы, обратитесь к администратору: @Mulpe')
            bot.delete_message(message.chat.id, message.message_id)
        elif message.text == '🌎 Посмотреть курс валют' or message.text.lower() == 'посмотреть курс валют':
            markup = types.InlineKeyboardMarkup()
            usd_to_rub_button = types.InlineKeyboardButton('USD/RUB', callback_data='USD to RUB')
            eur_to_rub_button = types.InlineKeyboardButton('EUR/RUB', callback_data='EUR to RUB')
            usd_to_eur_button = types.InlineKeyboardButton('USD/EUR', callback_data='USD to EUR')
            another_currency_button = types.InlineKeyboardButton('Ввести свои валюты', callback_data='Another')
            markup.add(usd_to_rub_button, eur_to_rub_button, usd_to_eur_button, another_currency_button)
            bot.send_message(message.chat.id, 'Выберите предложенные варианты', reply_markup=markup)
        elif message.text == '🔄 Конвертировать валюту' or message.text.lower() == 'конвертировать валюту':
            sent2 = bot.send_message(message.chat.id, 'Сначала введите валюту, которую надо конвертировать, затем валюту, в которую надо конвертировать и сумму.\n<b>Пример: USD RUB 100</b>', parse_mode='html')
            bot.register_next_step_handler(sent2, exchange)
        else:
            bot.send_message(message.chat.id, 'Я такой команды не знаю, вот список моих команд: /start, /help, Посмотреть курс валют.')


@bot.callback_query_handler(func=lambda call: call.data == 'USD to RUB')
def usd_to_rub(call):
    bot.send_message(call.message.chat.id, f'1 USD  ----->  {get_exchangerate('USD', 'RUB')} RUB')


@bot.callback_query_handler(func=lambda call: call.data == 'EUR to RUB')
def eur_to_rub(call):
    bot.send_message(call.message.chat.id, f'1 EUR  ----->  {get_exchangerate('EUR', 'RUB')} RUB')


@bot.callback_query_handler(func=lambda call: call.data == 'USD to EUR')
def usd_to_eur(call):
    bot.send_message(call.message.chat.id, f'1 USD  ----->  {get_exchangerate('USD', 'EUR')} EUR')


@bot.callback_query_handler(func=lambda call: call.data == 'Another')
def another_currency(call):
    sent = bot.send_message(call.message.chat.id, 'Введите свои валюты. <b>Пример: USD RUB</b>\n<b>Внимание❗</b> Названия валют должны быть записаны в виде аббревиатуры валют (USD, RUB, EUR, CNY и т.д.)', parse_mode='html')
    bot.register_next_step_handler(sent, reply_to_value)


def reply_to_value(message):
    banknotes = message.text
    banknotes_list = banknotes.split()
    bot.send_message(message.chat.id, f'1 {banknotes_list[0]}  ----->  {get_exchangerate(banknotes_list[0], banknotes_list[1])} {banknotes_list[1]}')


def exchange(message):
    banknotes_and_amount = message.text
    banknotes_and_amount_list = banknotes_and_amount.split()
    currency = get_exchangerate(banknotes_and_amount_list[0], banknotes_and_amount_list[1])
    res = currency * int(banknotes_and_amount_list[2])
    bot.send_message(message.chat.id, f'{banknotes_and_amount_list[2]} {banknotes_and_amount_list[0]}  ----->  {res} {banknotes_and_amount_list[1]}')


bot.polling(none_stop=True)
