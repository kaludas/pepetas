users = {}

def initialize_user(message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {
            "balance": 0,
            "last_task": 0,
            "nickname": message.from_user.username,
            "friends": [],
            "wallet_connected": False
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