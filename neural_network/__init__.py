"""Adapted from 
Nielsen - 2006 - Neural Networks and Deep Learning
"""
import numpy as np

def nl_func(z, kind='sigmoid'):
    if kind=='sigmoid':
        return 1./(1+np.exp(-z))
    elif kind=='linear':
        return z
    elif kind=='tanh':
        return tahn(z)

class Network:
    def __init__(self, sizes, nl_kind='sigmoid'):
        self.sizes = sizes
        self.nl_kind = nl_kind
        self.weights = [np.random.randn((sizes[isz], sizes[isz+1]))
            for isz in range(len(sizes)-1)]
        self.biases = [np.random.randn(sz)
            for sz in sizes[1:]] 
        
    def forward(self, a):
        for l in range(len(self.sizes)-1):
            a = nl_func(np.dot(a, self.weights[l]) + self.biases[l],
                kind=self.nl_kind)

        return a

    def backprop(self):
        """ Get derivatives for each layer's W and b.
        """
        nabla_b = []
        nabla_w = []
        for l in range(1, len(sizes)):
            pass

    def loss(self, X, y):
        y_calc = forward(self, X)
        return (y_calc - y)

            


     