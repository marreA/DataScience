import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns; sns.set()
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
x = np.array([2, 3, 4])
polynomial = PolynomialFeatures(3, include_bias=False)
result = polynomial.fit_transform(x[:, None])
polynomial_model = make_pipeline(PolynomialFeatures(7), LinearRegression())
rng = np.random.RandomState(1)
x = 10 * rng.rand(50)
y = np.sin(x) + 0.1 * rng.randn(50)
polynomial_model.fit(x[:, np.newaxis], y)
x_fit = np.linspace(0, 10, 1000)
y_fit = polynomial_model.predict(x_fit[:, np.newaxis])
plt.scatter(x, y)
plt.plot(x_fit, y_fit)
plt.show()
