import random

# ---- FUNCIÓN PARA DETECTAR VICTORIAS ----
# def detectar_victoria(state):
#     for row in state:
#         if row[0] and row[0] == row[1] == row[2]:
#             return True
#         
#     for i in range(3):
#         column = []
#         for j in range(3):
#             column.append(state[j][i])
#         if column[0] and column[0] == column[1] == column[2]:
#             return True
#     
#     if state[0][0] and state[0][0] == state[1][1] == state[2][2]:
#         return True
#     
#     elif state[0][2] and state[0][2] == state[1][1] == state[2][0]:
#         return True
# 
#     else:
#         return False

# FUNCIÓN QUE CREA UNA LISTA CON TODOS LOS MOVIMIENTOS POSIBLES DE {symbol}
def possible_future_states(state:list, symbol):
    compendium = []
    for row in range(3):
        for position in range(3):
            # Posición en la fila sin jugar (0)
            if not state[row][position]:
                future_state = []
                # Copiamos state → Future_state
                for fila in state:
                    future_state.append(fila.copy())
                future_state[row][position] = symbol
                compendium.append(future_state)
    
    return compendium
                
    
def bot_1T(state:list):
    # Prioriza el centro cuando no está ocupado
    if not state[1][1]:
        state[1][1] = 'J2'
        return state
    
    # Evita los lados en el segundo movimiento
    elif state[1][1] == 'J1' and (state[0], state[2]) == ([0, 0, 0], [0, 0, 0]) and (state[1][0], state[1][2]) == (0, 0):
        corner = random.randint(1, 4)
        match corner:
            case 1:
                state[0][0] = 'J2'
            case 2:
                state[0][2] = 'J2'
            case 3:
                state[2][0] = 'J2'
            case 4:
                state[2][2] = 'J2'
        return state
    
    # Clasifica todos los movimientos en listas dependiendo de lo buenos que son, y luego los utiliza en un orden
    # de prioridad por el cual: winning_moves > neutral_moves > losing_moves
    winning_moves = []
    neutral_moves = []
    losing_moves = []
    future_states = possible_future_states(state, 'J2')  # Obtenemos una lista de todos los movimientos de 2
    for possible_state in future_states:  # Comprobamos en cada uno de los movimientos si es una victoria
        if detectar_victoria(possible_state):
            winning_moves.append(possible_state)  # Si es victoria, es winning move
        else:
            lost = False  # Variable que determina si un movimiento es losing o neutral
            future_future_states = possible_future_states(possible_state, 'J1')  # Lista de todos los movimientos de 1 después del movimiento de 2
            for possible_state2 in future_future_states:
                if detectar_victoria(possible_state2):  # Si 1 gana después de 2, lost se pone a True
                    lost = True
            if lost:
                losing_moves.append(possible_state)  # Si pierde justo después de jugar, es un losing move
            else:
                neutral_moves.append(possible_state) # Si no pierde justo después de jugar, es un neutral move
    
    if winning_moves:
        return random.choice(winning_moves)  # Prioriza movimientos de victoria
    elif neutral_moves:
        return random.choice(neutral_moves)  # Prioriza (menos que los de victoria) los movimientos neutrales
    else:
        return random.choice(losing_moves)  # Evita movimientos de derrota
    

