import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN
from modules import user_management, wallet, tasks, frogger_game
import time

bot = telebot.TeleBot(TOKEN)

def create_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("🏠 Home"), KeyboardButton("🎮 Games"))
    markup.row(KeyboardButton("👥 Friends"), KeyboardButton("📋 Tasks"))
    markup.row(KeyboardButton("💰 Tap to Earn"), KeyboardButton("🎁 Claim"))
    markup.row(KeyboardButton("📅 Daily Check-in"), KeyboardButton("📊 Balance"))
    markup.row(KeyboardButton("🐸 Jouer à Frogger"), KeyboardButton("💼 Wallet"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_management.initialize_user(message)
    bot.send_message(message.chat.id, 
                     f"Bienvenue dans le bot PEPETAS, {message.from_user.first_name}!",
                     reply_markup=create_main_menu())

@bot.message_handler(func=lambda message: message.text == "🏠 Home")
def show_home(message):
    user_data = user_management.get_user_data(message.from_user.id)
    home_message = f"🏠 Accueil PEPETAS Bot\n\n"
    home_message += f"💰 Balance: {user_data['balance']:.2f} PEPETAS\n"
    home_message += f"🎁 Prochain claim disponible dans: {user_management.calculate_next_claim(user_data['last_claim'])}\n"
    home_message += f"📅 Prochain check-in dans: {user_management.calculate_next_checkin(user_data['last_checkin'])}\n"
    
    bot.reply_to(message, home_message, reply_markup=create_main_menu())

@bot.message_handler(func=lambda message: message.text == "🎮 Games")
def show_games(message):
    games_message = "Voici nos jeux disponibles :\n1. 🐸 Frogger\n2. 🎲 Dice Roll (à venir)\n3. 🃏 Blackjack (à venir)"
    bot.reply_to(message, games_message, reply_markup=create_main_menu())

@bot.message_handler(func=lambda message: message.text == "👥 Friends")
def show_friends(message):
    friends = user_management.get_user_friends(message.from_user.id)
    if friends:
        friend_list = "\n".join(friends)
        bot.reply_to(message, f"Vos amis :\n{friend_list}")
    else:
        bot.reply_to(message, "Vous n'avez pas encore d'amis. Invitez-en!")

@bot.message_handler(func=lambda message: message.text == "📋 Tasks")
def show_tasks(message):
    markup = tasks.get_tasks_markup()
    bot.reply_to(message, "Tâches disponibles:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "💰 Tap to Earn")
def tap_to_earn(message):
    user_id = message.from_user.id
    amount = 0.01
    user_management.add_pepetas(user_id, amount)
    balance = user_management.get_user_balance(user_id)
    bot.reply_to(message, f"Vous avez gagné {amount} PEPETAS! Votre balance: {balance:.2f} PEPETAS")

@bot.message_handler(func=lambda message: message.text == "🎁 Claim")
def claim(message):
    user_id = message.from_user.id
    claim_result = user_management.claim(user_id)
    bot.reply_to(message, claim_result)

@bot.message_handler(func=lambda message: message.text == "📅 Daily Check-in")
def daily_checkin(message):
    user_id = message.from_user.id
    checkin_result = user_management.daily_checkin(user_id)
    bot.reply_to(message, checkin_result)

@bot.message_handler(func=lambda message: message.text == "📊 Balance")
def show_balance(message):
    balance = user_management.get_user_balance(message.from_user.id)
    bot.reply_to(message, f"Votre balance actuelle est de {balance:.2f} PEPETAS")

@bot.message_handler(func=lambda message: message.text == "🐸 Jouer à Frogger")
def start_frogger(message):
    frogger_game.start_game(bot, message)

@bot.message_handler(func=lambda message: message.text == "💼 Wallet")
def wallet_info(message):
    wallet.handle_wallet_info(bot, message)

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
