"""Adapted from 
Nielsen - 2006 - Neural Networks and Deep Learning
"""
import numpy as np
import sys
sys.path.append('../utils')
from mnist_loader import load_data_wrapper

def nl_func(z, kind='sigmoid'):
    if kind=='sigmoid':
        return 1./(1+np.exp(-z))
    elif kind=='linear':
        return z
    elif kind=='tanh':
        return tahn(z)

def da_dz(a):
    """ a(z) is an element-wise mapping; so the multiplicaton is element-wise too.
    """
    return a*(a-1)

class Network:
    def __init__(self, sizes, nl_kind='sigmoid'):
        self.epochs = 3
        self.batch_size = 50
        self.eta = 0.1
        self.sizes = sizes
        self.nl_kind = nl_kind
        self.weights = [np.random.randn(sizes[isz], sizes[isz+1])
            for isz in range(len(sizes)-1)]
        self.biases = [np.random.randn(1, sz)
            for sz in sizes[1:]] 
        
    def forward(self, a):
        print(a)
        layer_outs = []
        for l in range(len(self.sizes)-1):
            print(l)
            print(a.shape, self.weights[l].shape, self.biases[l].shape)
            z= np.dot(a, self.weights[l])+ self.biases[l]
            a = nl_func(z, kind=self.nl_kind)
            layer_outs.append(a)
        return layer_outs

    def backprop(self, X, y):
        """ Get derivatives for each layer's W and b.
        """
        layer_outs = self.forward(X)

        a_last = layer_outs[-1]
        delta_l = self.loss_prime(a_last, y) * da_dz(a_last)

        nabla_b = [delta_l]
        nabla_w = [np.dot(delta_l, layer_outs[-2])]
        for l in range(len(self.sizes)-2, 1, -1):
            delta_l = np.dot(self.weights[l+1], delta_l) * da_dz(layer_outs[l])
            print(delta_l)
            nabla_b.insert(0, delta_l)
            nabla_w.insert(0, np.dot(delta_l, self.layer_outs[l-1]))

        return nabla_w, nabla_b

    def loss(self, y_calc, y):
        return 0.5*(y_calc - y)*(y_calc-y)

    def loss_prime(self, y_calc, y):
        return y_calc-y

    def SGD(self, X, y):
        """Train with small batches.
        """            
        for i in range(self.epochs):
            print("Epoch %s/%s" % (i, self.epochs))
            idx_shuffle = np.arange(len(X))
            np.random.shuffle(idx_shuffle)
            batch_size = self.batch_size
            idx_batches = [idx_shuffle[i*batch_size:(i+1)*batch_size] for i in range(len(X)//batch_size)]
            for idx_batch in idx_batches:
                nabla_w, nabla_b = self.backprop(X[idx_batch], y[idx_batch])
                for l in range(1, len(self.sizes)):
                    self.weights[-l] -= self.eta*nabla_w[-l]
                    self.biases[-l] -= self.eta*nabla_w[-l]

            self.evaluate(X, y)
            
    def evaluate(self, X, y):
        layer_outs = self.forward(X)    
        y_calc = layer_outs[-1]
        correct = [np.argmax(y_calc[i])==np.argmax(y[i]) for i in range(len(X))]
        print("Correct ratio: %.3f " % sum(correct)/len(X))

if __name__ == "__main__":
    network = Network([784, 30, 10], 'sigmoid')
    training, test, val = load_data_wrapper()
    X = np.array([tr[0] for tr in training])
    y = np.array([tr[1] for tr in training])

    network.SGD(X, y)
