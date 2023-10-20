# Author: rei-ashine
# DATE: Oct. 20th, 2023

"""
Create a scatter plot from PISA scores.
"""

import os
import os.path
import argparse
import warnings
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

warnings.filterwarnings("ignore", "is_categorical_dtype")
warnings.filterwarnings("ignore", "use_inf_as_na")


def loader(path):
    """
    Load the PISA score CSV file.
    """
    data = pd.read_csv(path)
    basename = os.path.basename(path)
    name = os.path.splitext(basename)[0]
    print("[INFO] Input CSV file : ", basename)
    return data, name


def init_figure():
    """
    Initialize the figure.
    """
    # Figure
    sns.set(font_scale=6)
    sns.set_palette("Set1")
    sns.set_style("whitegrid")

    fig = plt.figure(figsize=(50, 25))
    plt.subplots_adjust(left=0.02, bottom=0.06, right=0.8, top=0.96)
    ax = plt.gca()    # <-- To avoid MatplotlibDeprecationWarning

    # Font
    theme_font = "Times New Roman"
    plt.rcParams["font.family"] = theme_font

    # math font
    plt.rcParams["mathtext.fontset"] = "stix"
    plt.rcParams["font.size"] = 20

    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'

    return fig, ax


def label_point(x, y, idx, ax):
    """
    Label each point in a scatterplot.
    """
    df_tmp = pd.concat({"x":x, "y":y, "id":idx}, axis="columns")
    for _, point in df_tmp.iterrows():
        ax.text(point["x"], point["y"]-0.1, point["id"],
                fontsize=50, horizontalalignment="center", rotation=25)


def scatterplot(data, name, group, path):
    """
    Make a scatter plot.
    """
    # Initialize a figure
    fig, ax = init_figure()
    theme_font = "Times New Roman"

    xlabel = "Buried area\n[Å2]"
    ylabel = "ΔiG\n[kcal/mol]"
    idx = "Mutations"

    # Make a scatterplot
    ax = sns.scatterplot(data, x=xlabel, y=ylabel,
                         hue=group, size=group, sizes=(1000, 10000),
                         legend="full", palette="viridis")
    # Set labels
    label_point(data[xlabel], data[ylabel], data[idx], ax)

    # Set legends
    if group == "NHB":
        legend_title = "Number of potential \nHydrogen bonds"
    elif group == "NSB":
        legend_title = "Number of potential \nSalt bridges"
    else:
        legend_title = group

    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1.035),
                    fontsize=80, title_fontsize=60, title=legend_title)

    # Set the title of this figure
    position = re.findall("Mutate_7e5o_GlobalMinimized_(.*)", name)
    position = re.findall(r"([H,L]\-[A-Z]{3}_[0-9]+_[A-Z]{3}|[H,L]\-[A-Z]{3}_[0-9]+)", position[0])
    for i, p in enumerate(position):
        # Check the chain name
        if "H-" in p:
            chain = " in Heavy chain"
        elif "L-" in p:
            chain = " in Light chain"
        else:
            assert (re.match(r"[H,L]\-", p)), \
                "[Warning] An unknown file naming convention was detected."
        # Convert to protein mutation notation
        tmp = re.sub(r"[H,L]\-", "", p)
        tmp = tmp.split("_")
        tmp = list(map(lambda x: x.capitalize(), tmp))
        position[i] = "p." + "".join(tmp)

    position = "[ " + ", ".join(position) + " ]"

    fig_title = "Mutation of antibody residues at \n" + position + chain
    ax.set_title(fig_title, loc="left", fontsize=100, pad=100, fontname=theme_font)

    # Set axis names and axis labels
    ax.set_xlabel(xlabel.replace("\n", " "), labelpad=30, fontname=theme_font)
    ax.set_ylabel(ylabel.replace("\n", " "), labelpad=30, fontname=theme_font)
    plt.xticks(fontname=theme_font)
    plt.yticks(fontname=theme_font)

    # Make the output directory
    try:
        os.makedirs(path)
    except FileExistsError:
        pass

    # Save figure
    name = name + "_scatterplot_" + group + ".png"
    output = path + "/" + name

    fig.tight_layout()
    print("[INFO] Output scatterplot file : ", name)

    #fig.savefig(output, dpi=300)
    fig.savefig(output, transparent=True, dpi=300)
    #plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True,
                        help="Set the input PISA score CSV file path")
    parser.add_argument("-o", "--output", default="./data/PISA",
                        help="Set the output directory path")
    args = parser.parse_args()
    print("Seaborn " + sns.__version__)
    print("----- START -----")

    path_input = args.input
    path_output = args.output

    # Load an input PISA score CSV file
    df, filename = loader(path_input)

    # Make a scatter plot
    scatterplot(df, filename, "NHB", path_output)
    scatterplot(df, filename, "NSB", path_output)

    print("----- END -----")
