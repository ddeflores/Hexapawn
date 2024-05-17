# PART 4

import math
from formalization import utility

def classify(instance, inputs):
    for input in inputs:
        for i in range(len(instance[0])):
            instance[1][i] = sigmoid_activation(input)
    return instance

def sigmoid_activation(input):
    x = utility(input)
    output = 1 / (1 + (math.e) ** -x)
    return output

def relu_activation(input):
    x = utility(input)
    output = max(0, x)
    return output
