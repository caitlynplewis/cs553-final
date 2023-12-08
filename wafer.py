import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
# from ipywidgets import interact

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

def display_data(df):
    x = df.columns
    y = df.index
    z = df
    X, Y = np.meshgrid(x, y)

    fig, ax = plt.subplots()
    hm = sn.heatmap(data = df, cmap="viridis")

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
    display_data(df)


if __name__ == "__main__":
    main()