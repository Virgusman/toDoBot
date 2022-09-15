import telebot

token = "5497304680:AAH4QBbTWrMKLTdF81y1_nysUjBD4A71ZTU"

bot = telebot.TeleBot(token)

HELP = """
/help - напечатать справку.
/add - добавить новую задачу
/show - вывести все задачи.
"""

tasks = {}

flag = 0
date = ""

def add_task(date, task):
    if date in tasks:
      tasks[date].append(task)
    else:
      tasks[date] = [task]
    

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
    text = "Задачи:" + "\n"
    for date in tasks:
      text = text + date + ":" + "\n"
      for task in tasks[date]:
        text = text + "  -" + task + "\n"
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
        add_task(date, task)
        text = "Задача- "+ task + ", добавлена на дату- "+ date
        bot.send_message(message.chat.id, text)
        flag = 0
        


#обращается постоянно к серверам телеграмм
bot.polling(none_stop=True)