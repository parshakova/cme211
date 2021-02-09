import numpy as np

import sys

# print instruction when not enough arguments given
if len(sys.argv) != 3:
	print("Usage:\n$ python3 checksoln.py <maze file> <solution file>")
	sys.exit(0)

maze_file, sol_file = sys.argv[1:3]

f = open(maze_file, "r")
m,n = map(int, f.readline().strip().split())

maze = np.zeros((m,n))

# create maze from file
# 1 for wall  location and 0 for path
for line in f:
	i,j = map(int, line.strip().split())
	maze[i,j] = 1
f.close()

flag = True
# verify whether the solution is correct
f = open(sol_file, "r")
i1,j1 = map(int, f.readline().strip().split())
if i1 !=0:
	print("Solution is invalid!")


def is_valid(i1,j1,i2,j2,m,n):
	"""
	Check if each position change is valid 
	(i.e. you move one position at a time, don’t go through a wall, 
	and stay within the bounds of the maze)
	"""	
	if not  (0 <= i2 < m) and(0 <= j2 < n):
		return False
	dx = np.abs(i1-i2)
	dy = np.abs(j1-j2)
	if (dx+dy == 0) or (dx+dy > 1):
		return False
	else:
		return True

for k, line in enumerate(f):
	i2,j2 = map(int, line.strip().split())
	if not is_valid(i1,j1,i2,j2,m,n):
		flag = False
		break
	if maze[i2,j2] == 1:
		flag = False
		break
	i1,j1 = i2, j2
	
if i2 != m-1:
	flag = False
		
f.close()

if flag:
	print("Solution is valid!")
else:
	print("Solution is invalid!")