# PART 1

import copy

def toMove(state):
    # return the player in the first index of the state
    return state[0]

def actions(state):
    possible_actions = []
    turn = toMove(state)
    for i in range(1, 10):
        index = get_index(i)
        
        # if it is whites turn and the square has a white piece on it
        # and the piece hasnt reached the end
        if turn == 0 and state[i] == 1 and i > 3:    
            if state[i - 3] == 0:
                possible_actions.append(['advance', index[0], index[1]])
            if state[i - 2] == -1 and (index[1] == 0 or index[1] == 1):
                possible_actions.append(['capture-right', index[0], index[1]])
            if state[i - 4] == -1 and abs(index[0] - get_index(i - 4)[0]) == 1:
                possible_actions.append(['capture-left', index[0], index[1]])

        # if it is blacks turn and the square has a black piece on it
        # and the piece hasnt reached the end
        if turn == 1 and state[i] == -1 and i < 7:
            if state[i + 3] == 0:
                possible_actions.append(['advance', index[0], index[1]])
            if state[i + 2] == 1 and (index[1] == 2 or index[1] == 1):
                possible_actions.append(['capture-right', index[0], index[1]])
            if (index[1] == 0 or index[1] == 1):
                if state[i + 4] == 1 and abs(index[0] - get_index(i + 4)[0]) == 1:
                    possible_actions.append(['capture-left', index[0], index[1]])

    return possible_actions

            

def result(state, action):
    # find out which colors turn it is
    turn = toMove(state)

    # make a deep copy so that the original list isnt changed
    new_state = state_to_board(copy.deepcopy(state))

    '''perform the action based on which colors turn it is'''
    # --> if its whites turn
    if turn == 0:
        if action[0] == 'advance':
            new_state[action[1] - 1][action[2]] = 1
            new_state[action[1]][action[2]] = 0
        elif action[0] == 'capture-left':
            new_state[action[1] - 1][action[2] - 1] = 1
            new_state[action[1]][action[2]] = 0
        elif action[0] == 'capture-right':
            new_state[action[1] - 1][action[2] + 1] = 1
            new_state[action[1]][action[2]] = 0

    # --> if its blacks turn
    elif turn == 1:
        if action[0] == 'advance':
            new_state[action[1] + 1][action[2]] = -1
            new_state[action[1]][action[2]] = 0
        elif action[0] == 'capture-left':
            new_state[action[1] + 1][action[2] + 1] = -1
            new_state[action[1]][action[2]] = 0
        elif action[0] == 'capture-right':
            new_state[action[1] + 1][action[2] - 1] = -1
            new_state[action[1]][action[2]] = 0
            
    # return the new state in the correct form (1d list instead of 2d list)
    return [turn, *new_state[0], *new_state[1], *new_state[2]]

def is_terminal(state):
    # get the current players move
    turn = toMove(state)

    # if either colors pawn has reached the end
    if state[1] == 1 or state[2] == 1 or state[3] == 1:
        return True
    if state[7] == -1 or state[8] == -1 or state[9] == -1:
        return True

    # get all the possible actions for current state
    possible_actions = actions(state)

    # if there is a draw (i.e. no possible moves for the current turn)
    if not possible_actions:
        return True

    return False


def utility(state):
    # if the state is a draw, return 0
    possible_actions = actions(state)
    if not possible_actions:
        return 0
    # if the state is a win return 1, otherwise return 1/2
    if is_terminal(state):
        return 1
    else:
        return 1/2

INITIAL_STATE = [0, -1, -1, -1, 0, 0, 0, 1, 1, 1]

PLAYERS = set([-1, 1])

# helper function to get the index of a piece on the board
def get_index(i):
    if i < 4:
        return [0, i - 1]
    elif i < 7:
        return [1, i - 4]
    elif i < 10:
        return [2, i - 7]

# helper function to transform a 1d state list into a 2d state list for easier value manipulation
def state_to_board(state):
    if len(state) == 10:
        return [state[1:4], state[4: 7], state[7:10]]
    else:
        return [state[0:3], state[3: 6], state[6:9]]
