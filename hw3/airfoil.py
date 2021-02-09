import glob
import math
import os
import sys

class Airfoil:
    def __init__(self, inputdir):
        # initialize the data folder
        self.inputdir = inputdir
        self.output = ""
        if not os.path.exists(self.inputdir):
            raise RuntimeError("input directory does not exist")
        self.get_lift_coefficients()


    def get_files(self):
        # Return files from the folder
        files = glob.glob(self.inputdir + '/*.dat')
        xy_file = self.inputdir + '/xy.dat'
        if not xy_file not in files:
            raise RuntimeError("file with panel locations does not exist")
        flag = False
        if self.inputdir[-1] != '/':
            alpha_file = self.inputdir + '/alpha'
        else:
            alpha_file = self.inputdir + 'alpha'
        for f in files:
            if alpha_file in f:
                flag  = True
                break
        if not flag:
            raise RuntimeError("file with pressure coefficients does not exist")
        return files

    def parse_name(self, filename):
        # Return angle of attach from file name
        try:
            i1 = filename.find('alpha')
            i2 = filename.find('.dat')
            alpha = float(filename[i1+len('alpha'):i2])
        except:
            raise RuntimeError("error in file %s"%filename)
        return  alpha

    def get_cx_cy(self, chord, dxy, cp):
        # Return component of lift coefficient from given panel
        cx = (-cp*dxy[1])/chord
        cy = (cp*dxy[0])/chord
        return cx, cy

    def abs(self, x):
        # return absolute value
        if x < 0:
            x = -1*x
        return x

    def read_cp(self, filename):
        # Return pressure coefficients for the panel locations

        with open(filename) as f:
            content = f.readlines()
        content = [x.strip() for x in content[1:]]
        cp_data = [0]*len(content)
        idx_stag = 0

        for i in range(len(content)):
            try:
                cp_data[i] = float(content[i].split()[0])
                if i > 0:
                    # find index of element closest to 1
                    if self.abs(1-cp_data[i]) < self.abs(1-cp_data[idx_stag]):
                        idx_stag = i
            except:
                raise RuntimeError("error in file %s"%filename)

        return cp_data, idx_stag

    def read_dxy(self, filename):
        # Return deltas for the panel locations
        with open(filename) as f:
            content = f.readlines()
        chord = 0
        content = [x.strip() for x in content]
        self.output += "Test case: %s\n"%content[0]
        content = content[1:]

        xy_diff = [0]*(len(content)-1)
        xy_data = [0]*len(content)
        x1s = [0]*len(content)

        for i in range(len(content)-1):
            try:
                x1, y1 = map(float, content[i].split())
                x2, y2 = map(float, content[i+1].split())
                xy_diff[i] = (x2-x1, y2-y1)
                xy_data[i] = (x1, y1)
                x1s[i] = x1
            except:
                raise RuntimeError("error in file with panel locations %s"%filename)

        xy_data[-1] = (x2, y2)
        x1s[-1] = x2
        x1s.sort()
        chord = x1s[-1] - x1s[0]
        return xy_diff, xy_data, chord

    def get_lift_coefficients(self):
        # Return all lift coefficients
        files = self.get_files()
        cp_dict = {}
        for fname in files:
            if 'xy.dat' in fname:
                xy_diff, xy_data, chord = self.read_dxy(fname)
            elif 'alpha' in fname:
                alpha = self.parse_name(fname)
                cp_dict[alpha] = self.read_cp(fname)
        self.output += "alpha     cl        stagnation pt\n----- ------- --------------------------\n"
        cp_cum_dict = {}
        for alpha in sorted(cp_dict.keys()):
            cp_cum_dict[alpha] = [0,0]
            for i, cp in enumerate(cp_dict[alpha][0]):
                dxy = xy_diff[i]
                cx, cy = self.get_cx_cy(chord, dxy, cp)
                cp_cum_dict[alpha][0] += cx 
                cp_cum_dict[alpha][1] += cy
            idx_stag = cp_dict[alpha][1]
            point_stag = ((xy_data[idx_stag][0]+xy_data[idx_stag+1][0])/2.0, (xy_data[idx_stag][1]+xy_data[idx_stag+1][1])/2.0)
            val_stag = cp_dict[alpha][0][idx_stag]
            rad_alpha = math.radians(alpha)
            cl = cp_cum_dict[alpha][1]*math.cos(rad_alpha) - cp_cum_dict[alpha][0]*math.sin(rad_alpha)
            self.output += "%2.2f  %2.4f  (%2.4f,  %2.4f)  %2.4f\n"%(alpha, cl, point_stag[0], point_stag[1], val_stag)

    def __repr__(self):
        return self.output





