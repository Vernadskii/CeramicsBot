def send(message, nameCatalog):
    bot.send_message(message.chat.id, "Загружаю...")
    import googleCloud
    output = googleCloud.listOfLinks(nameCatalog)
    for i in output:
        bot.send_photo(message.chat.id,
                       i[0], i[1], None, None, None, True)
    from telebot import types
    itembtn1 = types.KeyboardButton('Вернуться в каталог')
    itembtn2 = types.KeyboardButton('Сделать заказ')
    markup = types.ReplyKeyboardMarkup(True, True)
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Понравилось? Что будем делать?", reply_markup=markup)

import telebot
import passwords
bot = telebot.TeleBot(passwords.key)

commands = {  # command description used in the "help" command
    'key '         : 'Информация о мастерской',
    'catalog'      : 'Каталог товаров',
    'help '        : 'Информация о существующих командах',
    'start '       : 'Знакомство с ботом'
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, str(message.from_user.first_name)+", тебя приветсвует мастерская керамики CeramicsWithLove, "
                 + "чтобы посмотреть все команды нажми /help")

@bot.message_handler(commands=['key'])
def get_text_messages(message):
    bot.send_message(message.chat.id, "Cейчас я расскажу тебе о нашей мастерской. Упс, мне пока"
                                      " нечего рассказать :( ")

@bot.message_handler(commands=['help'])
def command_help(message):
    cid = message.chat.id
    help_text = "Доступны следующие команды \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page

@bot.message_handler(commands=['catalog'])
def get_text_messageCatalog(message):
    # Импортируем типы из модуля, чтобы создавать кнопки
    from telebot import types
    markup = types.ReplyKeyboardMarkup(True, True)
    itembtn1 = types.KeyboardButton('Тарелки')
    itembtn2 = types.KeyboardButton('Вазы')
    itembtn3 = types.KeyboardButton('Кружки')
    itembtn4 = types.KeyboardButton('Прочее')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id,"Выбери интересующий раздел", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def hangle_text(message):
    if message.text == 'Тарелки':
        from telebot import types
        markup = types.ReplyKeyboardMarkup(True, True)
        itembtn1 = types.KeyboardButton('Плоские тарелки')
        itembtn2 = types.KeyboardButton('Глубокие тарелки')
        markup.add(itembtn1, itembtn2)
        bot.send_message(message.chat.id, "Выбери интересующий тип", reply_markup=markup)
    if message.text == 'Плоские тарелки':
        send(message, 'Flat plates')
    elif message.text == 'Глубокие тарелки':
        send(message, 'Deep plates')
    elif message.text == 'Вазы':
        send(message, 'Vases')
    elif message.text == 'Кружки':
        send(message, 'Cups')
    elif message.text == 'Прочее':
        send(message, 'Other')
    elif message.text == 'Вернуться в каталог':
        get_text_messageCatalog(message)
    elif message.text == 'Сделать заказ':
        from telebot import types
        markup = types.ReplyKeyboardMarkup(True, True)
        itembtn1 = types.KeyboardButton("Хочу чтобы со мной связались", True)
        itembtn2 = types.KeyboardButton("Я сам напишу")
        markup.add(itembtn1, itembtn2)
        bot.send_message(message.chat.id, "Выбери способ заказа", reply_markup=markup)
    elif message.text == 'Я сам напишу':
        bot.send_message(message.chat.id, 'Твое письмо уже ждут по адресу @annjuniper')


@bot.message_handler(content_types=["contact"])
def save_contact(message):
    from telebot import types
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Поздравляю будущего владельца керамики! Ваш контакт отослан, скоро с вами свяжутся", reply_markup=markup)
    bot.send_message(108020326, "Аня! Поздравляю, поступил новый заказ от: " + str(message.contact))



bot.polling(none_stop=False, interval=0, timeout=20)