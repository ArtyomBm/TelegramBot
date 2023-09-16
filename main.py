import telebot
import config
import sqlite3
import time

from telebot import types

bot = telebot.TeleBot(config.TOKEN)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item_1 = types.KeyboardButton("Техническое направление")
item_2 = types.KeyboardButton("Не техническое направление)")
item_3 = types.KeyboardButton('Прочее')
item_4 = types.KeyboardButton('Контакт организатора')
item_5 = types.KeyboardButton('info')

markup.add(item_1, item_2, item_3, item_4, item_5)

def sql(id, data, telegram):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS student_job(
                                id INTEGER,
                                ask TEXT NOT NULL,
                                telegram TEXT NOT NULL
                                );""")
    connect.commit()
    user_id = [id, data, telegram]
    cursor.execute("INSERT INTO student_job VALUES(?, ?, ?);", user_id)
    connect.commit()
    cursor.close()

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Добро пожаловать! '
                                      'Я бот для помощи студентам ВШЭ с какими-либо работами. '
                                      'Выбери направление работы.'.format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'info':
            sti = open('322656665037963564.webp', 'rb')
            bot.send_sticker(message.chat.id, sti)
            bot.send_message(message.chat.id, "Я бот для помощи студентам ВШЭ со всякими работами. "
                                              "Что я делаю? -Я записываю ваши ответы и отправляю их координатору, "
                                              "затем он скидывает работу студентам ВШЭ с соответствующих направлений, "
                                              "после чего те выполняют работу, и все остаются довольны!)"
                                              "Если вдруг есть что-то, что ты хочешь сказать непосредственно моему "
                                              "создателю, то выбери пункт 'Контакт организатора'. Удачи!", parse_mode='html',reply_markup=markup)

        elif message.text == '***':
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            a = """SELECT * FROM student_job"""
            cursor.execute(a)
            b = cursor.fetchall()
            persons = ''
            if len(b) == 0:
                bot.send_message(message.chat.id, 'Список запросов пуст')
            else:
                for i in b:
                    persons += str(i[0])
                    persons += ' '
                    persons += i[1]
                    persons += ' '
                    persons += i[2]
                    persons += '\n'
                bot.send_message(message.chat.id, persons)
        elif '***' in message.text:
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            a = """SELECT * FROM student_job"""
            cursor.execute(a)
            b = cursor.fetchall()
            try:
                person = message.text.split()[-1]
                cursor.execute(f"DELETE FROM student_job WHERE id = {person}")
                connect.commit()
                if int(message.text.split()[-1]) not in [i[0] for i in b]:
                    bot.send_message(message.chat.id, 'Пользователь не найден')
                else:
                    bot.send_message(message.chat.id, f'{person} успешно удален из бд')
            except:
                bot.send_message(message.chat.id, 'Пользователь не найден')
            cursor.close()

        elif message.text == 'Техническое направление':

            tehn_napr = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Цифровая грамотность")
            item2 = types.KeyboardButton("Python")
            item3 = types.KeyboardButton('Работа по SPSS')
            item5 = types.KeyboardButton('Математика')
            item7 = types.KeyboardButton('Анализ данных для курсовой работы')
            item8 = types.KeyboardButton('Свой вариант')
            item9 = types.KeyboardButton('Вернуться назад')
            tehn_napr.add(item1, item2, item3, item5, item7, item8, item9)

            bot.send_message(message.chat.id, "Хорошо, выбери работу:", parse_mode='html', reply_markup=tehn_napr)

        elif message.text == 'Свой вариант':

            bot.send_message(message.chat.id, 'Хорошо, с тобой скоро свяжутся и обсудят все детали.', reply_markup=markup)
            sql(message.chat.id, message.text, message.from_user.username)

        elif message.text == 'Вернуться назад':
            bot.send_message(message.chat.id, 'Вернул тебя обратно.', reply_markup=markup)

        elif message.text == 'Цифровая грамотность':

            bot.send_message(message.chat.id, "Хорошо, заявка на цг оставлена. Ориентировочная цена 2000р. "
                                              "С тобой скоро свяжутся.", parse_mode='html', reply_markup=markup)
            sql(message.chat.id, message.text, message.from_user.username)

        elif message.text == 'Python':

            pytonchik = types.InlineKeyboardMarkup(row_width=2)
            p1 = types.InlineKeyboardButton('Самостоятельная работа', callback_data=f'Ср питон,{message.from_user.username}')
            p2 = types.InlineKeyboardButton('Проект', callback_data=f'Проект питон,{message.from_user.username}')
            p3 = types.InlineKeyboardButton('Экзамен по предмету', callback_data=f'Экз,{message.from_user.username}')
            p4 = types.InlineKeyboardButton('НЭ по Python', callback_data=f'НЭ,{message.from_user.username}')
            pytonchik.add(p1, p2, p3, p4)

            bot.send_message(message.chat.id, 'Какая работа тебя интересует?', reply_markup=pytonchik)

        elif message.text == 'Анализ данных для курсовой работы':

            gde = types.InlineKeyboardMarkup(row_width=2)
            g1 = types.InlineKeyboardButton('SPSS', callback_data=f'spss,{message.from_user.username}')
            g2 = types.InlineKeyboardButton('Excel (рекомендуется)', callback_data=f'excel,{message.from_user.username}')
            gde.add(g1, g2)

            bot.send_message(message.chat.id, 'Где тебя интересует анализ данных? '
                                              '(Рекомендуется Excel, тк есть опыт работы в 30 курсовых)', reply_markup=gde)

        elif message.text == 'Работа по SPSS':

            bot.send_message(message.chat.id, 'Хорошо, с тобой скоро свяжутся и уточнят все детали.', reply_markup=markup)
            sql(message.chat.id, message.text, message.from_user.username)

        elif message.text == 'Математика':

            math = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Мат анализ')
            item2 = types.KeyboardButton('Вышмат')
            item3 = types.KeyboardButton('Линейная алгебра')
            item4 = types.KeyboardButton('Аналитическая геометрия')
            math.add(item1, item2, item3, item4)

            bot.send_message(message.chat.id, 'Выбери предмет', reply_markup=math)

        elif message.text == 'Мат анализ' or message.text == 'Вышмат' or message.text == 'Линейная алгебра' or message.text == 'Аналитическая геометрия':

            bot.send_message(message.chat.id, 'Хорошо, с тобой скоро свяжутся для обсуждения деталей.', reply_markup=markup)
            sql(message.chat.id, message.text, message.from_user.username)

        elif message.text == 'Не техническое направление)':

            gum_napr = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Английский')
            item2 = types.KeyboardButton('Вернуться назад')
            gum_napr.add(item1, item2)
            bot.send_message(message.chat.id, "Выбери предмет", reply_markup=gum_napr)

        elif message.text == 'Английский':

            angl = types.InlineKeyboardMarkup(row_width=2)
            a1 = types.InlineKeyboardButton('Эссе', callback_data=f'Эссе,{message.from_user.username}')
            a2 = types.InlineKeyboardButton('Письмо', callback_data=f'Письмо,{message.from_user.username}')
            a3 = types.InlineKeyboardButton('Домашняя работа', callback_data=f'Др,{message.from_user.username}')
            a4 = types.InlineKeyboardButton('Экзамен/кр и тд', callback_data=f'Экз кр и тд,{message.from_user.username}')
            angl.add(a1, a2, a3, a4)

            bot.send_message(message.chat.id, 'Какая работа тебя интересует?', reply_markup=angl)

        elif message.text == 'Контакт организатора':
            bot.send_message(message.chat.id, 'Telegram: https://t.me/DenyArt')
            bot.send_message(message.chat.id, 'Vk: https://vk.com/needtosleep', parse_mode='html',reply_markup=markup)

        elif message.text == 'Прочее':
            bot.send_message(message.chat.id, 'Хорошо, с тобой скоро свяжутся для обсуждения работы.', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Извини, я не понимаю тебя, используй кнопки снизу для оформления заказа")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data.split(',')[0] == 'Эссе':
                bot.send_message(call.message.chat.id, "Заявка на эссе оставлена. С тобой в скором времени свяжутся) "
                                                       "Ориентировочная цена: 1500р.", reply_markup=markup)
                sql(call.message.chat.id, call.data.split(',')[0], call.data.split(',')[-1])
            elif call.data.split(',')[0] == 'Письмо':
                bot.send_message(call.message.chat.id, "Заявка на письмо оставлена. С тобой в скором времени свяжутся) "
                                                        "Ориентировочная цена: 1000р.", reply_markup=markup)
                sql(call.message.chat.id, call.data.split(',')[0], call.data.split(',')[-1])
            elif call.data.split(',')[0] == 'Др':
                bot.send_message(call.message.chat.id, "Заявка на домашку отправлена. Тогда с выполнителем договоритесь о "
                                                       "конкретной цене и сроках выполнения.", reply_markup=markup)
                sql(call.message.chat.id, call.data.split(',')[0], call.data.split(',')[-1])
            elif call.data.split(',')[0] == 'Экз кр и тд':
                bot.send_message(call.message.chat.id, "Заявка на работу отправлена. С тобой в скором времени свяжутся)", reply_markup=markup)
                sql(call.message.chat.id, call.data.split(',')[0], call.data.split(',')[-1])
            elif call.data.split(',')[0] == 'Ср питон':
                bot.send_message(call.message.chat.id, "Заявка на самостоятельную работу отправлена. С тобой скоро свяжутся."
                                                       " Ориентировочная цена 1000р.", reply_markup=markup)
                sql(call.message.chat.id, call.data.split(',')[0], call.data.split(',')[-1])
            elif call.data.split(',')[0] == 'Проект питон':
                bot.send_message(call.message.chat.id, "Заявка на проект отправлена. С тобой скоро свяжутся."
                                                       " Ориентировочная цена 2500р. Цена будет варьироваться от сложности задания.", reply_markup=markup)
                sql(call.message.chat.id, call.data.split(',')[0], call.data.split(',')[-1])
            elif call.data.split(',')[0] == 'Экз':
                bot.send_message(call.message.chat.id, "Заявка на экзамен отправлена. С тобой скоро свяжутся."
                                                       " Ориентировочная цена 2000р.", reply_markup=markup)
                sql(call.message.chat.id, call.data.split(',')[0], call.data.split(',')[-1])
            elif call.data.split(',')[0] == 'НЭ':
                bot.send_message(call.message.chat.id, "Заявка на экзамен отправлена. С тобой скоро свяжутся."
                                                       " Ориентировочная цена 2500р. По поводу написания тебе напишут.", reply_markup=markup)
                sql(call.message.chat.id, call.data.split(',')[0], call.data.split(',')[-1])
            elif call.data.split(',')[0] == 'spss':
                bot.send_message(call.message.chat.id, 'Заявка на анализ данных отправлена. Тип выполнения: SPSS. '
                                                       'Ориентировочная цена 3000р. Тебе скоро напишут.', reply_markup=markup)
                sql(call.message.chat.id, call.data.split(',')[0], call.data.split(',')[-1])
            elif call.data.split(',')[0] == 'excel':
                bot.send_message(call.message.chat.id, 'Заявка на анализ данных отправлена. Тип выполнения: Excel. '
                                                       'Ориентировочная цена 3000р. Тебе скоро напишут.', reply_markup=markup)
                sql(call.message.chat.id, call.data.split(',')[0], call.data.split(',')[-1])
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Какая работа тебя интересует?')
    except Exception as e:
        print(repr(e))
if __name__ == '__main__':
    while True:
        try:
            bot.infinity_polling(none_stop=True)
        except Exception as e:
            bot.send_message(2027559485, 'Перезапусти меня, я сломался')
            time.sleep(5)
            continue