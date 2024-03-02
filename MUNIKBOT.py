import telebot
from telebot import types
import datetime
import csv
token = '6944176491:AAFutBEeym_NGP6p0gWx5_rGr_65FeglEE8'
bot = telebot.TeleBot(token)


markup = types.ReplyKeyboardMarkup()
btn1 = types.KeyboardButton('Часть 1')
btn2 = types.KeyboardButton('Часть 2')
markup.row(btn1, btn2)
btn3 = types.KeyboardButton('Часть 3')
btn4 = types.KeyboardButton('Часть 4')
markup.row(btn3, btn4)
btn5 = types.KeyboardButton('Завершить')
markup.row(btn5)


markup2 = types.ReplyKeyboardMarkup()
btn1 = types.KeyboardButton('1')
btn2 = types.KeyboardButton('2')
btn3 = types.KeyboardButton('3')
btn4 = types.KeyboardButton('4')
btn5 = types.KeyboardButton('5')
markup2.row(btn1, btn2, btn3, btn4, btn5)

markup2 = types.ReplyKeyboardMarkup()
btn1 = types.KeyboardButton('1')
btn2 = types.KeyboardButton('2')
btn3 = types.KeyboardButton('3')
btn4 = types.KeyboardButton('4')
btn5 = types.KeyboardButton('5')
markup2.row(btn1, btn2, btn3, btn4, btn5)
markupch1 = types.ReplyKeyboardMarkup()
btn1 = types.KeyboardButton('1')
btn2 = types.KeyboardButton('2')
btn3 = types.KeyboardButton('3')
btn4 = types.KeyboardButton('4')
markupch1.row(btn1, btn2, btn3, btn4)
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, команда ВЭШ рада приветствовать тебя на нашем пробном региональном"
                                      " этапе! Мы очень надеемся, что тебе понравятся задачи, которые мы подготовили "
                                      "для тебя! Для начала давай создадим уникальный никнейм.  По нему ты сможешь"
                                      " узнать свое место в рейтинге среди написавших. Если ты не хочешь, чтобы твой"
                                      " результат увидели другие участники, ты всегда можешь создать случайный ник,"
                                      " по которому никто не сможет тебя идентифицировать (например УдВуввв4444)."
                                      " Все оскорбительные никнеймы будут удалены. В случае возникновения технических"
                                      " неполадок используй /help. Если это не помогло решить проблему,"
                                      " напиши Роме (@raamensavin).")
    bot.register_next_step_handler(message, nick)


def nick(message):
    if message.text[0] == '/' or len(message.text) > 30:
        bot.send_message(message.chat.id, "Некорректное имя попробуйте другое")
        bot.register_next_step_handler(message, nick)
    else:
        a = 0
        with open('nicks.csv', "r") as fin:
            re = csv.reader(fin)
            at = []
            for row in re:
                at += row
            if at.count(message.text) != 0:
                bot.send_message(message.chat.id, "Занят, выберите другой")
                bot.register_next_step_handler(message, nick)
            else:
                a = 1
        if a == 1:
            with open('nicks.csv', "a") as fin:
                writer = csv.writer(fin)
                usr = [message.from_user.id, message.from_user.username, message.text]
                writer.writerow(usr)
                bot.send_message(chat_id='726382042', text=f"{message.from_user.username} зарегался как {message.text}")
                #bot.send_document(message.chat.id, open('Пробный Муницип.pdf', "rb"))
                msg = bot.send_message(message.chat.id, f"Очень приятно, {message.text}, для продолжения укажи, пожалуйста"
                                                  f", ФИО, почту, регион обучения (в каком городе школа), и класс обуче"
                                                  f"ния через запятую. В формате: 'Рома Савин, romashka@gmail.com, "
                                                  f"Москва, 13'.")
                bot.register_next_step_handler(msg, fio)


def fio(message):
    if len(message.text.split(',')) != 4:
        bot.send_message(message.chat.id, 'Какая-то проблема в формате, попробуй перечитать инструкцию к формату.')
        bot.register_next_step_handler(message, fio)
    else:
        if message.text.split(',')[1].count('@') == 0:
            bot.send_message(message.chat.id, 'Какая-то проблема в формате, попробуй перечитать инструкцию к формату.')
            bot.register_next_step_handler(message, fio)
        else:
            with open('imena.csv', "a") as fin:
                writer = csv.writer(fin)
                ussr = message.text.split(',')
                writer.writerow(ussr)
            bot.send_message(message.chat.id, 'Супер, все готово, для приступления к сдаче задач используй /region.')
            bot.send_document(message.chat.id, open('Municip.pdf', "rb"))

@bot.message_handler(commands=['region'])
def ziza(message):
    bot.send_message(message.chat.id, text='Выберите часть:', reply_markup=markup)
    bot.register_next_step_handler(message, click)


@bot.message_handler(commands=['rating'])
def rat(message):
    with open('rating.csv', 'r') as fin:
        zeze = csv.reader(fin)
        TOT = []
        a = 0
        me = -1
        for row in zeze:
            a+=1
            TOT.append(row)
    TOT.sort(key=lambda x: x[3], reverse=True)
    b=0
    for i in TOT:
        b+=1
        if int(i[0]) == message.from_user.id:
            me = b-1
    bot.send_message(message.chat.id, f'1 место -- {TOT[0][1]}, балл - {TOT[0][3]}\n2 место -- {TOT[1][1]}, балл'
                                      f' -- {TOT[1][3]}\n3 место -- {TOT[2][1]}, балл -- {TOT[2][3]}')
    bot.send_message(message.chat.id, f'Ваша позиция -- {me + 1}, ваш балл -- {TOT[me][3]}, всего участников --{a}')


