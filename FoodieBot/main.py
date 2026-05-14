import telebot
from telebot import types
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import datetime

# Создаем папку для изображений, если ее нет
if not os.path.exists('images'):
    os.makedirs('images')

# Инициализация бота
bot = telebot.TeleBot('8710330600:AAHTtK3S0ZH0dQjRI9tTWLQgAWED0Pb9fvQ')  # замените на ваш токен

# Настройка базы данных для пользователей
engine_users = create_engine('sqlite:///users.db')
BaseUsers = declarative_base()

class User(BaseUsers):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)

# Модели для заказов и позиций заказов
class Order(BaseUsers):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    status = Column(String, default='Новый')
    total_price = Column(Integer)
    created_at = Column(String)

class OrderItem(BaseUsers):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    item_name = Column(String)
    quantity = Column(Integer)
    price = Column(Integer)

BaseUsers.metadata.create_all(engine_users)
SessionUsers = sessionmaker(bind=engine_users)
session_users = SessionUsers()

# Настройка базы данных для меню
engine_menu = create_engine('sqlite:///menu.db')
BaseMenu = declarative_base()

class MenuItem(BaseMenu):
    __tablename__ = 'menu_items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    photo_path = Column(String)

BaseMenu.metadata.create_all(engine_menu)
SessionMenu = sessionmaker(bind=engine_menu)
session_menu = SessionMenu()

# Временно храним корзины пользователей
user_carts = {}
# Словарь для хранения последних сообщений корзины для обновления
user_cart_messages = {}

# Загружаем меню из базы или создаем пример
def load_menu():
    items = session_menu.query(MenuItem).all()
    if not items:
        # Создаем примеры блюд
        item1 = MenuItem(name='Пицца Маргарита', price=250, photo_path='images/pizza_margarita.jpg')
        item2 = MenuItem(name='Бургер', price=150, photo_path='images/burger.jpg')
        item3 = MenuItem(name='Суши', price=300, photo_path='images/sushi.jpg')
        session_menu.add_all([item1, item2, item3])
        session_menu.commit()
        return {item.id: {'name': item.name, 'price': item.price, 'photo': item.photo_path} for item in [item1, item2, item3]}
    else:
        return {item.id: {'name': item.name, 'price': item.price, 'photo': item.photo_path} for item in items}

MENU = load_menu()

@bot.message_handler(commands=['start'])
def main(message):
    user_id = message.from_user.id
    user_in_db = session_users.query(User).filter_by(user_id=user_id).first()
    if not user_in_db:
        new_user = User(
            user_id=user_id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            phone=''
        )
        session_users.add(new_user)
        session_users.commit()
    # Формируем приветствие
    first_name = message.from_user.first_name or ''
    last_name = message.from_user.last_name or ''
    full_name = f"{first_name} {last_name}".strip()
    bot.send_message(user_id, f'Привет, {full_name}! Чтобы узнать подробности, напиши /help')

@bot.message_handler(commands=['help'])
def helper(message):
    bot.send_message(message.chat.id,
        "Привет! Я FoodieBot — помощник по заказу еды.\n"
        "Вот что я умею:\n"
        "• Просматривать меню (/rest)\n"
        "• Добавлять блюда в корзину\n"
        "• Просматривать корзину (/cart)\n"
        "• Редактировать корзину (/editcart)\n"
        "• Оформлять заказ (/order)\n"
        "• Отслеживать статус заказа\n"
        "• Предложить блюдо\n"
        "• Добавлять новое блюдо (/adddish)\n"
        "• Посмотреть историю заказов (/history)")

