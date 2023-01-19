import telebot
import sqlite3

token = ""   #Указать ТОКЕН бота

bot = telebot.TeleBot(token)


HELP = """
/help - напечатать справку.
/add - добавить новую задачу
/show - вывести все задачи.
"""

#флаг определяет какое действие будет выполнено при вводе ссобщения пользователем
flag = 0 
date = ""


def add_task(user, date, task):
    conn = sqlite3.connect('db/database.db', check_same_thread = False) 
    cursor = conn.cursor()
    cursor.execute('INSERT INTO toDoBot (user_id,date,task) VALUES (?,?,?)', (user,date,task,))
    conn.commit()
    conn.close()
    
    
#выполнение команд в Боте:
@bot.message_handler(commands=['start'])
def start_mess(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=["add"])
def add(message):
    global flag
    flag = 1
    bot.send_message(message.chat.id, "Укажите дату:")
    
@bot.message_handler(commands=["show"])
def show(message):
    conn = sqlite3.connect('db/database.db', check_same_thread = False) 
    cursor = conn.cursor()
    cursor.execute('SELECT date, task FROM toDoBot WHERE user_id = (?)', (message.from_user.id,))
    tasks = cursor.fetchall()
    conn.close()

    text = "Задачи:"
    for date in tasks:
        text = text + "\n" + str(date[0]) + " - " + str(date[1])
      
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    global flag
    global date
    if flag == 1:
        date = message.text.lower()
        bot.send_message(message.chat.id, "Укажите задачу:")
        flag = 2
    elif flag == 2:
        task = message.text
        user = message.from_user.id
        add_task(user, date, task)
        text = "Задача- "+ task + ", добавлена на дату- "+ date
        bot.send_message(message.chat.id, text)
        flag = 0


#обращается постоянно к серверам телеграмм
bot.polling(none_stop=True)