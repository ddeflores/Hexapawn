# PART 2

from formalization import is_terminal, actions, result, utility

def min_value(state):
    # if the state is terminal, return its utility
    if is_terminal(state):
        return utility(state), None
    
    # otherwise, calculate value for each action
    v = float('inf')
    for action in actions(state):
        v2, a2 = max_value(result(state, action))
        if v2 < v:
            v, move = v2, action
    
    # return the minimized value
    return v, move 

def max_value(state):
    # if the state is terminal, return its utility
    if is_terminal(state):
        return utility(state), None
    
    # otherwise, calculate the value for each action
    v = float('-inf')
    for action in actions(state):
        v2, a2 = min_value(result(state, action))
        if v2 > v:
            v, move = v2, action

    # return the maximized value
    return v, move

def minimax_search(state):
    # find and return the move with the best value for the given state
    value, move = max_value(state)
    return move


def create_policy_table(start_state):
    policy_table = {}
    states = [start_state]
    visited = set()

    while states:
        state = states.pop()
        visited.add(state_to_string(state))

        if is_terminal(state):
            policy_table[state_to_string(state)] = [0] * 9  # No valid moves
        else:
            best_move = minimax_search(state)
            move_vector = [0] * 9
            possible_moves = actions(state)
            for i, move in enumerate(possible_moves):
                if move == best_move:
                    move_vector[i] = 1  # Ideal move
                else:
                    move_vector[i] = 0  # Non-ideal move

            policy_table[state_to_string(state)] = move_vector

            for action in possible_moves:
                next_state = result(state, action)
                if state_to_string(next_state) not in visited:
                    states.append(next_state)

    return policy_table


# helper function to convert a state into its string representation for hashing
def state_to_string(state):
    str_rep = ''
    for s in state:
        str_rep += str(s)
    return str_rep
