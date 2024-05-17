# PART 6

from formalization import toMove, utility, actions, result, is_terminal, INITIAL_STATE
from search import create_policy_table
from graph import Graph
import random


# create a network given a number of layers and nodes, and alpha that defaults to 0.01
def create_network(num_layers, num_nodes_per_layer):

    # initialize the graph structure and list of all neurons
    graph = Graph()
    neurons = []

    # add the input neurons
    input_neurons = []
    for i in range(10):
        input_neurons.append(graph.add_neuron())
    neurons.append(input_neurons)

    # add hidden layers
    for i in range(num_layers):
        hidden_neurons = []
        for j in range(num_nodes_per_layer):
            hidden_neurons.append(graph.add_neuron(random.choice(['sigmoid', 'relu'])))
    neurons.append(hidden_neurons)

    # add output neurons
    output_neurons = []
    for i in range(9):
        output_neurons.append(graph.add_neuron('sigmoid'))
    neurons.append(output_neurons)

    # connect all of the layers
    for i in range(len(neurons) - 1):
        for from_neuron in neurons[i]:
            for to_neuron in neurons[i + 1]:
                graph.add_edge(from_neuron, to_neuron, random.uniform(-0.5, 0.5))

    # return the connected neural network
    return graph

# train the network based on training data (a policy table), a number of epochs to train for (defaults to 1000), and alpha (defaults to 0.01)
def train_network(graph: Graph, training_data, epochs=1000, learning_rate=0.01):
    for epoch in range(epochs):
        for key, expected_output in training_data.items():
            # turn the string representation of the state into a state ready for processing
            state = string_to_state(key)
            # classify the state
            graph.classify(state)

            #update the weights
            graph.update_weights(expected_output, learning_rate)

# turn an output from a neuron into an action
def output_to_action(state, output):
    # get all possible moves for the current state
    possible_moves = actions(state)

    # sort each move by its associated confidence in decreasing order
    move_confidences = [(output[i], possible_moves[i]) for i in range(len(possible_moves))]
    sorted_moves = sorted(move_confidences, reverse=True, key=lambda x: x[0])

    # iterate through the sorted moves (highest to lowest confidence) and pick the first one that is possible
    for confidence, move in sorted_moves:
        if move in possible_moves:
            return move

    # if the output is not in the possible moves, return a random move
    return random.choice(possible_moves)



def play_hexapawn(graph: Graph, start_state):
    # start the game with the given state
    state = start_state
    if toMove(state) == 0:
            player = "WHITES"
    else:
        player = "BLACKS"
    print('It is ' + player + ' turn')
    state_to_board(state)

    # continue playing until a player has won, or there is a draw
    while not is_terminal(state):
        # get the output of the current state
        output = graph.classify(state)

        # given an output, turn it into a readable move
        move = output_to_action(state, output)

        # set the state to the result of the networks output move
        state = result(state, move)
        if toMove(state) == 0:
            player = "WHITES"
        else:
            player = "BLACKS"
        if not is_terminal(state):
            print("It is " + player + ' turn')
            state_to_board(state)

    if toMove(state) == 0:
        player = 'White'
    else:
        player = 'Black'
    
    # when the game is over, print how it ended
    print('Game over!')
    state_to_board(state)

# helper function to print the board representation of the state
def state_to_board(state):
    for row in [state[1:4], state[4:7], state[7:10]]:
        print(row)
    print()

# helper function to turn the hashable string representation of a state into an actual state that is ready for input
def string_to_state(string_representation):
    # initialize the state with the move
    state = [int(string_representation[0])]

    # parse the string into a state and return it
    i = 1
    while i < len(string_representation):
        if string_representation[i] == '-':
            state.append(-1)
            i += 1
        else:
            state.append(int(string_representation[i]))
        i += 1
    return state

# helper function to choose a start state for the game
def get_random_state(policy_table):
    # add all non-terminal states to the possible states list, and return a random one
    possible_states = []
    for key in policy_table.keys():
        state = string_to_state(key)
        if not is_terminal(state):
            possible_states.append(state)
    return random.choice(possible_states)

if __name__ == '__main__':
    # make network
    network = create_network(15, 3)

    # fetch training data from initial state
    policy_table = create_policy_table(INITIAL_STATE)

    # train the network
    train_network(network, policy_table)

    # launch a simulation of the game with a random non-terminal state from the policy table
    play_hexapawn(network, get_random_state(policy_table))
