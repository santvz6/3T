import copy
import random
from flask import Flask

# Lista de segundos movimientos en los que O gana
instant_wins = [[['0', 'X', '0'],
                 ['0', 'O', '0'],
                 ['0', '0', '0']],

                [['0', '0', '0'],
                 ['X', 'O', '0'],
                 ['0', '0', '0']],

                [['0', '0', '0'],
                 ['0', 'O', 'X'],
                 ['0', '0', '0']],

                [['0', '0', '0'],
                 ['0', 'O', '0'],
                 ['0', 'X', '0']]]



# ---- FUNCIÓN PARA DETECTAR VICTORIAS ----
def detect_victory(state):
    # Verificar filas
    for row in state:
        if row[0] == row[1] == row[2] != '0':
            return True

    # Verificar columnas
    for column in range(3):
        if (state[0][column] == state[1][column]
                == state[2][column] != '0'):
            return True

    # Verificar diagonales
    if (state[0][0] == state[1][1]
            == state[2][2] != '0'):
        return True

    if (state[0][2] == state[1][1]
            == state[2][0] != '0'):
        return True

    return False

# FUNCIÓN QUE CREA UNA LISTA CON TODOS LOS MOVIMIENTOS POSIBLES DE {symbol}
def possible_future_states(state:list, symbol):
    compendium = []
    for row in range(3):
        for position in range(3):
            if state[row][position] == '0':
                future_state = copy.deepcopy(state)
                future_state[row][position] = symbol
                compendium.append(future_state)

    return compendium


def bot_T1(state:list, difficulty:int):

    # ---------- SITUACIONES INICIALES ---------- #

    # Prioriza el centro cuando no está ocupado
    if difficulty > 1:
        if state[1][1] == '0':
            state[1][1] = 'O'
            return state

    # Evita las casillas en cruz en el segundo movimiento, ya que esos movimientos implican perder
    if difficulty > 1:
        if state == [['0', '0', '0'], ['0', 'X', '0'], ['0', '0', '0']]:
            corner = random.randint(1, 4)
            match corner:
                case 1:
                    state[0][0] = 'O'
                case 2:
                    state[0][2] = 'O'
                case 3:
                    state[2][0] = 'O'
                case 4:
                    state[2][2] = 'O'
            return state

    # Si x ha hecho un segundo movimiento en las casillas en cruz, el bot en su máxima dificultad gana
    if difficulty == 3 and state in instant_wins:
            if state == instant_wins[0]:
                state[2][0] = 'O'
            elif state == instant_wins[1]:
                state[2][2] = 'O'
            elif state == instant_wins[2]:
                state[0][0] = 'O'
            elif state == instant_wins[3]:
                state[0][2] = 'O'
            return state

    # ---------- SITUACIONES GENERALES ---------- #

    # Clasifica todos los movimientos en listas dependiendo de lo buenos que son, y luego los utiliza en un orden
    # de prioridad por el cual: winning_moves > neutral_moves > losing_moves
    winning_moves = []
    best_neutral_moves = []
    neutral_moves = []
    losing_moves = []
    future_states = possible_future_states(state, 'O')  # Obtenemos una lista de todos los movimientos de o
    for possible_state in future_states:  # Comprobamos en cada uno de los movimientos si es una victoria
        if detect_victory(possible_state):
            winning_moves.append(possible_state)  # Si es victoria, es winning move
        else:
            lost = False  # Variable que determina si un movimiento es losing o neutral
            future_future_states = possible_future_states(possible_state, 'X')  # Lista de todos los movimientos de x después del movimiento de o
            for possible_state2 in future_future_states:
                if detect_victory(possible_state2):  # Si x gana después de o, lost se pone a True
                    lost = True
            if lost:
                losing_moves.append(possible_state)  # Si pierde justo después de jugar, es un losing move
            else:
                best_move = False  # Clasificaremos los movimientos neutrales según esta variable
                future_wins = possible_future_states(possible_state, 'O')  # Lista de todos los posibles segundos movimientos de o
                for future_win in future_wins:
                    if detect_victory(future_win):
                        best_move = True  # Si el movimiento crea una futura situación de victoria, es el mejor movimiento neutral
                if best_move:
                    best_neutral_moves.append(possible_state)
                neutral_moves.append(possible_state)  # Si no pierde justo después de jugar, es un neutral move

    if winning_moves:
        return random.choice(winning_moves)  # Prioriza movimientos de victoria
    elif best_neutral_moves and difficulty == 3:
        return random.choice(best_neutral_moves) # Con dificultad máxima, prioriza movimientos que le ayuden a ganar
    elif neutral_moves:
        return random.choice(neutral_moves)  # Prioriza (menos que los de victoria) los movimientos neutrales
    else:
        return random.choice(losing_moves)  # Evita movimientos de derrota

def state_move(state1, state2):
    for row in range(3):
        if state1[row] != state2[row]:
            for column in range(3):
                if state1[row][column] != state2[row][column]:
                    return f'{row}{column}'  # Devuelve la fila y la columna del movimiento
    return None

def str_to_state(state):
    result = []
    row1 = state[0:3]
    row2 = state[3:6]
    row3 = state[6:9]
    difficulty = int(state[-1])
    for row in (row1, row2, row3):
        actual_row = []
        for cell in row:
            actual_row.append(cell)
        result.append(actual_row)
    return result, difficulty

bot = Flask(__name__)

@bot.route('/')
def hello_world():
    return ('This API takes a state of a tic tac toe game in form of a string and returns the next move in this format:\n'
            '00X0000O03\nWhere the rows are positions [0,3], [3,6] and [6,9] each, while [-1] is the difficulty (ranges from'
            '1 to 3).')

@bot.route('/<strstate>', methods=['GET'])
def get_state(strstate):
    try:
        if len(strstate) != 10:
            raise ValueError
        for char in strstate:
            if char not in '0OX123':
                raise ValueError
        state = str_to_state(strstate)
        difficulty = int(strstate[-1])
        return state_move(state[0], bot_T1(state[0], difficulty)), 200
    except ValueError:
        return 'Invalid state.', 400

strstate = '00O0OX00X2'
for char in strstate:
        if char not in '0OX123':
            raise ValueError
