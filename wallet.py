from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from modules import user_management

def handle_wallet_info(bot, message):
    user_id = message.chat.id
    if user_management.is_wallet_connected(user_id):
        bot.reply_to(message, "Votre wallet est connecté. Vous pouvez recevoir et envoyer des PEPETAS.")
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Connecter Wallet", callback_data="connect_wallet"))
        bot.reply_to(message, "Votre wallet n'est pas connecté.", reply_markup=markup)

def connect_wallet(bot, call):
    user_id = call.from_user.id
    if not user_management.is_wallet_connected(user_id):
        user_management.set_wallet_connected(user_id, True)
        user_management.add_pepetas(user_id, 1000)
        bot.answer_callback_query(call.id, "Wallet connecté avec succès! +1000 PEPETAS de bonus.")
    else:
        bot.answer_callback_query(call.id, "Votre wallet est déjà connecté.")