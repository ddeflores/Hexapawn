# PART 3, 4, 5

import math
 
class Edge:
    def __init__(self, from_neuron, to_neuron, weight, value=0.0, perceived_error=0.0):
        self.from_neuron: Neuron = from_neuron
        self.to_neuron: Neuron = to_neuron
        self.weight = weight
        self.value = value
        self.perceived_error = perceived_error

class Neuron:
    def __init__(self, activation_function='sigmoid'):
        self.incoming: list[Edge] = []
        self.outgoing: list[Edge] = []
        self.activation_function = activation_function
        self.output = 0
        self.input_sum = 0
        self.delta = 0

    # add an incoming edge
    def add_incoming(self, edge):
        self.incoming.append(edge)

    # add an outgoing edge 
    def add_outgoing(self, edge):
        self.outgoing.append(edge)

    # get output from a neuron
    def get_output(self):
        for edge in self.incoming:
            self.input_sum += edge.weight * edge.from_neuron.output
        self.output = self.activation_function(self.input_sum)

class Graph:
    def __init__(self):
        self.neurons: list[Neuron] = []

    def add_neuron(self, activation_function='sigmoid'):
        # add a neuron to the graph
        neuron = Neuron(activation_function)
        self.neurons.append(neuron)
        return neuron

    def add_edge(self, from_neuron: Neuron, to_neuron: Neuron, weight):
        # add an edge from one neuron to another
        edge = Edge(from_neuron, to_neuron, weight)
        from_neuron.add_outgoing(edge)
        to_neuron.add_incoming(edge)

    def classify(self, inputs):
        # start with initial inputs
        for i, input in enumerate(inputs):
            self.neurons[i].output = input
        
        # process the next neurons
        for neuron in self.neurons[len(inputs):]:
            neuron.get_output()
        
        # get all of the outputs from the neurons
        outputs = []
        for neuron in self.neurons[len(inputs):]:
            outputs.append(neuron.output)

        return outputs
    
    def update_weights(self, outputs: list[Neuron]):
        # output layer deltas
        output_neurons: list[Neuron] = self.neurons[-len(outputs)]
        for neuron, expected in zip(output_neurons, outputs):
            y_hat = neuron.output
            error = y_hat - expected
            delta = 2 * error * neuron.activation_function(neuron.input_sum)
            neuron.delta = delta

        # hidden layer deltas
        for neuron in reversed(self.neurons[:-len(outputs)]):
            if neuron.activation_function == 'sigmoid':
                derivative = sigmoid_derivative(neuron.input_sum)
            else:
                derivative = relu_derivative(neuron.input_sum)

            delta_sum = 0
            for edge in neuron.outgoing:
                delta_sum += edge.to_neuron.delta * edge.weight
            neuron.delta = delta_sum * derivative

        # update all of the weights
        for neuron in self.neurons:
            for edge in neuron.incoming:
                edge.weight -= edge.from_neuron.output * neuron.delta

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def relu(x):
    return max(0, x)

def sigmoid_derivative(x):
    sig = sigmoid(x)
    return sig * (1 - sig)

def relu_derivative(x):
    return 1 if x > 0 else 0