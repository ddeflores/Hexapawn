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

# create a policy table from the initial state
def create_policy_table(start_state):
    # initialize policy table as a dict
    policy_table = {}

    #initialize states queue
    states = [start_state]

    # initialize visited states set
    visited = set()

    # while the queue is not empty, process the states
    while states:
        # pop a state from the queue for processing
        state = states.pop()

        # add the state to the visited set in string form to save space
        visited.add(state_to_string(state))

        # if the state is terminal, append a vector of 0s
        if is_terminal(state):
            policy_table[state_to_string(state)] = [0] * 9  # No valid moves
        else:
            # find the best move for the given state
            best_move = minimax_search(state)

            # initialize move vector to 0s
            move_vector = [0] * 9

            # get the possible moves for the given state
            possible_moves = actions(state)

            # iterate through every move, adjusting the vector as you go
            for i, move in enumerate(possible_moves):
                # 1 means it is an ideal move
                if move == best_move:
                    move_vector[i] = 1
                # 0 means it is not
                else:
                    move_vector[i] = 0

            # hash the state in the table and record its value as the move vector
            policy_table[state_to_string(state)] = move_vector

            # add the resulting states for all possible actions to the queue
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
