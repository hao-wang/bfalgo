from mnist_loader import load_data, vectorized_result
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import accuracy_score
import numpy as np
import sys
sys.path.append('/Users/hao/Projects/algo_and_all/utils')


def linear_ae(X, y):
    """
    """
    hidden_dim = 10
    # np.dot(X, W)
    # np.dot(np.dot(W, X')', W)-X --> 0
    # learned W
    # encode X to H
    # train linear classification on H


if __name__ == "__main__":
    train, test, val = load_data()
    X, y = train
    lm = Ridge()  # Coefficents small
    # lm = LinearRegression()  # Coefficients much larger
    lm.fit(X, np.array(list(map(lambda x: vectorized_result(x, True), y))))
    print(lm.coef_[0][:10])

    random_guess = np.random.randint(10, size=len(X))
    print("random guess accuracy: ", accuracy_score(y, random_guess))

    y_pred = lm.predict(X)
    y_pred = [np.argmax(yp) for yp in y_pred]
    print("training accuracy: ", accuracy_score(y, y_pred))

    test_X, test_y = test
    test_y_pred = lm.predict(test_X)
    test_y_pred = [np.argmax(typ) for typ in test_y_pred]
    print("accuracy for test data: ", accuracy_score(test_y, test_y_pred))
