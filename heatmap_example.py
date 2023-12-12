
# Takes in a csv and produces a heatmap with col 1,2,3 being x,y,z coordinates

# Simple example to try and get familiar with some of useful tools

import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.colors as colors
import matplotlib.cm as cm

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

	data_array = np.array(df)

	x_data, y_data = np.meshgrid(np.arange(data_array.shape[1]), np.arange(data_array.shape[0]))

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	# Time permitting, add in buttons to pick between die colors and different presses

	# Title
	plt.title('Printing Press Dies')

	# Axes labels
	ax.set_xlabel('Wafer Row')
	ax.set_ylabel('Wafer Column')
	ax.set_zlabel('Die Count')

	x_data = x_data.flatten()
	y_data = y_data.flatten()
	z_data = data_array.flatten()

	print("Color schemes: roygbiv, viridis, plasma, inferno, magma, cividis, Greys, Blues, Purples, binary, none")
	press = input("For more color scheme options, refer to https://matplotlib.org/stable/users/explain/colors/colormaps.html: ")

	if press == "none":
		ax.bar3d(x_data, y_data, np.zeros(len(z_data)), 1, 1, z_data)
	else:	

		if(press == "roygbiv"):
			# Adds full range of color 
			offset = z_data + np.abs(z_data.min())
			fracs = offset.astype(float)/offset.max()
			norm = colors.Normalize(fracs.min(), fracs.max())
			colored = cm.jet(norm(fracs))

		else:
			# Old color schemes
			cmap = cm.get_cmap(press)
			norm = colors.Normalize(vmin=min(z_data), vmax=max(z_data))
			colored = cmap(norm(z_data))


		ax.bar3d(x_data, y_data, np.zeros(len(z_data)), 1, 1, z_data, color=colored )


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