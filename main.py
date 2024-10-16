import telebot
from telebot.types import ReplyKeyboardMarkup
from config import TOKEN
from modules import user_management, wallet, tasks, frogger_game

bot = telebot.TeleBot(TOKEN)

def create_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('💰 Balance', '🎯 Tâches')
    markup.row('👥 Amis', '💼 Wallet')
    markup.row('🐸 Jouer à Frogger')
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_management.initialize_user(message)
    bot.send_message(message.chat.id, 
                     f"Bienvenue dans le bot PEPETAS, {message.from_user.first_name}!",
                     reply_markup=create_main_menu())

@bot.message_handler(func=lambda message: message.text == '💰 Balance')
def show_balance(message):
    balance = user_management.get_user_balance(message.chat.id)
    bot.reply_to(message, f"Votre balance actuelle est de {balance} PEPETAS.")

@bot.message_handler(func=lambda message: message.text == '🎯 Tâches')
def show_tasks(message):
    markup = tasks.get_tasks_markup()
    bot.reply_to(message, "Tâches disponibles:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '👥 Amis')
def show_friends(message):
    friends = user_management.get_user_friends(message.chat.id)
    if friends:
        friend_list = "\n".join(friends)
        bot.reply_to(message, f"Vos amis :\n{friend_list}")
    else:
        bot.reply_to(message, "Vous n'avez pas encore d'amis. Invitez-en!")

@bot.message_handler(func=lambda message: message.text == '💼 Wallet')
def wallet_info(message):
    wallet.handle_wallet_info(bot, message)

@bot.message_handler(func=lambda message: message.text == '🐸 Jouer à Frogger')
def start_frogger(message):
    frogger_game.start_game(bot, message)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith('task_'):
        tasks.handle_task(bot, call)
    elif call.data == 'connect_wallet':
        wallet.connect_wallet(bot, call)
    elif call.data.startswith('move_'):
        frogger_game.handle_move(bot, call)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Utilisez le menu pour interagir avec le bot.", reply_markup=create_main_menu())

if __name__ == "__main__":
    bot.polling()