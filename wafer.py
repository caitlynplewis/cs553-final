import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, CheckButtons

def load_data():
    data = pd.read_csv("export.csv")
    return data

def count_die(data, rows, cols ):
    df = pd.DataFrame(0, index=rows, columns=cols)
    if(len(data) != 0):
        for index, row in data.iterrows():
            df[row['WAFER_COLUMN']][row['WAFER_ROW']] += 1

    return df

def subset_data(data):
    outputs = {}
    visible = {}
    for color in data["PEN_COLOR_NAME"].unique():
        outputs[color] = data[data['PEN_COLOR_NAME'] == color]
        visible[color] = True
    return outputs, visible

def annotate_map(display_data, rows, cols, ax):
    annots = []
    for i in rows:
        for j in cols:
            val = display_data.iloc[int(i)-1, int(j)-1]
            text = ax.text(j-1, i-1, val,
                        ha="center", va="center", color="w")
            annots.append(text)
    return annots

def clear_annotations(annots):
    for ann in annots:
        ann.remove()

def matplot_only_heatmap(data):
    fig, ax = plt.subplots()
    subsets, subset_visible = subset_data(data)
    rows = sorted(data['WAFER_ROW'].unique())
    cols = sorted(data['WAFER_COLUMN'].unique())
    z = count_die(data, rows, cols)
    zmax = z.max().max()

    display_data = z

    im = ax.imshow(display_data)
    fig.colorbar(im, ticks=range(0,zmax,5))
    annots = annotate_map(display_data, rows, cols, ax)
    ax.set_aspect(3)

    ####################### Radio button for cmap
    ax_radio = plt.axes([0.0, 0.0, 0.1, 0.25])
    labels = ["viridis", "hot", "plasma", "inferno", "magma", "cividis" ]
    color_button = RadioButtons(ax_radio, labels, activecolor='black')

    def select_color(label):
        im.set_cmap(label)
        fig.canvas.draw()

    color_button.on_clicked(select_color)
    ####################### 

    ####################### Checkboxes for data selection
    activated = [True] * (len(data["PEN_COLOR_NAME"].unique()))
    labels = data["PEN_COLOR_NAME"].unique()
    ax_check = plt.axes([0.0, 0.3, 0.1, 0.3])
    pen_colors = CheckButtons(ax_check, labels, activated)

    def filter_data(label):
        nonlocal annots
        nonlocal im
        clear_annotations(annots)
        subset_visible[label] = not subset_visible[label]
        active_subsets = []
        for k in subsets.keys():
            if subset_visible[k]:
                active_subsets.append(subsets[k])

        display_data = pd.concat(active_subsets)
        display_data = count_die(display_data, rows, cols)

        annots = annotate_map(display_data, rows, cols, ax)
        im = ax.imshow(display_data, vmin=0, vmax=zmax)
        ax.set_aspect(3)
        fig.canvas.draw()

    pen_colors.on_clicked(filter_data)
    ####################### 

    plt.show()

def main():
    data = load_data()
    print(data['WP_NAME'].unique())
    # press = input("Choose a press: ")
    press = "RS31" # For ease of development

    pressdata = data[data['WP_NAME'] == press]
    matplot_only_heatmap(data)


if __name__ == "__main__":
    main()