@bot.message_handler(commands=['rest'])
def show_rest_button(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("Ознакомиться с меню", callback_data="open")
    markup.row(btn)
    bot.send_message(message.chat.id, "Нажмите кнопку, чтобы просмотреть меню.", reply_markup=markup)

@bot.message_handler(commands=['cart'])
def show_cart_command(message):
    chat_id = message.chat.id
    show_or_update_cart(chat_id)

@bot.message_handler(commands=['editcart'])
def edit_cart_command(message):
    chat_id = message.chat.id
    show_edit_cart_menu(chat_id)

@bot.message_handler(commands=['order'])
def order_command(message):
    chat_id = message.chat.id
    show_or_update_cart(chat_id, show_order_button=True)

def show_or_update_cart(chat_id, show_order_button=False):
    cart = user_carts.get(chat_id, {})
    if not cart:
        bot.send_message(chat_id, "Ваша корзина пуста.")
        return
    total = 0
    msg_lines = ["Ваша корзина:"]
    for item_id, qty in cart.items():
        item = MENU[item_id]
        total += item['price'] * qty
        msg_lines.append(f"{item['name']} x{qty} - {item['price'] * qty} рублей")
    msg_lines.append(f"ИТОГО: {total} рублей")
    if show_order_button:
        markup = types.InlineKeyboardMarkup()
        btn_order = types.InlineKeyboardButton("Оформить заказ", callback_data="order_confirm")
        markup.row(btn_order)
        if chat_id in user_cart_messages:
            try:
                bot.edit_message_text("\n".join(msg_lines), chat_id, user_cart_messages[chat_id], reply_markup=markup)
            except:
                msg = bot.send_message(chat_id, "\n".join(msg_lines), reply_markup=markup)
                user_cart_messages[chat_id] = msg.message_id
        else:
            msg = bot.send_message(chat_id, "\n".join(msg_lines), reply_markup=markup)
            user_cart_messages[chat_id] = msg.message_id
    else:
        if chat_id in user_cart_messages:
            try:
                bot.edit_message_text("\n".join(msg_lines), chat_id, user_cart_messages[chat_id])
            except:
                msg = bot.send_message(chat_id, "\n".join(msg_lines))
                user_cart_messages[chat_id] = msg.message_id
        else:
            msg = bot.send_message(chat_id, "\n".join(msg_lines))
            user_cart_messages[chat_id] = msg.message_id

def show_food_menu(message):
    chat_id = message.chat.id
    for item_id, item in MENU.items():
        markup = types.InlineKeyboardMarkup()
        btn_add = types.InlineKeyboardButton("Добавить в корзину", callback_data=f'add_{item_id}')
        markup.row(btn_add)
        photo_path = item['photo']
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(
                    chat_id,
                    photo,
                    caption=f"{item['name']} - {item['price']} рублей",
                    reply_markup=markup
                )
        except:
            bot.send_message(
                chat_id,
                f"{item['name']} - {item['price']} рублей",
                reply_markup=markup
            )

def add_item_to_cart(callback):
    item_id = int(callback.data.split('_')[1])
    chat_id = callback.message.chat.id
    if chat_id not in user_carts:
        user_carts[chat_id] = {}
    user_carts[chat_id][item_id] = user_carts[chat_id].get(item_id, 0) + 1
    bot.answer_callback_query(callback.id, f"{MENU[item_id]['name']} добавлено в корзину.")
    show_or_update_cart(chat_id)

def show_edit_cart_menu(chat_id):
    cart = user_carts.get(chat_id, {})
    if not cart:
        bot.send_message(chat_id, "Ваша корзина пуста.")
        return
    for item_id, qty in cart.items():
        item = MENU[item_id]
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("+", callback_data=f'set_{item_id}_inc'),
            types.InlineKeyboardButton("-", callback_data=f'set_{item_id}_dec'),
            types.InlineKeyboardButton("Удалить", callback_data=f'remove_{item_id}')
        )
        bot.send_message(chat_id, f"{item['name']} x{qty}", reply_markup=markup)

def remove_item_from_cart(callback):
    item_id = int(callback.data.split('_')[1])
    chat_id = callback.message.chat.id
    if chat_id in user_carts and item_id in user_carts[chat_id]:
        del user_carts[chat_id][item_id]
        bot.answer_callback_query(callback.id, "Товар удален.")
        show_or_update_cart(chat_id)

def set_item_quantity(callback):
    chat_id = callback.message.chat.id
    data = callback.data.split('_')
    item_id = int(data[1])
    action = data[2]
    if chat_id not in user_carts:
        user_carts[chat_id] = {}
    if item_id not in user_carts[chat_id]:
        user_carts[chat_id][item_id] = 0
    if action == 'inc':
        user_carts[chat_id][item_id] += 1
    elif action == 'dec':
        user_carts[chat_id][item_id] -= 1
        if user_carts[chat_id][item_id] <= 0:
            del user_carts[chat_id][item_id]
    show_or_update_cart(chat_id)

