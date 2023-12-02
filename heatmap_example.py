
# Takes in a csv and produces a heatmap with col 1,2,3 being x,y,z coordinates

# Simple example to try and get familiar with some of useful tools

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

DataAll1D = np.loadtxt("test_data.csv", delimiter=",", skiprows=1)
# create 2d x,y grid (both X and Y will be 2d)
X, Y = np.meshgrid(DataAll1D[:,0], DataAll1D[:,1])

# repeat Z to make it a 2d grid
Z = np.tile(DataAll1D[:,2], (len(DataAll1D[:,2]), 1))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='hot')
plt.show()
