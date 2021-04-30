"""Adapted from Nielsen - 2006 - Neural Networks and Deep Learning, with array
shape following TensorFlow's convention (None, n_layer_out)
"""
from mnist_loader import load_data, vectorized_result
import numpy as np
import sys
sys.path.append('../utils')


def nl_func(z, kind='sigmoid'):
    if kind == 'sigmoid':
        return 1./(1+np.exp(-z))
    elif kind == 'linear':
        return z
    elif kind == 'tanh':
        return np.tanh(z)


def da_dz(a):
    """ a(z) is an element-wise mapping; so is the multiplicaton.
    """
    return a*(1-a)


class Network:
    def __init__(self, sizes, nl_kind='sigmoid'):
        self.epochs = 3
        self.batch_size = 50
        self.eta =5.0 
        self.sizes = sizes
        self.nl_kind = nl_kind
        self.weights = [np.random.randn(sizes[isz], sizes[isz+1])
                        for isz in range(len(sizes)-1)]
        self.biases = [np.random.randn(1, sz) for sz in sizes[1:]]
        
    def forward(self, a):
        """ Forward pass. Record a for each layer. Note that
        Layer-l corresponds to a[l], weights[l-1], and biases[l-1] (l>=1).
        """
        a = a.reshape(-1, 784)
        layer_outs = [a]
        for layer in range(1, len(self.sizes)):
            z = np.dot(a, self.weights[layer-1]) + self.biases[layer-1]
            a = nl_func(z, kind=self.nl_kind)
            layer_outs.append(a)
        return layer_outs

    def backprop(self, x, y):
        """ Get derivatives for each layer's weight and bias. Most vector
        differentiation analysis happens here.

        Note that Layer-l corresponds to layer_outs[l],
        weights[l-1], and biases[l-1] (l>=1).
        """
        layer_outs = self.forward(x)

        a_L = layer_outs[-1]
        delta_L = self.loss_prime(a_L, y) * da_dz(a_L).T  # (n_L, 1)

        nabla_b = [delta_L.T]  # (1, n_L)
        nabla_w = [np.dot(layer_outs[-2].T, delta_L.T)]  # (n_L-1, n_L)

        delta_next_layer = delta_L
        for layer in range(len(self.sizes)-2, 0, -1):
            delta_l = np.dot(self.weights[layer], delta_next_layer) * \
                        da_dz(layer_outs[layer]).T
            
            # Correction for Video: nabla_xx is kind of a misnomer - they 
            # are the orthogonal of the true nabla's (gradients).
            nabla_b.insert(0, delta_l.T)
            nabla_w.insert(0, np.dot(layer_outs[layer-1].T, delta_l.T))

            delta_next_layer = delta_l

        return nabla_w, nabla_b

    def loss_prime(self, a_L, y):
        return (a_L-y).T

    def SGD(self, X, y):
        """Train with small batches. Get smoothed(averaged) nabla_w & nabla_b,
        then update weights and biases, by training with mini-batches.
        """
        for i in range(self.epochs):
            print("Epoch %s/%s" % (i, self.epochs))
            idx_shuffle = np.arange(len(X))
            np.random.shuffle(idx_shuffle)
            batch_size = self.batch_size
            idx_batches = [idx_shuffle[i*batch_size:(i+1)*batch_size]
                           for i in range(len(X)//batch_size)]

            for idx, idx_batch in enumerate(idx_batches):
                nabla_w = [np.zeros((self.sizes[i], self.sizes[i+1]))
                           for i in range(len(self.sizes)-1)]
                nabla_b = [np.zeros((1, self.sizes[i]))
                           for i in range(1, len(self.sizes))]

                for one_x, one_y in zip(X[idx_batch], y[idx_batch]):
                    nb_w, nb_b = self.backprop(one_x, one_y)
                    nabla_w = [nw + self.eta/batch_size * nbw
                               for (nw, nbw) in zip(nabla_w, nb_w)]
                    nabla_b = [nb + self.eta/batch_size * nbb
                               for (nb, nbb) in zip(nabla_b, nb_b)]

                self.weights = [w-nbw for (w, nbw) in
                                zip(self.weights, nabla_w)]
                self.biases = [b-nbb for (b, nbb) in
                               zip(self.biases, nabla_b)]

                print("Now the {}th batch.".format(idx))
                if idx%50==0:
                    self.evaluate(X, y)
            
    def evaluate(self, X, y):
        layer_outs = self.forward(X)
        y_calc = layer_outs[-1]
        correct = [np.argmax(y_calc[i]) == np.argmax(y[i])
                   for i in range(len(X))]
        print("Correct ratio: %.3f " % (sum(correct)/len(X)))


if __name__ == "__main__":
    network = Network([784, 30, 10], 'sigmoid')
    training, test, val = load_data()
    X = training[0]
    y_raw = training[1]
    y = np.array([vectorized_result(iy, True) for iy in y_raw])
    print(X.shape, y.shape)

    network.SGD(X, y)
