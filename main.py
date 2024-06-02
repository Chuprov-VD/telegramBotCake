import config
from datetime import *
import telebot
import sqlite3
from keyboard import *

bot = telebot.TeleBot(config.token)


# -------------------------------------- # START # -------------------------------------- #


@bot.message_handler(commands=['start'])
def start(message):
    connection = sqlite3.connect('users_data.db')
    cursor = connection.cursor()
    # Создаем таблицу Users (если ее нет)
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            name VARCHAR(50),
            last_name VARCHAR(50),
            numer_tel VARCHAR(30)
            )
            ''')
    # Сохраняем изменения
    connection.commit()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users_temp (
                id INTEGER PRIMARY KEY, 
                id_telegram VARCHAR(30),
                name VARCHAR(50),
                last_name VARCHAR(50),
                numer_tel VARCHAR(30)
                )
                ''')
    # Сохраняем изменения
    connection.commit()

    # Создаем таблицу Order (если ее нет)
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Order_price (
                    id INTEGER PRIMARY KEY,
                    datetime VARCHAR(30),
                    id_users INTEGER NOT NULL,
                    term_date VARCHAR(30),
                    time_date VARCHAR(30),
                    cake VARCHAR(50),
                    biscuit VARCHAR(50),
                    filling VARCHAR(50),
                    decor TEXT(100),
                    note TEXT(100),
                    units_sum VARCHAR(50),
                    payment VARCHAR(15),
                    transferred VARCHAR(15),
                    FOREIGN KEY (id_users) REFERENCES Users(id)
                    )
                    ''')
    # Сохраняем изменения и закрываем соединение
    connection.commit()

    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Order_price_temp (
                        id INTEGER PRIMARY KEY,
                        id_telegram VARCHAR(30),
                        id_users INTEGER,
                        term_date VARCHAR(30),
                        time_date VARCHAR(30),
                        cake VARCHAR(50),
                        biscuit VARCHAR(50),
                        filling VARCHAR(50),
                        decor TEXT(100),
                        note TEXT(100),
                        units_sum VARCHAR(50)
                        )
                        ''')
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()
    bot.send_message(
        message.chat.id, "Выберите, пожалуйста, действие: ",
        reply_markup=new_order_and_search())


@bot.callback_query_handler(func=lambda call: call.data == 'НовыйЗаказ')
def new_order(call):
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'INSERT INTO Order_price_temp (id_telegram) VALUES("{call.from_user.id}")'
    )
    connection.commit()
    connection.close()
    msg_user_name = bot.send_message(
        call.from_user.id, "Напишите пожалуйста номер телефона клиента: ")
    bot.register_next_step_handler(msg_user_name, user_name)


def user_name(message):
    tel = message.text
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'SELECT * FROM Users WHERE numer_tel = "{tel}"')
    data = cursor.fetchall()
    if data == list():
        bot.send_message(
            message.chat.id, "Такого номера нет! "
                             "Если желаете добавить клиента нажмите\n"
                             "/start -> Добавить клиента"
        )
    else:
        for i in data:
            id_user = i[0]
            name_user = i[1]
            lastname_user = i[2]
        connection.commit()
        cursor.execute(
            f'UPDATE Order_price_temp SET id_users = "{id_user}" WHERE id_telegram = "{message.from_user.id}"'
        )
        connection.commit()
        connection.close()
        bot.send_message(
            message.chat.id, f"Принято! Выбран {name_user} "
                             f"{lastname_user} \n"
                             f"Выберите наименование товара из прайса",
            reply_markup=price()
        )


@bot.callback_query_handler(func=lambda call:
                            call.data == 'БентоТорт' or
                            call.data == 'БисквитныйТорт' or
                            call.data == 'СвадебныйТорт' or
                            call.data == 'ТортЦифра' or
                            call.data == 'Капкейки' or
                            call.data == 'ДругойТовар'
                            )
