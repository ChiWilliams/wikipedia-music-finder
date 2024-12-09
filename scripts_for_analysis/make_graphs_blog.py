#make graphs
import numpy as np
import matplotlib.pyplot as plt

LOW = 0.058
MIDDLE = 0.074
HIGH = 0.09

x = np.arange(100)
plt.plot(x,100*(1-(1-LOW)**x), 'r--', label = 'Lower Bound Estimate', linewidth = 2)
plt.plot(x,100*(1-(1-MIDDLE)**x), 'b', label = 'Point Estimate', linewidth = 2)
plt.plot(x,100*(1-(1-HIGH)**x), 'g--', label = 'Upper Bound Estimate', linewidth = 2)
plt.xlabel('Number of Attempts')
plt.ylabel('Probability %')
plt.legend()
plt.title('Probability of hitting a music article within n attempts')
plt.show()