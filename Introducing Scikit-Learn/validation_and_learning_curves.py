
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import validation_curve
from sklearn.model_selection import learning_curve
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set()

def polynomial_regression(degree = 2, **kwargs):
    return make_pipeline(PolynomialFeatures(degree), LinearRegression(kwargs))

def make_data(N, err = 1.0, rseed = 1):
    range = np.random.RandomState(rseed)
    X = range.rand(N, 1) ** 2
    y = 10 - 1. / (X.ravel() + 0.1)
    if err > 0:
        y += err * range.randn(N)
    return X, y

def visualize_data(X, y, x_test):
    plt.scatter(X.ravel(), y, color = 'black')
    axis = plt.axis()
    for degree in [1, 3, 5]:
        y_test = polynomial_regression(degree).fit(X, y).predict(x_test)
        plt.plot(x_test.ravel(), y_test, label = 'degree={0}'.format(degree))
    plt.xlim(-0.1, 1.0)
    plt.ylim(-2, 12)
    plt.legend(loc='best')
    plt.show()

def validate_model(X, y):
    degree = np.arange(0, 21)
    train_score, val_score = validation_curve(polynomial_regression(), X, y, 'polynomialfeatures__degree', degree, cv = 7)
    plt.plot(degree, np.median(train_score, 1), color = 'blue', label = 'training score')
    plt.plot(degree, np.median(val_score, 1), color = 'red', label = 'validation score')
    plt.ylim(0, 1)
    plt.xlabel('degree')
    plt.ylabel('score')
    plt.legend(loc = 'best')
    plt.show()
    return train_score, val_score

def best_model(x, y, x_test, degree):
    plt.scatter(x.ravel(), y)
    lim = plt.axis()
    y_test = polynomial_regression(degree).fit(x, y).predict(x_test)
    plt.plot(x_test.ravel(), y_test)
    plt.axis(lim)
    plt.show()

def compare(x2, y2, train_score, val_score):
    degree = np.arange(21)
    train_score2, val_score2 = validation_curve(polynomial_regression(), x2, y2, 'polynomialfeatures__degree', degree, cv = 7)
    plt.plot(degree, np.median(train_score2, 1), color = 'blue', label = 'training score')
    plt.plot(degree, np.median(val_score2, 1), color = 'red', label = 'validation score')
    plt.plot(degree, np.median(train_score, 1), color = 'blue', alpha = 0.3, linestyle = 'dashed')
    plt.plot(degree, np.median(val_score, 1), color = 'red', alpha = 0.3, linestyle = 'dashed')
    plt.legend(loc = 'lower center')
    plt.ylim(0, 1)
    plt.xlabel('degree')
    plt.ylabel('score')
    plt.show()

def plot_learning_curve(x, y):
    fig, ax = plt.subplots(1, 2, figsize = (16, 6))
    fig.subplots_adjust(left = 0.0625, right = 0.95, wspace = 0.1)
    for i, degree in enumerate([2, 9]):
        N, train_lc, val_lc = learning_curve(polynomial_regression(degree), x, y, cv = 7, train_sizes = np.linspace(0.3, 1, 25))
        ax[i].plot(N, np.mean(train_lc, 1), color = 'blue', label = 'training score')
        ax[i].plot(N, np.mean(val_lc, 1), color = 'red', label = 'validation score')
        ax[i].hlines(np.mean([train_lc[-1], val_lc[-1]]), N[0], N[-1], color = 'gray', linestyle = 'dashed')
        ax[i].set_ylim(0, 1)
        ax[i].set_xlim(N[0], N[-1])
        ax[i].set_xlabel('training size')
        ax[i].set_ylabel('score')
        ax[i].set_title('degree = {0}'.format(degree), size = 14)
    plt.legend(loc = 'best')
    plt.show()

def grid_search(x, y, x_test):
    param_grid = {'polynomialfeatures__degree': np.arange(21),
                  'linearregression__fit_intercept': [True, False],
                  'linearregression__normalize': [True, False]}
    grid = GridSearchCV(polynomial_regression(), param_grid, cv = 7)
    grid.fit(x, y)
    # Mejores parametros
    print(grid.best_params_)
    print(grid.best_estimator_)
    # Mejor modelo
    model = grid.best_estimator_
    plt.scatter(x.ravel(), y, color = 'red', label = 'points')
    lim = plt.axis()
    y_test = model.fit(x, y).predict(x_test)
    plt.plot(x_test.ravel(), y_test, color = 'blue', label = 'best model')
    plt.title("Best model found with GridSearchCV", loc = 'center')
    plt.axis(lim)
    plt.legend(loc = 'best')
    plt.show()

x, y = make_data(40)
x_test = np.linspace(-0.1, 1.1, 500)[:, None]

visualize_data(x, y, x_test)
train_score, val_score = validate_model(x, y) 
# Mostramos la mejor opción obtenida
best_model(x, y, x_test, 3)

# Curva de aprendizaje
x2, y2 = make_data(200)
# Comparamos la curva de validacion con los nuevos datos
compare(x2, y2, train_score, val_score)
plot_learning_curve(x2, y2)
# Aplicamos GridSearchCV para encontrar el mejor modelo
grid_search(x, y, x_test)