def cake(call):
    cake_user = call.data
    id_user_telegram = call.from_user.id
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'UPDATE Order_price_temp SET cake = "{cake_user}" WHERE id_telegram = "{id_user_telegram}"'
    )
    connection.commit()
    connection.close()
    bot.send_message(
        call.from_user.id, "Выберите бисквит", reply_markup=biscuit()
    )


@bot.callback_query_handler(func=lambda call:
                            call.data == 'Эскимошки' or
                            call.data == 'Картошка')
def cake(call):
    cake_user = call.data
    id_user_telegram = call.from_user.id
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'UPDATE Order_price_temp SET cake = "{cake_user}" WHERE id_telegram = "{id_user_telegram}"'
    )
    connection.commit()
    connection.close()
    msg_decor = bot.send_message(
        call.from_user.id, "Принято! \nНапишите декор, если он есть")
    bot.register_next_step_handler(msg_decor, decor)


@bot.callback_query_handler(func=lambda call: call.data == 'Трайфлы')
def cake(call):
    cake_user = call.data
    id_user_telegram = call.from_user.id
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'UPDATE Order_price_temp SET cake = "{cake_user}" WHERE id_telegram = "{id_user_telegram}"'
    )
    connection.commit()
    connection.close()
    bot.send_message(
        call.from_user.id, "Выберите бисквит", reply_markup=biscuit_tr()
    )


@bot.callback_query_handler(func=lambda call:
                            call.data == 'ШоколадныйТр' or
                            call.data == 'ФисташковыйТр'
                            )
def cake(call):
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'UPDATE Order_price_temp SET biscuit = "{call.data}" WHERE id_telegram = "{call.from_user.id}"'
    )
    connection.commit()
    connection.close()
    msg_decor = bot.send_message(
        call.from_user.id, "Принято! \nНапишите декор, если он есть")
    bot.register_next_step_handler(msg_decor, decor)


@bot.callback_query_handler(func=lambda call:
                            call.data == 'Ванильный' or
                            call.data == 'Шоколадный' or
                            call.data == 'Фисташковый' or
                            call.data == 'Морковный' or
                            call.data == 'ДругойБисквит'
                            )
def cake(call):
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'UPDATE Order_price_temp SET biscuit = "{call.data}" WHERE id_telegram = "{call.from_user.id}"'
    )
    connection.commit()
    connection.close()
    bot.send_message(
        call.from_user.id, "Выберите начинку", reply_markup=filling()
    )


@bot.callback_query_handler(func=lambda call:
                            call.data == 'ДругаяНачинка' or
                            call.data == 'ВишневоеКонфи' or
                            call.data == 'КлубничноеКонфи' or
                            call.data == 'ЧернаяСмородина' or
                            call.data == 'МолочныйШоколад' or
                            call.data == 'МолочныйШоколадКриспи' or
                            call.data == 'СоленаяКарамельСАрахисом' or
                            call.data == 'СоленаяКарамельБезАрахиса'
                            )
def cake(call):
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'UPDATE Order_price_temp SET filling = "{call.data}" WHERE id_telegram = "{call.from_user.id}"'
    )
    connection.commit()
    connection.close()
    msg_decor = bot.send_message(
        call.from_user.id, "Принято! \nНапишите декор если он есть")
    bot.register_next_step_handler(msg_decor, decor)


def decor(message):
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'UPDATE Order_price_temp SET decor = "{message.text}" WHERE id_telegram = "{message.chat.id}"'
    )
    connection.commit()
    connection.close()
    msg_text_note = bot.send_message(
        message.chat.id, "Принято! \nДобавьте примечание!")
    bot.register_next_step_handler(msg_text_note, text_note)


def text_note(message):
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'UPDATE Order_price_temp SET note = "{message.text}" WHERE id_telegram = "{message.chat.id}"'
    )
    connection.commit()
    connection.close()
    msg_order_sum = bot.send_message(
        message.chat.id, "Принято! \nНапишите итоговую стоимость")
    bot.register_next_step_handler(msg_order_sum, order_sum)


