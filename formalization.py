# PART 1
def toMove(state):
    # return the player in the first index of the state
    return state[0]

def actions(state):
    possible_actions = []
    turn = toMove(state)
    for i in range(10):
        # if it is whites turn and the square has a white piece on it
        # and the piece hasnt reached the end
        if turn == 1 and state[i] == 1 and i > 3:
            # if the square ahead is empty
            if state[i - 3] == 0:
                index = get_index(i)
                possible_actions.append(['advance', index[0], index[1]])
            if state[i - 4] == -1:
                possible_actions.append(['capture-right', index[0], index[1]])
            if state[i - 5] == -1:
                possible_actions.append(['capture-left', index[0], index[1]])
        # if it is blacks turn and the square has a black piece on it
        # and the piece hasnt reached the end
        elif turn == -1 and state[i] == -1 and i < 7:
            # if the square ahead is empty
            if state[i + 3] == 0:
                index = get_index(i)
                possible_actions.append(['advance', index[0], index[1]])
            if state[i + 4] == 1:
                possible_actions.append(['capture-right', index[0], index[1]])
            if state[i + 5] == 1:
                possible_actions.append(['capture-left', index[0], index[1]])

            return possible_actions

            

def result(state, action):
    turn = toMove(state)
    new_state = state
    # perform the action based on which colors turn it is

    # if its whites turn
    if turn == 1:
        if action[0] == 'advance':
            new_state[actions[1] - 3] = 1
            new_state[actions[1]] = 0
        elif action[0] == 'capture-right':
            new_state[actions[1] - 4] = 1
            new_state[actions[1]] = 0
        elif action[0] == 'capture-left':
            new_state[actions[1] - 5] = 1
            new_state[actions[1]] = 0
    # if its blacks turn
    elif turn == -1:
        if action[0] == 'advance':
            new_state[actions[1] + 3] = 1
            new_state[actions[1]] = 0
        elif action[0] == 'capture-right':
            new_state[actions[1] + 4] = 1
            new_state[actions[1]] = 0
        elif action[0] == 'capture-left':
            new_state[actions[1] + 5] = 1
            new_state[actions[1]] = 0
    return new_state

def is_terminal(state):
    # get the current players move
    turn = toMove(state)

    # if it is whites turn
    if turn == 1:
        if state[1] == 1 and state[2] == 1 and state[3] == 1:
            return True
    # if it is blacks turn
    elif turn == -1:
        if state[7] == -1 and state[8] == -1 and state[9] == -1:
            return True
        
    # get all the possible actions for current state
    possible_actions = actions(state)

    # if there is a draw
    if not possible_actions:
        return True
    
    # if the opponent has moves left, return false
    opponent = PLAYERS - {turn}
    for action in possible_actions:
        if action[0] == opponent:
            return False
    # if the opponent has no moves return true
    return True


def utility(state):
    # if the state is a draw, return 0
    possible_actions = actions(state)
    if not possible_actions:
        return 0
    # if the state is a win return 1, otherwise return -1
    if is_terminal(state):
        return 1
    else:
        return -1

INITIAL_STATE = [0, -1, -1, -1, 0, 0, 0, 1, 1, 1]

PLAYERS = set([-1, 1])

# helper function to get the index of the current square
def get_index(i):
    if i < 4:
        return [0, i - 1]
    elif i < 7:
        return [1, i - 4]
    elif i < 10:
        return [2, i - 7]