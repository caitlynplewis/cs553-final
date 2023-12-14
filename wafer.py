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
    ax.set_title('Printing Press Die Source Location')
    ax.set_xlabel('Wafer Column')
    ax.set_ylabel('Wafer Row')
    _ , active_colors = subset_data(data)
    active_presses = data['WP_NAME'].unique().tolist()
    rows = sorted(data['WAFER_ROW'].unique())
    cols = sorted(data['WAFER_COLUMN'].unique())
    z = count_die(data, rows, cols)
    zmax = z.max().max()
    annots = []
    im = None

    active_data = data
    display_data = z

    def draw_plot():
        nonlocal im, annots
        clear_annotations(annots)
        im = ax.imshow(display_data)
        annots = annotate_map(display_data, rows, cols, ax)
        ax.set_aspect(4.25)
        fig.canvas.draw()

    draw_plot()
    ####################### Checkboxes for press selection
    activated = [True] * (len(data["WP_NAME"].unique()))
    labels = data["WP_NAME"].unique()
    ax_press = plt.axes([0.0, 0.0, 0.1, 0.3])
    press_picker = CheckButtons(ax_press , labels, activated)
    def press_filter(label):
        nonlocal active_data, display_data
        if label in active_presses:
            active_presses.remove(label)
        else:
            active_presses.append(label)
        active_data = all_filters(data, active_presses, active_colors)

        display_data = count_die(active_data, rows, cols)
        draw_plot()

    press_picker.on_clicked(press_filter)
    ####################### Checkboxes for data selection
    activated = [True] * (len(data["PEN_COLOR_NAME"].unique()))
    labels = data["PEN_COLOR_NAME"].unique()
    ax_check = plt.axes([0.0, 0.3, 0.1, 0.3])
    pen_colors = CheckButtons(ax_check, labels, activated)

    def color_filter(label):
        nonlocal display_data, active_data
        active_colors[label] = not active_colors[label]
        active_data = all_filters(data, active_presses, active_colors)
        display_data = count_die(active_data, rows, cols)

        draw_plot()

    pen_colors.on_clicked(color_filter)
    ####################### 

    plt.show()

def all_filters(data, active_presses, active_colors):
    active_data = filter_for_press(data, active_presses)
    subsets, _ = subset_data(active_data)
    active_subsets = filter_for_color(subsets, active_colors)
    active_data = pd.concat(active_subsets)
    return active_data

def filter_for_press(data, presses):
    output = []
    for press in presses:
        output.append(data[data['WP_NAME'] == press])
    output = pd.concat(output)
    return output

def filter_for_color(subsets, subset_visible):
    active_subsets = []
    for k in subsets.keys():
        if subset_visible[k]:
            active_subsets.append(subsets[k])
    return active_subsets

def main():
    data = load_data()
    matplot_only_heatmap(data)


if __name__ == "__main__":
    main()