from telebot import types


def new_order_and_search():
    keyboard = types.InlineKeyboardMarkup()
    new_order = types.InlineKeyboardButton(text="Новый заказ", callback_data="НовыйЗаказ")
    add_client = types.InlineKeyboardButton(text="Добавить клиента", callback_data="ДобавитьКлиента")
    order = types.InlineKeyboardButton(text="Отдать заказ", callback_data="ОтдатьЗаказ")
    paid = types.InlineKeyboardButton(text="Оплатить заказ", callback_data="ОплатитьЗаказ")
    all_orders = types.InlineKeyboardButton(text="Заказы", callback_data="Заказы")
    keyboard.row(new_order)
    keyboard.row(add_client)
    keyboard.row(order)
    keyboard.row(paid)
    keyboard.row(all_orders)
    return keyboard


def price():
    keyboard = types.InlineKeyboardMarkup()
    bento_cake = types.InlineKeyboardButton(text="Бенто торт", callback_data="БентоТорт")
    sponge_cakes = types.InlineKeyboardButton(text="Бисквитный торт", callback_data="БисквитныйТорт")
    wedding_cake = types.InlineKeyboardButton(text="Свадебный торт", callback_data="СвадебныйТорт")
    figure_cake = types.InlineKeyboardButton(text="Торт цифра", callback_data="ТортЦифра")
    trifles = types.InlineKeyboardButton(text="Трайфлы", callback_data="Трайфлы")
    cupcakes = types.InlineKeyboardButton(text="Капкейки", callback_data="Капкейки")
    eskimos = types.InlineKeyboardButton(text="Эскимошки", callback_data="Эскимошки")
    potato = types.InlineKeyboardButton(text="Картошка", callback_data="Картошка")
    order = types.InlineKeyboardButton(text="Другое", callback_data="ДругойТовар")
    keyboard.row(bento_cake, sponge_cakes)
    keyboard.row(wedding_cake, figure_cake)
    keyboard.row(trifles, cupcakes)
    keyboard.row(eskimos, potato)
    keyboard.row(order)
    return keyboard


def filling():
    keyboard = types.InlineKeyboardMarkup()
    сherry_confit = types.InlineKeyboardButton(text="Вишневое конфи", callback_data="ВишневоеКонфи")
    strawberry_confit = types.InlineKeyboardButton(text="Клубничное конфи", callback_data="КлубничноеКонфи")
    blackcurrant_confit = types.InlineKeyboardButton(text="Конфи из черной смородины", callback_data="ЧернаяСмородина")
    milk_chocolate = types.InlineKeyboardButton(text="Молочный шоколад", callback_data="МолочныйШоколад")
    milk_chocolate_crispy = types.InlineKeyboardButton(text="Молочный шоколад + криспи",
                                                       callback_data="МолочныйШоколадКриспи")
    salted_caramel_ar = types.InlineKeyboardButton(text="Соленая карамель с арахисом",
                                                   callback_data="СоленаяКарамельСАрахисом")
    salted_caramel = types.InlineKeyboardButton(text="Соленая карамель без арахиса",
                                                callback_data="СоленаяКарамельБезАрахиса")
    order = types.InlineKeyboardButton(text="Другое", callback_data="ДругаяНачинка")
    keyboard.row(сherry_confit)
    keyboard.row(strawberry_confit)
    keyboard.row(blackcurrant_confit)
    keyboard.row(milk_chocolate)
    keyboard.row(milk_chocolate_crispy)
    keyboard.row(salted_caramel_ar)
    keyboard.row(salted_caramel)
    keyboard.row(order)
    return keyboard


def payment():
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Да", callback_data="ДаОплачен")
    no = types.InlineKeyboardButton(text="Нет", callback_data="НетНеОплачен")
    keyboard.row(yes, no)
    return keyboard


def away():
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Да", callback_data="ДаОтдан")
    no = types.InlineKeyboardButton(text="Нет", callback_data="НетНеОтдан")
    keyboard.row(yes, no)
    return keyboard


def save():
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Да", callback_data="ДаСохранить")
    keyboard.row(yes)
    return keyboard


def biscuit():
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Ванильный", callback_data="Ванильный")
    btn2 = types.InlineKeyboardButton(text="Шоколадный", callback_data="Шоколадный")
    btn3 = types.InlineKeyboardButton(text="Фисташковый", callback_data="Фисташковый")
    btn4 = types.InlineKeyboardButton(text="Морковный", callback_data="Морковный")
    btn5 = types.InlineKeyboardButton(text="Другой", callback_data="ДругойБисквит")
    keyboard.row(btn1, btn2)
    keyboard.row(btn3, btn4)
    keyboard.row(btn5)
    return keyboard


def biscuit_tr():
    keyboard = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton(text="Шоколадный", callback_data="ШоколадныйТр")
    btn3 = types.InlineKeyboardButton(text="Фисташковый", callback_data="ФисташковыйТр")
    keyboard.row(btn3, btn2)
    return keyboard


def option():
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Показать все заказы", callback_data="ПоказатьВсеЗаказы")
    btn6 = types.InlineKeyboardButton(text="Показать все заказы клиента", callback_data="ПоказатьЗаказыКлиента")
    btn7 = types.InlineKeyboardButton(text="Показать все заказы по дате", callback_data="ПоказатьЗаказыПоДате")
    btn2 = types.InlineKeyboardButton(text="Показать все оплаченные заказы", callback_data="ПоказатьВсеОплаченныеЗаказы")
    btn3 = types.InlineKeyboardButton(text="Показать все отданные заказы",
                                      callback_data="ПоказатьВсеОтданныеЗаказы")
    btn4 = types.InlineKeyboardButton(text="Показать все не отданные заказы",
                                      callback_data="ПоказатьВсеНеОтданныеЗаказы")
    btn5 = types.InlineKeyboardButton(text="Показать все не оплаченные заказы",
                                      callback_data="ПоказатьВсеНеОплаченныеЗаказы")
    keyboard.row(btn1)
    keyboard.row(btn6)
    keyboard.row(btn7)
    keyboard.row(btn2)
    keyboard.row(btn3)
    keyboard.row(btn4)
    keyboard.row(btn5)
    return keyboard
