from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from modules import user_management

def get_tasks_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Ajouter ❤️ au pseudo (+300 PEPETAS)", callback_data="task_heart"))
    markup.add(InlineKeyboardButton("Inviter un ami (+500 PEPETAS)", callback_data="task_invite"))
    markup.add(InlineKeyboardButton("Connecter votre wallet (+1000 PEPETAS)", callback_data="task_wallet"))
    return markup

def handle_task(bot, call):
    user_id = call.from_user.id
    task = call.data.split('_')[1]
    
    if task == 'heart':
        if '❤️' not in user_management.users[user_id]['nickname']:
            user_management.users[user_id]['nickname'] += '❤️'
            user_management.add_pepetas(user_id, 300)
            bot.answer_callback_query(call.id, "Tâche complétée! +300 PEPETAS ajoutés.")
        else:
            bot.answer_callback_query(call.id, "Vous avez déjà complété cette tâche.")
    
    elif task == 'invite':
        invite_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
        bot.answer_callback_query(call.id, "Voici votre lien d'invitation:")
        bot.send_message(call.message.chat.id, f"Partagez ce lien: {invite_link}")
    
    elif task == 'wallet':
        if not user_management.is_wallet_connected(user_id):
            user_management.set_wallet_connected(user_id, True)
            user_management.add_pepetas(user_id, 1000)
            bot.answer_callback_query(call.id, "Wallet connecté! +1000 PEPETAS ajoutés.")
        else:
            bot.answer_callback_query(call.id, "Votre wallet est déjà connecté.")