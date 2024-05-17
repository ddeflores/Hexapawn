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
    # initialize the policy table as a dictionary
    policy_table = {}

    # initialize a queue of states to process 
    states = [start_state]

    # initialize a set of visited states
    visited = set()

    # while the queue is not empty, process the states
    while states:

        # pop a state off the queue, and add it to the visited set as a string (to save memory)
        state = states.pop()
        visited.add(state_to_string(state))

        # if the state is terminal, there is no move to add to the policy table --> otherwise, process the state
        if is_terminal(state):
            policy_table[state_to_string(state)] = None
        else:
            # find the best move for that state and add it to the policy table
            policy_table[state_to_string(state)] = minimax_search(state)

            # add the result of each possible action in the current state to the queue
            for action in actions(state):
                next_state = result(state, action)
                if state_to_string(next_state) not in visited:
                    states.append(next_state)

    # return the policy table when the queue is empty
    return policy_table

# helper function to convert a state into its string representation for hashing
def state_to_string(state):
    str_rep = ''
    for s in state:
        str_rep += str(s)
    return str_rep
