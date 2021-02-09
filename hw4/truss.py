import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import scipy
import warnings

from scipy.sparse.linalg import spsolve
from scipy.sparse import csr_matrix

class Truss(object):
	""" 
	Truss is a class for computing truss beams forces for a given
	configuration of joints and beams.

	By using the equillibrium equations,  we form a linear system and obtain the
	necessary unknowns.
	"""
	def __init__(self, fjoints, fbeam, fplot):
		
		self.fplot = fplot
		self.joints_list, self.beams_list, self.connections = self.read_data(fjoints, fbeam)

		if fplot != None:
			self.PlotGeometry()

		self.compute_forces()

		

	def compute_forces(self):
		"""
		Computes the beam forces and support forces by formming a sparce linear system
		Populates self.beam_forces variable  
		"""
		# form CSR for the sparse linear system
		vals = []
		col_idx = []
		row_idx = [0]
		njoints = len(self.joints_list)
		nbeam = len(self.beams_list)
		f = [0]*(2*njoints)
		nR = 0

		for i  in range(len(self.connections)):
			R = int(self.joints_list[i][4])
			if R == 1:
				nR += 1
			f[2*i] = self.joints_list[i][2]
			f[2*i+1] = self.joints_list[i][3]

			ikj_row = self.connections[i]
			# sort elements in the increasing order of the beam index
			ikj_row.sort(key = lambda x: x[0])
			thetas = []
			# populate equations for the x component
			for k, j in ikj_row:
				# consider all joints j connected to joint i
				theta_ij = self.get_angle(self.joints_list[i][:2], self.joints_list[j][:2])
				thetas = thetas + [theta_ij]
				vals = vals + [np.cos(theta_ij)]
				col_idx  = col_idx + [k]
			if R == 1:
				vals = vals + [1]
				col_idx = col_idx + [nbeam + 2*(nR - 1)]
			row_idx = row_idx + [row_idx[-1] + len(ikj_row)+ R]

			# populate equations for the y component
			for idx, (k, j) in enumerate(ikj_row):
				# consider all joints j connected to joint i
				theta_ij = thetas[idx]
				vals = vals + [np.sin(theta_ij)]
				col_idx  = col_idx + [k]
			if R == 1:
				vals = vals + [1]
				col_idx = col_idx + [nbeam + 2*(nR - 1)+1]
			row_idx = row_idx + [row_idx[-1] + len(ikj_row)+ R]

		# solve sparse system Ax=f
		A = csr_matrix((vals, col_idx, row_idx), shape=(2*njoints, nbeam+2*nR))
		# Catch warnings as exceptions
		warnings.filterwarnings('error')
		try: 
			x = spsolve(A, f)
		except Warning as e:
		    raise RuntimeError("Cannot solve the linear system, unstable truss?")
		    sys.exit(2)
		except ValueError:
			raise RuntimeError("Truss geometry not suitable for static equilbrium analysis")
			sys.exit(3)

		# remove minuses in from of 0's
		self.beam_forces = np.around(x[:nbeam], decimals=3)
		signs = np.sign(self.beam_forces)
		self.beam_forces = np.multiply(signs, np.abs(self.beam_forces))


	def read_data(self, fjoints, fbeam):
		""" Reads data from joints file and beam file
			Returns the output lists of tuples 
			Joints and beams start from 1 and continue to increase 
			consecutively; and list of neighboring joints
			joints_list[i] = (xi, yi, Fix, Fiy, Ri!=0)
			beams_list[k] = (i,j)
			connections[i] = [(k,j)]
		"""
		joints_list = []
		beams_list = []

		with open(fjoints, "r") as f:
			f.readline()
			for i, line in enumerate(f):
				# i: (xi, yi, Fix, Fiy, Ri!=0)
				joints_list = joints_list + [tuple(map(float, line.split()))[1:]]

		# list of neighbors for every joint
		connections = [-1]*len(joints_list)

		with open(fbeam, "r") as f:
			f.readline()
			for k, line in enumerate(f):
				i,j = [ v-1 for v in map(int, line.split())][1:]
				if connections[i] == -1:
					connections[i] = [(k, j)]
				else:
					connections[i] = connections[i] + [(k,j)]
				if connections[j] == -1:
					connections[j] = [(k,i)]
				else:
					connections[j] = connections[j] + [(k,i)]
				# k: (i,j)
				beams_list = beams_list + [(i,j)]

		return joints_list, beams_list, connections


	def get_angle(self, x1, x2):
		"""
		Returns the angle of inclination of the beam
		Used to make the beam force parallel to the beam
		"""
		v1 = np.array([x2[0]-x1[0], x2[1]-x1[1]])
		v1 = v1 / np.linalg.norm(v1)
		v2 = np.array([1, 0])
		dot = np.dot(v1, v2)
		theta = np.arccos(dot)
		return theta


	def __repr__(self):
		"""
		Return the beam force information
		"""
		output = "Beam       Force\n"
		output += "-"*17+"\n"
		for k in range(self.beam_forces.shape[0]):
			output += "%4d    % -.3f\n"%(k+1, self.beam_forces[k])
		return output

	def PlotGeometry(self):
		"""
		Plot joints and beams and stores them into a file
		"""
		for i,j in self.beams_list:
			x = [self.joints_list[i][0], self.joints_list[j][0]]
			y = [self.joints_list[i][1], self.joints_list[j][1]]
			plt.plot(x, y, 'm')
		plt.axis('equal')
		plt.savefig(self.fplot)

