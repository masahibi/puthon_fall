import matplotlib.pyplot as plt    # 未完成
import numpy as np

x = np.arange(-0.05, 0.05, 0.01)

y = np.sqrt(1**2 - x**2)

plt.plot(x, y)
plt.show()