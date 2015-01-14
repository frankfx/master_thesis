import matplotlib.pyplot as plt

plt.matplotlib.matplotlib_fname()
plt.plot([1,2,3,4])
plt.ylabel('some numbers')
plt.show()

from pylab import *

t = arange(0.0, 2.0, 0.01)
s = sin(2*pi*t)
plot(t, s)

xlabel('time (s)')
ylabel('voltage (mV)')
title('About as simple as it gets, folks')
grid(True)
savefig("test.png")
show()