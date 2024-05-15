# PART 3

class Edge:
    def __init__(self, weight, value=0.0, perceived_error=0.0):
        self.weight = weight
        self.value = value
        self.perceived_error = perceived_error

class Neuron:
    def __init__(self):
        self.incoming = []
        self.outgoing = []

    def add_incoming(self, edge):
        self.incoming.append(edge)

    def add_outgoing(self, edge):
        self.outgoing.append(edge)

class Graph:
    def __init__(self):
        self.neurons = []

    def add_neuron(self):
        neuron = Neuron()
        self.neurons.append(neuron)
        return neuron

    def add_edge(self, from_neuron, to_neuron, weight):
        edge = Edge(weight)
        from_neuron.add_outgoing_edge(edge)
        to_neuron.add_incoming_edge(edge)