def order_sum(message):
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'UPDATE Order_price_temp SET units_sum = "{message.text}" WHERE id_telegram = "{message.chat.id}"'
    )
    connection.commit()
    connection.close()
    msg_order_price = bot.send_message(
        message.chat.id, "Принято! \nНапишите дату окончания заказа в формате 00-00-0000(23-12-2024):  ")
    bot.register_next_step_handler(msg_order_price, order_time)


def order_time(message):
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'UPDATE Order_price_temp SET term_date = "{message.text}" WHERE id_telegram = "{message.chat.id}"'
    )
    connection.commit()
    connection.close()
    msg_order_price = bot.send_message(
        message.chat.id, "Принято! \nНапишите время передачи заказа в формате 00:00(18:00):  ")
    bot.register_next_step_handler(msg_order_price, order_term)


def order_term(message):
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'UPDATE Order_price_temp SET time_date = "{message.text}" WHERE id_telegram = "{message.chat.id}"'
    )
    connection.commit()
    connection.close()
    bot.send_message(
        message.chat.id, "Принято! Сохранить данные?\n Если нет, то нажмите /start", reply_markup=save()
    )


@bot.callback_query_handler(func=lambda call: call.data == 'ДаСохранить')
def user_add_order(call):
    current_date = str(datetime.now())
    date_var_new = current_date[8:10] + "-" + current_date[5:7] + "-" + current_date[0:4]
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'SELECT * FROM Order_price_temp WHERE id_telegram = "{call.from_user.id}" ORDER BY id DESC LIMIT 1'
    )
    data = cursor.fetchall()
    connection.commit()
    for i in data:
        id_user = i[2]
        date_order = i[3]
        time_d = i[4]
        cake = i[5]
        biscuit = i[6]
        filling = i[7]
        decor = i[8]
        text_note = i[9]
        sum_unit = i[10]
    cursor.execute(
        f'INSERT INTO Order_price (datetime, id_users, term_date, time_date, cake, biscuit, '
        f'filling, decor, note, units_sum,  payment, transferred) '
        
        f'VALUES("{date_var_new}", '
        f'"{id_user}", '
        f'"{date_order}", '
        f'"{time_d}", '
        f'"{cake}", '
        f'"{biscuit}", '
        f'"{filling}", '
        f'"{decor}", '
        f'"{text_note}", '
        f'"{sum_unit}", '
        f'"НетНеОплачен", '
        f'"НетНеОтдан")')
    connection.commit()
    connection.close()
    bot.send_message(call.from_user.id, "Заказ принят!")


# call Добавить клиента начало ------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == 'ДобавитьКлиента')
def hd(call):
    name_user = bot.send_message(
        call.from_user.id, "Напишите пожалуйста имя заказчика: ")
    bot.register_next_step_handler(name_user, user_name_add)


def user_name_add(message):
    name_user = message.text
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'INSERT INTO Users_temp (id_telegram, name) '
        f'VALUES ("{message.chat.id}" ,"{name_user}")')
    connection.commit()
    connection.close()
    user_lastname = bot.send_message(
        message.chat.id, f"Принято! \nНапишите фамилию или ник в телеграмм. ")
    bot.register_next_step_handler(user_lastname, user_lastname_add)


def user_lastname_add(message):
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'UPDATE Users_temp SET last_name = "{message.text}" '
        f'WHERE id_telegram = "{message.chat.id}" AND id = (SELECT MAX(id) FROM Users_temp )'
    )

    connection.commit()
    connection.close()
    user_number = bot.send_message(
        message.chat.id, f"Принято! \nНапишите номер телефона заказчика ")
    bot.register_next_step_handler(user_number, user_number_add)


