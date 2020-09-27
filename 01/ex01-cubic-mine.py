import matplotlib.pyplot as plt
import numpy as np

x = np.arange(-5, 5, 0.1)    # -50 <= 0 <= 50

y = x**3 + x**2 - 8*x -12    # f(x) = x^3 + x^2 - 8x -12

plt.plot(x, y)
plt.show()