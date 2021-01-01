import telebot
import passwords
bot = telebot.TeleBot(passwords.key)
# bot.delete_webhook()

commands = {  # command description used in the "help" command
    'catalog'      : 'Каталог товаров 📦',
    'master_class' : 'Мастер-классы 👩‍🏫',
    'key '         : 'Информация о мастерской 📝',
    'help '       : 'Возврат к разделам 🏳️',
}


import os
from flask import Flask, request
import logging
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
server = Flask(__name__)
os.environ['FLASK_ENV'] = 'development'


@server.route('/' + passwords.key, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, str(message.from_user.first_name)+", тебя приветсвует мастерская " +
                "керамики CeramicsWithLove!")
    command_help(message)
    from functions import add_person
    add_person(message, bot)


@bot.message_handler(commands=['key'])
def get_text_messages(message):
    bot.send_message(message.chat.id, "Cейчас я расскажу тебе о нашей мастерской. Упс, мне пока"
                                      " нечего рассказать :( ")


@bot.message_handler(commands=['master_class'])
def master_class(message):
    from telebot import types
    button1 = types.InlineKeyboardButton(text="🎓 Записаться на мастер класс", callback_data="sign_up_master_class")
    button2 = types.InlineKeyboardButton(text="🔙  Назад", callback_data="menu")
    markup = types.InlineKeyboardMarkup()
    markup.row(button1)
    markup.row(button2)
    bot.send_message(message.chat.id, "Мастер-класс проходит в два дня.\nВ первый день 2,5-3 часа лепим\n" \
                                      "Попробуем <b>разные техники</b> ручной лепки🤲🏻\n"
                                      "Потом изделия сохнут и проходят первый обжиг\nИ затем мы "
                                      "<b>встречаемся ещё раз</b> и "
                                      "вы свои изделия покрываете цветными <b>глазурями</b>\nПотом изделия еще раз "
                                      "отправляются в печку \nИ вуаля! Можете их забирать :)\n"
                                      "<b>Получится 3-5 изделий</b> (в зависимости от сложности вашего запроса)"
                                      "\n1500₽ с человека за два дня\nГруппкам от 3 человек <b>скидка 20%</b>",
                     parse_mode='HTML', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "sign_up_master_class":
        from functions import sign_up_master_class
        sign_up_master_class(call.message, bot)
    if call.data == "menu":
        command_help(call.message)


@bot.message_handler(commands=['help'])
def command_help(message):
    """Вывод пользователю список команд"""
    cid = message.chat.id
    help_text = "Доступны следующие разделы:\n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


@bot.message_handler(commands=['catalog'])
def get_text_messageCatalog(message):
    """Импортируем типы из модуля, чтобы создавать кнопки"""
    from telebot import types
    markup = types.ReplyKeyboardMarkup(True, True)
    itembtn1 = types.KeyboardButton('Тарелки')
    itembtn2 = types.KeyboardButton('Вазы')
    itembtn3 = types.KeyboardButton('Кружки')
    itembtn4 = types.KeyboardButton('Прочее')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id,"Выбери интересующий раздел", reply_markup=markup)


@bot.message_handler(commands=['send_messageAnna'])
def send_message_to_all(message):
    from functions import send_to_all
    text = message.text[18:]    # Оставляем только текст после команды
    if text != '' and text != ' ':
        send_to_all(text, bot)


LIST_OF_COMMANDS = {'Плоские тарелки': 'Flat plates', 'Глубокие тарелки': 'Deep plates', 'Вазы': 'Vases',
                    'Кружки': 'Cups', 'Прочее': 'Other'}


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text in LIST_OF_COMMANDS:
        from functions import send
        send(message, LIST_OF_COMMANDS[message.text], bot)
    elif message.text == 'Тарелки':
        from telebot import types
        markup = types.ReplyKeyboardMarkup(True, True)
        itembtn1 = types.KeyboardButton('Плоские тарелки')
        itembtn2 = types.KeyboardButton('Глубокие тарелки')
        markup.add(itembtn1, itembtn2)
        bot.send_message(message.chat.id, "Выберите интересующий тип", reply_markup=markup)
    elif message.text == 'Вернуться в каталог':
        get_text_messageCatalog(message)
    elif message.text == 'Сделать заказ':
        from telebot import types
        markup = types.ReplyKeyboardMarkup(True, True, True)
        itembtn1 = types.KeyboardButton("Хочу чтобы со мной связались", request_contact = True)
        itembtn2 = types.KeyboardButton("Я сам напишу")
        markup.add(itembtn1, itembtn2)
        bot.send_message(message.chat.id, "Выбери способ заказа", reply_markup=markup)
    elif message.text == 'Я сам напишу':
        from telebot import types
        button1 = types.InlineKeyboardButton(text="Меню", callback_data="menu")
        markup = types.InlineKeyboardMarkup()
        markup.add(button1)
        bot.send_message(message.chat.id, 'Твое письмо уже ждут по адресу @annjuniper' + "\n"
                         + "Можешь в добавок просто переслать изделие которое понравилось",
                         reply_markup=markup)
    else: bot.send_message(message.chat.id, 'Я тебя не понимаю :(' + "\n" + "Воспользуйся командой /help")


@bot.message_handler(content_types=["contact"])
def save_contact(message):
    from telebot import types
    button1 = types.InlineKeyboardButton(text="Меню", callback_data="menu")
    markup = types.InlineKeyboardMarkup()
    markup.add(button1)
    bot.send_message(message.chat.id, "Поздравляю будущего владельца керамики! "
                                      "Ваш контакт отослан, скоро с вами свяжутся", reply_markup=markup)
    bot.send_message(108020326, "Аня! Поздравляю, поступил новый заказ от: " + str(message.contact))


# bot.polling(none_stop=False, interval=0, timeout=20)


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://telegrambot151.herokuapp.com/' + passwords.key)
    return "!", 200


server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