def user_number_add(message):
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'UPDATE Users_temp SET numer_tel = "{message.text}" '
        f'WHERE id_telegram = "{message.chat.id}" AND id = (SELECT MAX(id) FROM Users_temp )'
    )
    connection.commit()
    cursor.execute(
        f'SELECT * FROM Users_temp WHERE id_telegram = "{message.chat.id}" ORDER BY id DESC LIMIT 1'
    )
    data = cursor.fetchall()
    connection.commit()
    for i in data:
        name = i[2]
        last_name = i[3]
        numer_tel = i[4]
    cursor.execute(
        f'INSERT INTO Users (name, last_name, numer_tel) '
        f'VALUES("{name}", "{last_name}", "{numer_tel}")'
    )
    connection.commit()
    connection.close()
    bot.send_message(
        message.chat.id, f"Клиент {name} {last_name} добавлен! Спасибо!")

# call Добавить клиента конец ------------------------------------------

# call Заказы начало ------------------------------------------


@bot.callback_query_handler(func=lambda call: call.data == 'Заказы')
def search(call):
    bot.send_message(
        call.from_user.id, "Выберите вариант: ", reply_markup=option()
    )


@bot.callback_query_handler(func=lambda call: call.data == 'ПоказатьВсеЗаказы')
def search(call):
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM Order_price, Users WHERE Users.id = Order_price.id_users"
    )
    data = cursor.fetchall()
    for i in data:
        bot.send_message(
            call.from_user.id, f"Номер заказа: {i[0]}\n"
                               f"ФИО заказчика: {i[14]} {i[15]}\n"
                               f"Дата заказа: {i[1]}\n"
                               f"Что заказал: {i[5]}\n"
                               f"Бисквит: {i[6]}\n"
                               f"Начинка: {i[7]}\n"
                               f"Декор: {i[8]}\n"
                               f"Примечание: {i[9]}\n"
                               f"Итоговая стоимость:  {i[10]}\n"
                               f"Заказ оплачен:  {i[11]}\n"
                               f"Заказ отдан:  {i[12]}\n"
                               f"Дата передачи заказа:  {i[3]}\n"
                               f"Время передачи заказа:  {i[4]}\n"

        )
    connection.commit()
    connection.close()


@bot.callback_query_handler(func=lambda call: call.data == 'ПоказатьЗаказыКлиента')
def new_order(call):
    msg_user_name = bot.send_message(
        call.from_user.id, "Напишите пожалуйста номер телефона клиента: ")
    bot.register_next_step_handler(msg_user_name, user_search)


def user_search(message):
    tel = message.text
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'SELECT id FROM Users WHERE numer_tel = "{tel}" ')
    data = cursor.fetchall()
    for i in data:
        id_users = i[0]
    cursor.execute(
        f'SELECT * FROM Order_price, Users WHERE id_users = {id_users} '
        f'AND Users.id = Order_price.id_users')
    data = cursor.fetchall()
    for i in data:
        bot.send_message(
            message.chat.id,   f"Номер заказа: {i[0]}\n"
                               f"ФИО заказчика: {i[14]} {i[15]}\n"
                               f"Дата заказа: {i[1]}\n"
                               f"Что заказал: {i[5]}\n"
                               f"Бисквит: {i[6]}\n"
                               f"Начинка: {i[7]}\n"
                               f"Декор: {i[8]}\n"
                               f"Примечание: {i[9]}\n"
                               f"Итоговая стоимость:  {i[10]}\n"
                               f"Заказ оплачен:  {i[11]}\n"
                               f"Заказ отдан:  {i[12]}\n"
                               f"Дата передачи заказа:  {i[3]}\n"
                               f"Время передачи заказа:  {i[4]}\n"

        )
    connection.commit()
    connection.close()


@bot.callback_query_handler(func=lambda call: call.data == 'ПоказатьЗаказыПоДате')
def new_order(call):
    msg_user_name = bot.send_message(
        call.from_user.id, "Напишите пожалуйста дату в формате 00-00-0000 (12-03-2024)")
    bot.register_next_step_handler(msg_user_name, user_date)


