from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
from modules import user_management

ROAD_WIDTH = 5
GAME_WIDTH = 7
GAME_HEIGHT = 5
FROG = '🐸'
CAR = '🚗'
ROAD = '⬛'
SAFE = '🟩'

games = {}

def create_game_board():
    board = [[SAFE] * GAME_WIDTH for _ in range(GAME_HEIGHT)]
    for i in range(1, GAME_HEIGHT - 1):
        board[i] = [ROAD] * GAME_WIDTH
    return board

def add_cars(board):
    for i in range(1, GAME_HEIGHT - 1):
        car_positions = random.sample(range(GAME_WIDTH), 2)
        for j in car_positions:
            board[i][j] = CAR
    return board

def create_game_keyboard(game_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("⬅️", callback_data=f"move_{game_id}_left"),
        InlineKeyboardButton("➡️", callback_data=f"move_{game_id}_right")
    )
    keyboard.row(InlineKeyboardButton("⬆️", callback_data=f"move_{game_id}_up"))
    return keyboard

def board_to_string(board, frog_pos):
    board_copy = [row.copy() for row in board]
    board_copy[frog_pos[0]][frog_pos[1]] = FROG
    return '\n'.join([''.join(row) for row in board_copy])

def start_game(bot, message):
    game_id = str(message.chat.id)
    board = create_game_board()
    board = add_cars(board)
    frog_pos = [GAME_HEIGHT - 1, GAME_WIDTH // 2]
    games[game_id] = {'board': board, 'frog_pos': frog_pos, 'moves': 0}
    
    bot.send_message(
        message.chat.id,
        f"Aidez le crapaud 🐸 à traverser la route!\n\n{board_to_string(board, frog_pos)}",
        reply_markup=create_game_keyboard(game_id)
    )

def handle_move(bot, call):
    _, game_id, direction = call.data.split('_')
    game = games.get(game_id)
    
    if not game:
        bot.answer_callback_query(call.id, "Jeu terminé ou inexistant.")
        return
    
    frog_pos = game['frog_pos']
    board = game['board']
    
    if direction == 'left' and frog_pos[1] > 0:
        frog_pos[1] -= 1
    elif direction == 'right' and frog_pos[1] < GAME_WIDTH - 1:
        frog_pos[1] += 1
    elif direction == 'up' and frog_pos[0] > 0:
        frog_pos[0] -= 1
    
    game['moves'] += 1
    
    # Vérifier collision
    if board[frog_pos[0]][frog_pos[1]] == CAR:
        bot.edit_message_text(
            f"Game Over! Le crapaud s'est fait écraser. Nombre de mouvements: {game['moves']}",
            call.message.chat.id,
            call.message.message_id
        )
        del games[game_id]
        return
    
    # Vérifier victoire
    if frog_pos[0] == 0:
        pepetas_earned = 100 + max(0, 50 - game['moves'])  # Bonus pour moins de mouvements
        user_management.add_pepetas(int(game_id), pepetas_earned)
        bot.edit_message_text(
            f"Félicitations! Le crapaud a traversé en {game['moves']} mouvements.\nVous gagnez {pepetas_earned} PEPETAS!",
            call.message.chat.id,
            call.message.message_id
        )
        del games[game_id]
        return
    
    # Mettre à jour le jeu
    games[game_id] = game
    bot.edit_message_text(
        f"Mouvements: {game['moves']}\n\n{board_to_string(board, frog_pos)}",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=create_game_keyboard(game_id)
    )