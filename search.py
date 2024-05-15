# PART 2

from formalization import toMove, is_terminal, actions, result, utility

def min_value(state):
    if is_terminal(state):
        return utility(state), None
    v = float('inf')
    for action in actions(state):
        v2, a2 = max_value(result(state, action))
        if v2 < v:
            v, move = v2, action
    return v, move 

def max_value(state):
    if is_terminal(state):
        return utility(state), None
    v = float('-inf')
    for action in actions(state):
        v2, a2 = min_value(result(state, action))
        if v2 > v:
            v, move = v2, action
    return v, move

def minimax_search(state):
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
            policy_table[state_to_string(state)] = None
        else:
            policy_table[state_to_string(state)] = minimax_search(state)
            for action in actions(state):
                next_state = result(state, action)
                if state_to_string(next_state) not in visited:
                    states.append(next_state)

    return policy_table


def state_to_string(state):
    str_rep = ''
    for s in state:
        str_rep += str(s)
    return str_rep

