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
