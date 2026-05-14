import telebot
from telebot import types


bot = telebot.TeleBot('8710330600:AAHTtK3S0ZH0dQjRI9tTWLQgAWED0Pb9fvQ')

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}! Чтобы узнать подробности, напиши /help')


@bot.message_handler(commands=['rest'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Ознакомиться с меню", callback_data="open")
    btn2 = types.InlineKeyboardButton("Корзина", callback_data="check")
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton("Выбрать блюдо", callback_data="edit")
    btn3 = types.InlineKeyboardButton("Добавить своё блюдо", callback_data="send")
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, "Добро пожаловать, что вы хотите сделать?", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'edit':
        pass

    elif callback.data == "send":
        pass

    elif callback.data == "open":
        pass

    elif callback.data == "check":
        pass

@bot.message_handler(commands=['help'])
def helper(message):
    bot.send_message(message.chat.id,
        "Привет! Я FoodieBot — помощник по заказу еды.\n"
        "Вот что я умею:\n"
        "• Просматривать меню\n"
        "• Добавлять блюда в корзину\n"
        "• Просматривать и редактировать корзину\n"
        "• Оформлять заказ\n"
        "• Отслеживать статус заказа\n"
        "• Предложить блюдо\n")

bot.polling(none_stop=True)