def user_date(message):
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f'SELECT * FROM Order_price, Users WHERE term_date = "{message.text}" '
        f'AND Users.id = Order_price.id_users')
    data = cursor.fetchall()
    for i in data:
        bot.send_message(
            message.chat.id,   f"Номер заказа: {i[0]}\n"
                               f"ФИО заказчика: {i[14]} {i[15]}\n"
                               f"Дата заказа: {i[1]}\n"
                               f"Что заказал: {i[5]}\n"
                               f"Бисквит: {i[6]}\n"
                               f"Начинка: {i[7]}\n"
                               f"Декор: {i[8]}\n"
                               f"Примечание: {i[9]}\n"
                               f"Итоговая стоимость:  {i[10]}\n"
                               f"Заказ оплачен:  {i[11]}\n"
                               f"Заказ отдан:  {i[12]}\n"
                               f"Дата передачи заказа:  {i[3]}\n"
                               f"Время передачи заказа:  {i[4]}\n"

        )
    connection.commit()
    connection.close()


@bot.callback_query_handler(func=lambda call:
                            call.data == 'ПоказатьВсеОтданныеЗаказы' or
                            call.data == 'ПоказатьВсеНеОтданныеЗаказы'
                            )
def search(call):
    if call.data == 'ПоказатьВсеОтданныеЗаказы':
        order_price = "ДаОтдан"
    elif call.data == 'ПоказатьВсеНеОтданныеЗаказы':
        order_price = "НетНеОтдан"
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT * FROM Order_price, Users WHERE transferred = '{order_price}'"
        f"AND Users.id = Order_price.id_users"
    )
    data = cursor.fetchall()
    for i in data:
        bot.send_message(
            call.from_user.id, f"Номер заказа: {i[0]}\n"
                               f"ФИО заказчика: {i[14]} {i[15]}\n"
                               f"Дата заказа: {i[1]}\n"
                               f"Что заказал: {i[5]}\n"
                               f"Бисквит: {i[6]}\n"
                               f"Начинка: {i[7]}\n"
                               f"Декор: {i[8]}\n"
                               f"Примечание: {i[9]}\n"
                               f"Итоговая стоимость:  {i[10]}\n"
                               f"Заказ оплачен:  {i[11]}\n"
                               f"Заказ отдан:  {i[12]}\n"
                               f"Дата передачи заказа:  {i[3]}\n"
                               f"Время передачи заказа:  {i[4]}\n"

        )
    connection.commit()
    connection.close()


@bot.callback_query_handler(func=lambda call:
                            call.data == 'ПоказатьВсеОплаченныеЗаказы' or
                            call.data == 'ПоказатьВсеНеОплаченныеЗаказы'
                            )
def search(call):
    if call.data == 'ПоказатьВсеОплаченныеЗаказы':
        order_price = "ДаОплачен"
    elif call.data == 'ПоказатьВсеНеОплаченныеЗаказы':
        order_price = "НетНеОплачен"
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT * FROM Order_price, Users WHERE Order_price.payment = '{order_price}'"
        f"AND Users.id = Order_price.id_users"
    )
    data = cursor.fetchall()
    for i in data:
        bot.send_message(
            call.from_user.id, f"Номер заказа: {i[0]}\n"
                               f"ФИО заказчика: {i[14]} {i[15]}\n" 
                               f"Дата заказа: {i[1]}\n" 
                               f"Что заказал: {i[5]}\n"
                               f"Бисквит: {i[6]}\n"
                               f"Начинка: {i[7]}\n"
                               f"Декор: {i[8]}\n" 
                               f"Примечание: {i[9]}\n"
                               f"Итоговая стоимость:  {i[10]}\n"
                               f"Заказ оплачен:  {i[11]}\n" 
                               f"Заказ отдан:  {i[12]}\n" 
                               f"Дата передачи заказа:  {i[3]}\n"
                               f"Время передачи заказа:  {i[4]}\n"

        )
    connection.commit()
    connection.close()


