import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import time
import json

TOKEN = 'VOTRE_TOKEN_BOT'
bot = telebot.TeleBot(TOKEN)

# Stockage des données utilisateur (à remplacer par une base de données réelle)
users = {}

# Tâches disponibles
tasks = [
    {"name": "Inviter 5 amis", "reward": 100, "progress": 0, "goal": 5},
    {"name": "Jouer 3 mini-jeux", "reward": 50, "progress": 0, "goal": 3}
]

def create_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("🏠 Home"), KeyboardButton("🎮 Games"))
    markup.row(KeyboardButton("👥 Friends"), KeyboardButton("📋 Tasks"))
    markup.row(KeyboardButton("💰 Tap to Earn"), KeyboardButton("🎁 Claim"))
    markup.row(KeyboardButton("📅 Daily Check-in"), KeyboardButton("📊 Balance"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {"balance": 0, "last_claim": 0, "last_checkin": 0}
    
    bot.reply_to(message, "Bienvenue dans PEPETAS Bot!", reply_markup=create_main_menu())

@bot.message_handler(func=lambda message: message.text == "🏠 Home")
def show_home(message):
    user_id = message.from_user.id
    user_data = users[user_id]
    home_message = f"🏠 Accueil PEPETAS Bot\n\n"
    home_message += f"💰 Balance: {user_data['balance']:.2f} PEPETAS\n"
    home_message += f"🎁 Prochain claim disponible dans: {calculate_next_claim(user_data['last_claim'])}\n"
    home_message += f"📅 Prochain check-in dans: {calculate_next_checkin(user_data['last_checkin'])}\n"
    
    bot.reply_to(message, home_message, reply_markup=create_main_menu())

@bot.message_handler(func=lambda message: message.text == "🎮 Games")
def show_games(message):
    # Implémentez ici la logique pour les jeux
    bot.reply_to(message, "Voici nos jeux disponibles : [liste des jeux]", reply_markup=create_main_menu())

@bot.message_handler(func=lambda message: message.text == "👥 Friends")
def show_friends(message):
    # Implémentez ici la logique pour la fonctionnalité amis
    bot.reply_to(message, "Voici vos amis : [liste des amis]", reply_markup=create_main_menu())

@bot.message_handler(func=lambda message: message.text == "📋 Tasks")
def show_tasks(message):
    task_list = "Vos tâches :\n\n"
    for i, task in enumerate(tasks):
        task_list += f"{i+1}. {task['name']} - Progrès : {task['progress']}/{task['goal']} - Récompense : {task['reward']} PEPETAS\n"
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("Compléter une tâche"), KeyboardButton("Retour"))
    
    bot.reply_to(message, task_list, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Compléter une tâche")
def complete_task(message):
    import random
    task = random.choice(tasks)
    task['progress'] = min(task['progress'] + 1, task['goal'])
    
    if task['progress'] == task['goal']:
        users[message.from_user.id]['balance'] += task['reward']
        bot.reply_to(message, f"Tâche '{task['name']}' complétée! Vous avez gagné {task['reward']} PEPETAS!")
    else:
        bot.reply_to(message, f"Progrès sur la tâche '{task['name']}' : {task['progress']}/{task['goal']}")

@bot.message_handler(func=lambda message: message.text == "💰 Tap to Earn")
def tap_to_earn(message):
    user_id = message.from_user.id
    users[user_id]["balance"] += 0.01
    bot.reply_to(message, f"Vous avez gagné 0.01 PEPETAS! Votre balance: {users[user_id]['balance']:.2f} PEPETAS")

@bot.message_handler(func=lambda message: message.text == "🎁 Claim")
def claim(message):
    user_id = message.from_user.id
    current_time = time.time()
    if current_time - users[user_id].get("last_claim", 0) > 21600:  # 6 heures
        users[user_id]["balance"] += 50
        users[user_id]["last_claim"] = current_time
        bot.reply_to(message, f"Vous avez réclamé 50 PEPETAS! Votre balance: {users[user_id]['balance']:.2f} PEPETAS")
    else:
        remaining_time = 21600 - (current_time - users[user_id].get("last_claim", 0))
        hours, remainder = divmod(remaining_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        bot.reply_to(message, f"Vous devez attendre encore {int(hours)}h {int(minutes)}m avant de pouvoir réclamer à nouveau.")

@bot.message_handler(func=lambda message: message.text == "📅 Daily Check-in")
def daily_checkin(message):
    user_id = message.from_user.id
    current_time = time.time()
    if current_time - users[user_id].get("last_checkin", 0) > 86400:  # 24 heures
        users[user_id]["balance"] += 10
        users[user_id]["last_checkin"] = current_time
        bot.reply_to(message, f"Check-in quotidien réussi! Vous avez reçu 10 PEPETAS. Votre balance: {users[user_id]['balance']:.2f} PEPETAS")
    else:
        bot.reply_to(message, "Vous avez déjà fait votre check-in aujourd'hui. Revenez demain!")

@bot.message_handler(func=lambda message: message.text == "📊 Balance")
def show_balance(message):
    user_id = message.from_user.id
    bot.reply_to(message, f"Votre balance actuelle est de {users[user_id]['balance']:.2f} PEPETAS")

@bot.message_handler(func=lambda message: message.text == "Retour")
def go_back(message):
    bot.reply_to(message, "Retour au menu principal", reply_markup=create_main_menu())

def calculate_next_claim(last_claim):
    current_time = time.time()
    time_passed = current_time - last_claim
    if time_passed >= 21600:
        return "Disponible maintenant!"
    else:
        remaining = 21600 - time_passed
        hours, remainder = divmod(remaining, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}h {int(minutes)}m"

def calculate_next_checkin(last_checkin):
    current_time = time.time()
    time_passed = current_time - last_checkin
    if time_passed >= 86400:
        return "Disponible maintenant!"
    else:
        remaining = 86400 - time_passed
        hours, remainder = divmod(remaining, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}h {int(minutes)}m"

bot.polling()
