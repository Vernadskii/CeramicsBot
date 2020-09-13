from token import bot

commands = {  # command description used in the "help" command
    'start '       : 'Знакомство с ботом',
    'help '        : 'Информация о существующих командах',
    'key '         : 'Информация о мастерской',
    'catalog'      : 'Каталог товаров'
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, str(message.from_user.first_name)+", тебя приветсвует мастерская CeramicsWithLove "
                 + "чтобы посмотреть все команды нажми /help")

@bot.message_handler(commands=['key'])
def get_text_messages(message):
    bot.send_message(message.chat.id, "Cейчас я расскажу тебе о нашей мастерской ")

@bot.message_handler(commands=['help'])
def command_help(message):
    cid = message.chat.id
    help_text = "Доступны следующие команды \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page

@bot.message_handler(commands=['catalog'])
def get_text_messages(message):
    #bot.reply_to(message, "Выбери интересующий раздел")
    # Импортируем типы из модуля, чтобы создавать кнопки
    from telebot import types
    markup = types.ReplyKeyboardMarkup(True, True)
    itembtn1 = types.KeyboardButton('Тарелки')
    itembtn2 = types.KeyboardButton('Вазы')
    itembtn3 = types.KeyboardButton('Кружки')
    itembtn4 = types.KeyboardButton('Прочее')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id,"Выбери интересующий раздел", reply_markup=markup)

@bot.message_handler(regexp = 'Тарелки')
def plates(message):
    from telebot import types
    markup = types.ReplyKeyboardMarkup(True, True)
    itembtn1 = types.KeyboardButton('Плоские')
    itembtn2 = types.KeyboardButton('Глубокие')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Выбери интересующий тип", reply_markup=markup)
    @bot.message_handler(regexp='Плоские')
    def flat_plates(message):
        bot.send_message(message.chat.id, "Тут будут фото плоских тарелок")

@bot.message_handler(regexp = 'Вазы')
def vase(message):
    pass

@bot.message_handler(regexp = 'Кружки')
def cup(message):
    pass

@bot.message_handler(regexp = 'Прочее')
def other(message):
    pass



bot.polling(none_stop=False, interval=0, timeout=20)