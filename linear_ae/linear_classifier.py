import numpy as np
import sys
sys.path.append('utils')
import utils.mnist_loader as mnist_loader, vectorized
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import accuracy_score

# vs PCA (vs autoencoder)

def linear_ae(X, y):
    """
    """
    hidden_dim = 10
    #np.dot(X, W)
    # np.dot(np.dot(W, X')', W)-X --> 0
    # learned W
    # encode X to H
    # train linear classification on H

if __name__ == "__main__":
    train, test, val = mnist_loader.load_data()
    X, y = train
    test_X, test_y = test
    lm = LinearRegression()
    lm.fit(X,list(map(vectorized, y)))

    random_guess = np.random.randint(10, size=len(X))
    print("random guess accuracy: ", accuracy_score(y, random_guess))

    y_pred = lm.predict(X) 
    y_pred = [np.argmax(yp) for yp in y_pred]
    print("training accuracy: ", accuracy_score(y, y_pred))
    
    test_y_pred = lm.predict(test_X)
    test_y_pred = [np.argmax(typ) for typ in test_y_pred]
    print("accuracy for test data: ", accuracy_score(test_y, test_y_pred))
