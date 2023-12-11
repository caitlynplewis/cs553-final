
# Takes in a csv and produces a heatmap with col 1,2,3 being x,y,z coordinates

# Simple example to try and get familiar with some of useful tools

import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def load_data():
	data = pd.read_csv("export.csv")
	# print(sorted(data['WAFER_ROW'].unique()))
	# print(sorted(data['WAFER_COLUMN'].unique()))
	return data

def count_die(data, press=None, color=None ):
	y = sorted(data['WAFER_ROW'].unique())
	x = sorted(data['WAFER_COLUMN'].unique())
	df = pd.DataFrame(0, index=x, columns=y)
	for index, row in data.iterrows():
		df[row['WAFER_ROW']][row['WAFER_COLUMN']] += 1

	return df



def display_3D_heatmap(df):

	x = df.columns
	y = df.index
	# z = df
	X, Y = np.meshgrid(x, y)

	print(len(x))
	print(len(y))
	


	# DataAll1D = np.loadtxt("test_data.csv", delimiter=",", skiprows=1)
	# create 2d x,y grid (both X and Y will be 2d)
	# X, Y = np.meshgrid(DataAll1D[:,0], DataAll1D[:,1])

	# Z = np.tile(df, (len(df), 1))

	# repeat Z to make it a 2d grid
	# Z = np.tile(DataAll1D[:,2], (len(DataAll1D[:,2]), 1))

	Z = df
	print(len(Z))

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	# for other color options, try between viridis, plasma, inferno, magma, cividis 
	ax.plot_surface(X, Y, Z, cmap='plasma')

	# for single colors, use Greys, Blues, Purples, etc.
	# ax.plot_surface(X, Y, Z, cmap='Reds')

	# greyscale
	# ax.plot_surface(X, Y, Z, cmap='binary')

	# "no color"
	# ax.plot_surface(X, Y, Z)

	plt.show()



def display_2D_heatmap(df):
	
	x = df.columns
	y = df.index
	z = df
	X, Y = np.meshgrid(x, y)

	fig, ax = plt.subplots()
	hm = sn.heatmap(data = df, cmap="hot")

	# rax = ax.inset_axes([0.0, 0.0, 0.12, 0.2])
	# check = CheckButtons(
	#     ax=rax,
	#     labels=["One", "Two", "Three"],
	#     actives=[True, False, True]
	# )
    
	# def callback(label):
	#     pass

	# check.on_clicked(callback)

	plt.show()


def main():
	data = load_data()
	print(data['WP_NAME'].unique())
	press = input("Choose a press: ")
	# press = "RS31" # For ease of development

	pressdata = data[data['WP_NAME'] == press]
	df = count_die(pressdata)

	# display_2D_heatmap(df)
	display_3D_heatmap(df)


if __name__ == "__main__":
	main()