def click(message):
    if message.text.lower() == 'часть 1':
        msg = bot.send_message(message.chat.id, 'Выберите номер, на который хотите сдать ответ. Сдавайте '
                                                'номера ответа, а не сам ответ (например, если вы выбрали 1)0.5, то нап'
                                                'ишите 1 без скобки)', reply_markup=markup2)
        bot.register_next_step_handler(msg, ch1)
    elif message.text.lower() == 'часть 2':
        msg = bot.send_message(message.chat.id, 'Выберите номер, на который хотите сдать ответ. '
                                                'Отправьте варианты ответов, которые вы выбрали без пробелов (например,'
                                                ' если вы выбрали 1), 2) и 4) напишите 124)', reply_markup=markup3)
        bot.register_next_step_handler(msg, ch1)

    elif message.text.lower() == 'завершить':
        a = 0
        with open('ans/part2.csv', 'r') as fin:
            red = csv.reader(fin)
            at = []
            for row in red:
                at += row
        if at.count(str(message.from_user.id)) != 0:
            a += 1
        with open('ans/part1.csv', 'r') as fin:
            red = csv.reader(fin)
            at = []
            for row in red:
                at += row
        if at.count(str(message.from_user.id)) != 0:
            a += 1
        if a == 0:
            msg = bot.send_message(message.chat.id, 'Вы еще не сдали ни одной части')
            bot.register_next_step_handler(msg, click)
        else:
            msg = bot.send_message(message.chat.id, f'Вы уверены? Вы сдали {a} из 2 частей.', reply_markup=markup2)
            bot.register_next_step_handler(msg, check)
    else:
        msg = bot.send_message(message.chat.id, 'Используйте кнопки')
        bot.register_next_step_handler(msg, click)


def check(message):
    if message.text.lower() == 'да':
        schet = 0
        idd = message.from_user.id
        with open('ans/part1.csv', 'r') as fin:
            red = csv.reader(fin)
            for row in red:
                if int(row[0]) == idd:
                    schet += int(row[3])
                    nickk = row[1]
        with open('ans/part2.csv', 'r') as fin:
            red = csv.reader(fin)
            for row in red:
                if int(row[0]) == message.from_user.id:
                    schet += int(row[3])
                    nickk = row[1]
        usr = [message.from_user.id, nickk, message.from_user.username, schet, datetime.datetime.now()]
        with open('rating.csv', 'a') as fin:
            writer = csv.writer(fin)
            writer.writerow(usr)
        bot.send_message(message.chat.id, f'Супер, твой суммарный балл -- {schet} из 100. Ты можешь узнать свою позицию'
                                          f'в рейтинге используя /rating')
        bot.send_message(message.chat.id, 'Понравилось? Присоединяйся к другим нашим проектам: \n1. Воскресным контестам'
                                          ' от ВЭШ, которые ты можешь найти по ссылке: https://t.me/contest_vesh \n2. '
                                          'Нашему интенсиву к региональному этапу ВСОШ по Экономике. Больше информации '
                                          'можно найти по ссылке: https://t.me/v_e_sh/567 До скорых встреч!')
    elif message.text.lower() == 'нет':
        bot.send_message(message.chat.id, text='Выберите часть:', reply_markup=markup)
        bot.register_next_step_handler(message, click)
    else:
        bot.send_message(message.chat.id, text='Что-то не так, используйте кнопки.', reply_markup=markup2)
        bot.register_next_step_handler(message, check)


def ch1(message):
    if message.text == '1':
        bot.send_message(message.chat.id, 'Выберите ваш ответ на 1 номер:', reply_markup=markupch1)


def zadachi(message):
    if len(message.text.split()) == 10:
        answ = [6, -2, 180, 20, 14, 6, 61, -2, 620, 56]
        schet = 0
        a = message.text.split()
        a1 = []
        for i in a:
            if i.isdigit() or i == '-2':
                a1.append(float(i))
            else:
                a1.append(999999999999)
        for i in range(len(a1)):
            if float(answ[i]) == float(a1[i]):
                schet += 8
        nickk = 'ooooooooooooooooooooooooooooooooooooooooo'
        with open('nicks.csv', 'r') as fin:
            red = csv.reader(fin)
            for row in red:
                if int(row[0]) == int(message.from_user.id):
                    nickk = row[2]
                    break
        with open('ans/part2.csv', 'a') as fin:
            writer = csv.writer(fin)
            usr = [message.from_user.id, nickk, message.from_user.username, schet, datetime.datetime.now()]
            writer.writerow(usr)
            bot.send_message(message.chat.id, f'Супер, твой балл за задачи составляет {schet} из 80')
            bot.send_message(message.chat.id, text='Выберите часть:', reply_markup=markup)
            bot.register_next_step_handler(message, click)
    else:
        bot.send_message(message.chat.id, 'Проверьте правильность написания ответов, по техническим вопросам пишите'
                                          ' @raamensavin')
        bot.send_message(message.chat.id, text='Выберите часть:', reply_markup=markup)
        bot.register_next_step_handler(message, click)


@bot.message_handler(commands=['help'])
def help_m(message):
    bot.send_message(message.chat.id, 'После создания ника и заполнения ваших данных, вы должны были получить файл с за'
                                      'даниями, если этого не произошло, свяжитесь с Ромой @raamensavin. После получения'
                                      'задач используйте /test для сдачи ответов. Внимательно прочитайте инструкцию по'
                                      'формату ответов и всем удачи!!')


bot.infinity_polling()
