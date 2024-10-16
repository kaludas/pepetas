import time

users = {}

def initialize_user(message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {
            "balance": 0,
            "last_task": 0,
            "nickname": message.from_user.username,
            "friends": [],
            "wallet_connected": False,
            "last_claim": 0,
            "last_checkin": 0
        }

def get_user_balance(user_id):
    return users[user_id]["balance"]

def get_user_friends(user_id):
    return users[user_id]["friends"]

def add_pepetas(user_id, amount):
    users[user_id]["balance"] += amount

def set_wallet_connected(user_id, status):
    users[user_id]["wallet_connected"] = status

def is_wallet_connected(user_id):
    return users[user_id]["wallet_connected"]

def get_last_claim(user_id):
    return users[user_id].get("last_claim", 0)

def set_last_claim(user_id, timestamp):
    users[user_id]["last_claim"] = timestamp

def get_last_checkin(user_id):
    return users[user_id].get("last_checkin", 0)

def set_last_checkin(user_id, timestamp):
    users[user_id]["last_checkin"] = timestamp

def update_balance(user_id, amount):
    users[user_id]["balance"] += amount

def get_user_data(user_id):
    return users.get(user_id, {})

def can_claim(user_id):
    last_claim = get_last_claim(user_id)
    return time.time() - last_claim > 21600  # 6 heures

def can_checkin(user_id):
    last_checkin = get_last_checkin(user_id)
    return time.time() - last_checkin > 86400  # 24 heures

def add_friend(user_id, friend_id):
    if friend_id not in users[user_id]["friends"]:
        users[user_id]["friends"].append(friend_id)
        return True
    return False

def remove_friend(user_id, friend_id):
    if friend_id in users[user_id]["friends"]:
        users[user_id]["friends"].remove(friend_id)
        return True
    return False


def claim(user_id):
    current_time = time.time()
    if current_time - users[user_id].get("last_claim", 0) > 21600:  # 6 heures
        users[user_id]["balance"] += 50
        users[user_id]["last_claim"] = current_time
        return f"Vous avez réclamé 50 PEPETAS! Votre balance: {users[user_id]['balance']:.2f} PEPETAS"
    else:
        remaining_time = 21600 - (current_time - users[user_id].get("last_claim", 0))
        hours, remainder = divmod(remaining_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"Vous devez attendre encore {int(hours)}h {int(minutes)}m avant de pouvoir réclamer à nouveau."

def daily_checkin(user_id):
    current_time = time.time()
    if current_time - users[user_id].get("last_checkin", 0) > 86400:  # 24 heures
        users[user_id]["balance"] += 10
        users[user_id]["last_checkin"] = current_time
        return f"Check-in quotidien réussi! Vous avez reçu 10 PEPETAS. Votre balance: {users[user_id]['balance']:.2f} PEPETAS"
    else:
        return "Vous avez déjà fait votre check-in aujourd'hui. Revenez demain!"

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
