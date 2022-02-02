import matplotlib.pyplot as p
import matplotlib.cm as cm
from matplotlib.colors import LogNorm
import numpy as np
import hyperspy.api as hs
import atomap.api as am
import pathlib as Path

path = "4DSTEM/Datos/s_adf_IFFT.tif"

s = hs.load(path)

s_peaks = am.get_feature_separation(s, separation_range=(2, 20), show_progressbar=True)

atom_positions = am.get_atom_positions(s, separation=3)

sublattice = am.Sublattice(atom_positions, image=s.data)

N = len(sublattice.x_position)

pos = np.zeros((N,3))
distances = np.zeros(N)
neighbors = np.zeros(6)
for i in range(0,N):
    pos[i][0] = sublattice.x_position[i]
    pos[i][1] = sublattice.y_position[i]
    pos[i][2] = np.sqrt(pos[i][0]**2 + pos[i][1]**2)
for j in range(0,N):
    posp = np.zeros(N)
    for k in range(0,N):
        posp[k] = abs(pos[j][2] - pos[k][2])
    for l in range(0,6):
        minValue = posp[0]
        minIndex = 0
        for m in range(0,len(posp)):
            if posp[m] < minValue:
                minValue = posp[m]
                minIndex = m
        neighbors[l] = minValue
        posp = np.delete(posp, minIndex)
    distances[j] = np.mean(neighbors)
x = pos[:,0]
y = pos[:,1]
z = distances

x1 = []
y1 = []
z1 = []

for i in range(0, N-1):
    if x[i] > 20 and x[i] < 260 and y[i] > 20 and y[i] < 260:
        x1.append(x[i])
        y1.append(y[i])
        z1.append(z[i])
        

fig, ax = p.subplots()
sc = ax.scatter(x, y, c=z)
cbar = fig.colorbar(sc)
p.show()