@bot.callback_query_handler(func=lambda call: call.data == 'ОплатитьЗаказ')
def search(call):
    user_payment = bot.send_message(
        call.from_user.id, "Напишите номер заказа: ")
    bot.register_next_step_handler(user_payment, user_payment_add)


def user_payment_add(message):
    order_price = "ДаОплачен"
    id_user = message.text
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f"UPDATE Order_price SET payment = 'ДаОплачен' WHERE id = {id_user} AND payment = 'НетНеОплачен'"
    )
    data = cursor.fetchall()
    connection.commit()
    cursor.execute(
        f"SELECT * FROM Order_price, Users WHERE Order_price.payment = '{order_price}'"
        f"AND Users.id = Order_price.id_users AND Order_price.id = {id_user}"
    )
    data = cursor.fetchall()

    if data == []:
        bot.send_message(message.chat.id, f"Заказ {id_user} не оплачен")

    else:
        bot.send_message(message.chat.id, f"Заказ {id_user} оплачен")
        for i in data:
            bot.send_message(
                message.chat.id,    f"Номер заказа: {i[0]}\n"
                                    f"ФИО заказчика: {i[14]} {i[15]}\n"
                                    f"Дата заказа: {i[1]}\n"
                                    f"Что заказал: {i[5]}\n"
                                    f"Бисквит: {i[6]}\n"
                                    f"Начинка: {i[7]}\n"
                                    f"Декор: {i[8]}\n"
                                    f"Примечание: {i[9]}\n"
                                    f"Итоговая стоимость:  {i[10]}\n"
                                    f"Заказ оплачен:  {i[11]}\n"
                                    f"Заказ отдан:  {i[12]}\n"
                                    f"Дата передачи заказа:  {i[3]}\n"
                                    f"Время передачи заказа:  {i[4]}\n"

            )
            connection.commit()
            connection.close()


@bot.callback_query_handler(func=lambda call: call.data == 'ОтдатьЗаказ')
def transferred(call):
    user_transferred = bot.send_message(
        call.from_user.id, "Напишите номер заказа: ")
    bot.register_next_step_handler(user_transferred, transferred_add)


def transferred_add(message):
    order_price = "ДаОтдан"
    id_user = message.text
    connection = sqlite3.connect("users_data.db")
    cursor = connection.cursor()
    cursor.execute(
        f"UPDATE Order_price SET transferred = 'ДаОтдан' WHERE id = {id_user} AND transferred = 'НетНеОтдан'"
    )
    data = cursor.fetchall()
    connection.commit()
    cursor.execute(
        f"SELECT * FROM Order_price, Users WHERE Order_price.transferred = '{order_price}'"
        f"AND Users.id = Order_price.id_users AND Order_price.id = {id_user}"
    )
    data = cursor.fetchall()

    bot.send_message(message.chat.id, f"Заказ {id_user} отдан")
    for i in data:
        bot.send_message(
            message.chat.id,   f"Номер заказа: {i[0]}\n"
                               f"ФИО заказчика: {i[14]} {i[15]}\n"
                               f"Дата заказа: {i[1]}\n"
                               f"Что заказал: {i[5]}\n"
                               f"Бисквит: {i[6]}\n"
                               f"Начинка: {i[7]}\n"
                               f"Декор: {i[8]}\n"
                               f"Примечание: {i[9]}\n"
                               f"Итоговая стоимость:  {i[10]}\n"
                               f"Заказ оплачен:  {i[11]}\n"
                               f"Заказ отдан:  {i[12]}\n"
                               f"Дата передачи заказа:  {i[3]}\n"
                               f"Время передачи заказа:  {i[4]}\n"

        )
        connection.commit()
        connection.close()


bot.infinity_polling()
