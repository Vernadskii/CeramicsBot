""" Модуль с отдельными функциями, выполняемыми в main"""


def send(message, nameCatalog, bot):
    """Функция отправки фотографий из Dropbox"""
    bot.send_message(message.chat.id, "Загружаю...")
    import requests
    import dropbox
    from passwords import ACESS_TOKEN
    dbx = dropbox.Dropbox(ACESS_TOKEN)
    for entry in dbx.files_list_folder('/' + nameCatalog).entries:
        # print(entry.name)
        # print(entry.name[-3::])
        if entry.name[-3::].lower() == 'jpg':
            # print('/' + nameCatalog + '/' + entry.name[:-3:] + "txt")
            link_photo = dbx.files_get_temporary_link(entry.path_lower).link
            try:
                link_descriprion = dbx.files_get_temporary_link('/' + nameCatalog + '/' + entry.name[:-3:] + "txt").link
                bot.send_photo(message.chat.id, link_photo, caption=requests.get(link_descriprion).content,
                               disable_notification=True)
            except Exception as ex:
                print('Не нашлось файла с описанием к фото')
    from telebot import types
    itembtn1 = types.KeyboardButton('Вернуться в каталог')
    itembtn2 = types.KeyboardButton('Сделать заказ')
    markup = types.ReplyKeyboardMarkup(True, True)
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Понравилось? Что будем делать?", reply_markup=markup)


def send_to_all(text, bot):
    """Функция отправки авторского сообщения всем пользователям"""
    import pymongo
    import passwords
    try:
        # ПОДКЛЮЧАЕМСЯ К MONGOCLIENT
        client = pymongo.MongoClient(passwords.mongodb_key)
        # ПОЛУЧАЕМ БАЗУ ДАННЫХ
        db = client['Project_for_messages_from_ceramic_bot']
        # ПОЛУЧАЕМ КОЛЛЕКЦИЮ
        collection = db["MainCluster"]
        from telebot import types
        button1 = types.InlineKeyboardButton(text="Меню", callback_data="menu")
        markup = types.InlineKeyboardMarkup()
        markup.add(button1)
        for instance in db.posts.find({}):
            try:
                bot.send_message(instance['message_chat_id'], text, reply_markup=markup)
            except:
                pass
    except Exception as ex:
        import logging
        logging.error("Ошибка отправки пользователям: " + str(ex))
        bot.send_message(108020326, "‼️ Ошибка отправки пользователям сообщения! :( ‼️")


def sign_up_master_class(message, bot):
    """Функция оповещения об отправке заявки на мастер класс"""
    from telebot import types
    button1 = types.InlineKeyboardButton(text="🔙 Меню", callback_data="menu")
    markup = types.InlineKeyboardMarkup()
    markup.row(button1)
    bot.send_message(message.chat.id, "Поздраляю, заявка на мастер класс отправлена, "
                                      "ожидайте ответа ☕", reply_markup=markup)
    bot.send_message(108020326, "Поздравляю, появился новый желающий принять участие в #мастер-классе.\n"
                                "Вот его контакты: @" + message.chat.username)


def add_person(message, bot):
    """ Функция добавления в бд нового пользователя"""

    import pymongo
    import passwords
    try:
        # ПОДКЛЮЧАЕМСЯ К MONGOCLIENT
        client = pymongo.MongoClient(passwords.mongodb_key)

        # ПОЛУЧАЕМ БАЗУ ДАННЫХ
        db = client['Project_for_messages_from_ceramic_bot']

        # ПОЛУЧАЕМ КОЛЛЕКЦИЮ
        collection = db["MainCluster"]

        if db.posts.find_one({"message_chat_id": message.chat.id}) is None:
            # Формируем текущюю дату
            from datetime import date
            import time
            time_first = date(time.localtime()[0], time.localtime()[1], time.localtime()[2])

            # ДОБАВЛЯЕМ В БД
            new_person = {"message_chat_id": message.chat.id,
                       "username": "@"+str(message.chat.username),
                       "time_of_first_using": str(time_first)}

            db.posts.insert_one(new_person)
            bot.send_message(108020326, "Аня! Поздравляю, ещё один новый человек воспользовался мною!\n"
                                        "Общее кол-во: " + str(db.posts.count_documents({})))
    except Exception as ex:
        import logging
        logging.error("Ошибка добавления в бд нового пользователя: " + str(ex))
        bot.send_message(108020326, "‼️Аня, Ошибка добавления в бд нового пользователя: " + str(ex) + " ‼️")
