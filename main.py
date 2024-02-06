import telebot
import sqlite3

bot = telebot.TeleBot('6012349907:AAEJI30cmP1mhiv6W1dcs6UKfmWVz9U3yPU')
db_file = "for school"
con = sqlite3.connect(db_file, check_same_thread=False)
cur = con.cursor()


@bot.message_handler(commands=['start'])
def start_main(message):
    # Старт - классическая команда у всех ботов, создается для начала работы и проверки работоспобности проекта
    bot.send_message(message.chat.id, f'привет, {message.from_user.first_name}, это школьный цифоровой дневник в '
                                      f'телеграмм')


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'заглушка')  # инструкция по работе с ботом


@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Что ж, начнём по-новой")  # бот будет сбрасывать данные


@bot.message_handler(commands=['register'])
def register(message):
    bot.send_message(message.chat.id, "Введите имя: ")

    bot.register_next_step_handler(message, user_name)


def user_name(message):
    res = cur.execute("""SELECT FIO from ученики UNION 
    SELECT FIO from учителя""").fetchall()
    res_str = ''
    for i in range(len(res)):
        for j in range(len(res[i])):
            res_str += ''.join(res[i][j])
        res_str += ', '
    print(res_str)
    name = message.text.strip()
    if name in res_str:
        bot.send_message(message.chat.id, "Введите пароль: ")
        bot.register_next_step_handler(message, user_get_password, name)
    else:
        bot.send_message(message.chat.id, "Вас нет в базе данных(либо опечатались), обратитесь за помощью к @yarmixer")


def user_get_password(message, name):
    password = message.text.strip()
    res = cur.execute(f"""SELECT password from ученики WHERE FIO='{name}'
    UNION SELECT password from учителя WHERE FIO='{name}'""").fetchall()
    print(res)
    if password == str(res[0][0]):
        bot.send_message(message.chat.id, "Вы успешно вошли в аккаунт")
        print(message.chat.id)
        cur.execute(f"""UPDATE ученики SET chat_id = '{message.chat.id}'
        WHERE FIO = '{name}'""").fetchall()
        con.commit()
    else:
        bot.send_message(message.chat.id, "Неверный пароль")


@bot.message_handler(commands=['оценки'])
def assessments(message):
    '''if message.from_user.first_name =='''
'''    if message.chat.id in
        bot.send_message(message.chat.id, 'сейчас посмотрим')
    else:
        bot.send_message(message.chat.id, 'вы не вошли в аккаунт')'''


@bot.message_handler(content_types=['text'])
def name_get(message):
    text = message.text.strip()  # заглушка
    print(text)


bot.polling(none_stop=True)
