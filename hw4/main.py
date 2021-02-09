import sys
import truss

# print instruction when not enough arguments given
if len(sys.argv) not in [3,4]:
	print("Usage:\n$ python3 main.py [joints file] [beams file] [optional plot output file]")
	sys.exit(0)

fjoints, fbeam = sys.argv[1:3]
fplot = None
if len(sys.argv) == 4:
	fplot = sys.argv[3]

a = truss.Truss(fjoints, fbeam, fplot)

print(a)