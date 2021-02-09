import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import os
import sys
from scipy.sparse import coo_matrix 

if len(sys.argv) != 3:
	print("Usage:\n$ python3 postprocess.py <input conditions file> <solution file>")
	sys.exit(0)

input_file, sol_file = sys.argv[1:3]

with open(input_file, "r") as f:
	length, width, h = map(float, f.readline().strip().split())
	Tc, Th = map(float, f.readline().strip().split())


m = int(length/h)
n = int(width/h)

# Organize the solution vector into a matrix and add boundary values
res = np.zeros((m,n))

with  open(sol_file, "r") as f:
	for k, line in enumerate(f.readlines()):
		val = float(line)
		i = k % (m-1)
		j = k // (m-1)
		res[i,j+1] = val

for i in range(m-1):
	res[:,0] = -Tc*(np.exp(-10*(i*h - length/2)**2)-2)
res[:,n-1] = Th
res[m-1,:] = res[0, :] 
res = res.transpose()

print("Input file processed: %s"%input_file)

mean_temp = res[:,:-1].mean()
print("Mean temperature: %.5f"%mean_temp)

# find interpolated values
ys = np.arange(0, width, h)
interps = np.zeros(m)
for i in range(m):
	x = i*h
	interps[i] = np.interp(mean_temp, res[:, i], ys)
ixs = np.arange(0, length, h)

y, x = np.mgrid[slice(0, width, h),
                slice(0, length, h)]

fig, ax = plt.subplots(1,1)
c = ax.pcolor(x, y, res, cmap='jet', vmin=res.min(), vmax=res.max())
ax.plot(ixs, interps, c="k")
ax.set_title('Pipe temperature')
ax.set_xlabel("X")
ax.set_ylabel("Y")
fig.colorbar(c)
ax.set_aspect('equal')
#fig.savefig("temperature1.png")
plt.show()


