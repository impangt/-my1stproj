import numpy as np
import matplotlib.pyplot as plt

t = np.arange(-1, 2, .01)
s = np.sin(2*np.pi*t)

# draw a thick blue vline at x=0 that spans the upper quadrant of
# the yrange
# l = plt.axvline(x=1, ymax=1/2, ymin=0.0, linewidth=8, color='#1f77b4')

lx=[1,1]
ly=[0,0.6]
plt.plot(lx, ly, linewidth=8, color='#1f77b4')

plt.axis([0, 2, 0, 2])

plt.show()