def handle_order(callback):
    chat_id = callback.message.chat.id
    cart = user_carts.get(chat_id, {})
    if not cart:
        bot.answer_callback_query(callback.id, "Ваша корзина пуста.")
        return
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton('Отправить номер', request_contact=True))
    bot.send_message(chat_id, "Отправьте ваш номер телефона:", reply_markup=markup)
    bot.register_next_step_handler(callback.message, process_contact)

def process_contact(message):
    contact = None
    if message.contact:
        contact = message.contact.phone_number
    else:
        contact = message.text
    chat_id = message.chat.id
    user = session_users.query(User).filter_by(user_id=chat_id).first()
    if user:
        user.phone = contact
        session_users.commit()
    # Создаем заказ
    total_price = 0
    cart = user_carts.get(chat_id, {})
    for item_id, qty in cart.items():
        total_price += MENU[item_id]['price'] * qty

    new_order = Order(
        user_id=chat_id,
        status='Новый',
        total_price=total_price,
        created_at=str(datetime.datetime.now())
    )
    session_users.add(new_order)
    session_users.commit()

    order_id = new_order.id

    for item_id, qty in cart.items():
        item = MENU[item_id]
        order_item = OrderItem(
            order_id=order_id,
            item_name=item['name'],
            quantity=qty,
            price=item['price']
        )
        session_users.add(order_item)
    session_users.commit()

    user_carts.pop(chat_id, None)
    # Удаляем сообщение корзины
    if chat_id in user_cart_messages:
        try:
            bot.delete_message(chat_id, user_cart_messages[chat_id])
        except:
            pass
        del user_cart_messages[chat_id]

    bot.send_message(chat_id, f"Спасибо! Заказ №{order_id} оформлен.")

@bot.message_handler(commands=['adddish'])
def add_dish_command(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Введите название блюда:")
    bot.register_next_step_handler(msg, process_dish_name)

def process_dish_name(message):
    name = message.text
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Введите цену блюда (цифрой):")
    bot.register_next_step_handler(msg, process_dish_price, name)

def process_dish_price(message, name):
    try:
        price = int(message.text)
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, "Отправьте фотографию блюда:")
        bot.register_next_step_handler(msg, process_dish_photo, name, price)
    except:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректную цену.")

def process_dish_photo(message, name, price):
    if message.photo:
        photo_file_id = message.photo[-1].file_id
        file_info = bot.get_file(photo_file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        photo_path = f'images/{name}.jpg'
        with open(photo_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        new_item = MenuItem(name=name, price=price, photo_path=photo_path)
        session_menu.add(new_item)
        session_menu.commit()
        global MENU
        MENU = load_menu()
        bot.send_message(message.chat.id, f"Блюдо '{name}' успешно добавлено!")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, отправьте фотографию блюда.")

@bot.message_handler(commands=['history'])
def show_order_history(message):
    chat_id = message.chat.id
    orders = session_users.query(Order).filter_by(user_id=chat_id).order_by(Order.id.desc()).all()
    if not orders:
        bot.send_message(chat_id, "У вас пока нет заказов.")
        return
    for order in orders:
        try:
            dt = datetime.datetime.strptime(order.created_at, '%Y-%m-%d %H:%M:%S.%f')
        except:
            try:
                dt = datetime.datetime.strptime(order.created_at, '%Y-%m-%d %H:%M:%S')
            except:
                dt = None
        formatted_date = dt.strftime('%Y-%m-%d %H:%M') if dt else order.created_at
        msg = f"Заказ №{order.id} от {formatted_date}\nСтатус: {order.status}\nОбщая сумма: {order.total_price} рублей\n"
        items = session_users.query(OrderItem).filter_by(order_id=order.id).all()
        for item in items:
            msg += f"{item.item_name} x{item.quantity} - {item.price * item.quantity} рублей\n"
        bot.send_message(chat_id, msg)

# Обработка callback для редактирования корзины
@bot.callback_query_handler(func=lambda callback: True)
def callback_handler(callback):
    data = callback.data
    chat_id = callback.message.chat.id
    if data == 'open':
        show_food_menu(callback.message)
    elif data == 'check':
        show_or_update_cart(chat_id)
    elif data.startswith('add_'):
        add_item_to_cart(callback)
    elif data == 'order_confirm':
        handle_order(callback)
    elif data == 'edit_cart':
        show_edit_cart_menu(chat_id)
    elif data.startswith('remove_'):
        remove_item_from_cart(callback)
    elif data.startswith('set_'):
        set_item_quantity(callback)

# Запуск бота
bot.polling(none_stop=True)