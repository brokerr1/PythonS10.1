
from cgitb import handler
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from scripts import check
from random import choice as ch


bot = Bot(token='')
updater = Updater(token='')
dispatcher = updater.dispatcher

data = {2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 10: 4, 'Валет': 4, 'Дама': 4, 'Король': 4,
        'Туз': 4}

count_points_user = []
count_points_bot = 0
score_user = 0
score_bot = 0

WINNER = None # 0 - ничья, 1 - выиграл пользователь, -1 - выиграл бот

BOT = 1
USER = 2


def winner_check(user, bots):
    global WINNER
    if sum(user) > 21 and bots < 22 or sum(user) < bots and sum(user) <= 21 and bots <= 21:
        WINNER = -1
        global score_bot
        score_bot += 1
    elif bots > 21 and sum(user) < 22 or sum(user) > bots and sum(user) <= 21 and bots <= 21:
        WINNER = 1
        global score_user
        score_user += 1
    elif sum(user) > 21 and bots > 21:
        WINNER = 0
    else: WINNER = 0


def start(update, context):
    global count_points_user, count_points_bot, WINNER

    count_points_user.clear()
    count_points_bot = 0
    WINNER = None

    for i in range(2):
        data_object = ch(list(data.keys()))
        print("Карты бота:",data_object)
        while data[data_object] == 0:
            data_object = ch(list(data.keys()))
        data[data_object] -= 1
        points = check(data_object)
        count_points_bot += points

    for i in range(2):
        data_object = ch(list(data.keys()))
        print("Карты пользователя:",data_object)
        while data[data_object] == 0:
            data_object = ch(list(data.keys()))
        data[data_object] -= 1
        points = check(data_object)
        count_points_user.append(points)



    if sum(count_points_user) > 21 and count_points_bot < 22:
        context.bot.send_message(update.effective_chat.id, "Перебор выиграл бот")
    elif count_points_bot > 21 and sum(count_points_user) < 22:
        context.bot.send_message(update.effective_chat.id, "Перебор выиграл ты")
    elif sum(count_points_user) > 21 and count_points_bot > 21:
        context.bot.send_message(update.effective_chat.id, "Перебор вы оба лузеры")
    else:
        #a = '\n'.join([str(i) for i in count_points_user])
        context.bot.send_message(update.effective_chat.id, f"Сумма ваших карт: {sum(count_points_user)}")
    context.bot.send_message(update.effective_chat.id, f"Чтобы взять еще карту нажми -> /Yet")
    context.bot.send_message(update.effective_chat.id, f"Чтобы закончить набор карт нажми -> /stop")


def yet(update, context):
    global count_points_user
    if sum(count_points_user) < 21:
        data_object = ch(list(data.keys()))
        print("Еще карта пользователя:",data_object)
        while data[data_object] == 0:
            data_object = ch(list(data.keys()))
        data[data_object] -= 1
        points = check(data_object)
        count_points_user.append(points)

        a = '\n'.join([str(i) for i in count_points_user])
        #winner_check(count_points_user, count_points_bot)
        if sum(count_points_user) > 21:
            context.bot.send_message(update.effective_chat.id, f"{update.effective_user.first_name}, перебор нажми -> /stop")
        context.bot.send_message(update.effective_chat.id, f"Сумма ваших карт: {sum(count_points_user)}")
        context.bot.send_message(update.effective_chat.id, f"Чтобы взять еще нажми -> /Yet")
        context.bot.send_message(update.effective_chat.id, f"Чтобы закончить набор карт нажми -> /stop")
    else:
        context.bot.send_message(update.effective_chat.id, "Ты не можешь взять больше!")
        context.bot.send_message(update.effective_chat.id, f"Чтобы взять еще нажми -> /Yet")
        context.bot.send_message(update.effective_chat.id, f"Чтобы закончить набор карт нажми -> /stop")



def stop(update, context):
    global WINNER
    if WINNER == None:
        global count_points_bot
        context.bot.send_message(update.effective_chat.id, 'Вы закончили набор, теперь набирает бот')
        if count_points_bot > 15 and ch([True, False]) or count_points_bot <= 12:
            data_object = ch(list(data.keys()))
            while data[data_object] == 0:
                data_object = ch(list(data.keys()))
            data[data_object] -= 1
            points = check(data_object)
            count_points_bot += points

        winner_check(count_points_user, count_points_bot)
        context.bot.send_message(update.effective_chat.id, f'Кол-во очков у бота: {count_points_bot}\n'
                                                           f'Кол-во очков у {update.effective_user.first_name}: {sum(count_points_user)}')
        if WINNER == -1:
            context.bot.send_message(update.effective_chat.id, f"{update.effective_user.first_name}, "
                                                               f"Выиграл бот.\nЧтобы начать заново нажми -> /start")
        elif WINNER == 1:
            context.bot.send_message(update.effective_chat.id, f"{update.effective_user.first_name}, ты выиграл.\nЧтобы начать заново нажми -> /start")
            
        elif WINNER == 0:
            context.bot.send_message(update.effective_chat.id, f"{update.effective_user.first_name} вы с ботом оба лузеры.\nЧтобы начать заново нажми -> /start")
    else:
        context.bot.send_message(update.effective_chat.id, f"Игра окончена, чтобы начать заново нажми -> /start")

def score(update, context):
    global score_bot
    global score_user
    context.bot.send_message(update.effective_chat.id, f'Количество побед у бота: {score_bot}\n'
                                                        f'Количество побед у {update.effective_user.first_name}: {score_user}\n'
                                                         'Сброс счетчика побед -> /restart')



def restart(update, context):
    global score_bot
    global score_user
    score_bot = 0
    score_user = 0
    context.bot.send_message(update.effective_chat.id, 'Количество побед обнулено \n'
                                                        f'Количество побед у бота: {score_bot}\n'
                                                        f'Количество побед у {update.effective_user.first_name}: {score_user}')

start_handler = CommandHandler('start', start)
still_handler = CommandHandler('yet', yet)
stop_handler = CommandHandler('stop', stop)
score_handler = CommandHandler('score', score)
restart_handler = CommandHandler('restart', restart)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(still_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(score_handler)
dispatcher.add_handler(restart_handler)

updater.start_polling()
updater.idle()
