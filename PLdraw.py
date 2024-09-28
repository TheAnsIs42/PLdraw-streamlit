# python package for PLdraw

import scienceplots, os, fnmatch
import pandas as pd
import matplotlib.pyplot as plt
from warnings import warn
from matplotlib.axes import Axes
from matplotlib.figure import Figure


global h  # eV energy
global c
h = 6.63e-34 / 1.6e-19  # eV energy
c = 3e8


def find(pattern, path):
    result = []
    for fileName in os.listdir(path):
        if fnmatch.fnmatch(fileName, pattern):
            result.append(os.path.join(path, fileName))
    return result


def read_data(file) -> pd.DataFrame:
    data = pd.read_csv(file, sep="\s+", header=None, names=["wavelength", "count"])
    # normalize
    data["normalized"] = (data["count"] - data["count"].min()) / (
        data["count"].max() - data["count"].min()
    )
    data["energy"] = h * c / (data["wavelength"] * 1e-9)
    return data


def single_plot(ax: Axes, file: str, energyDiagram: bool, rcParDict: dict = {}) -> Axes:
    if bool(rcParDict):
        plt.rcParams.update(rcParDict)
    data = read_data(file)
    ax.set_ylabel("Normalized intensity(arb.u.)", fontsize=12)
    ax.tick_params(width=1.0, labelsize=12)
    plt.setp(ax.spines.values(), linewidth=1.0)
    if energyDiagram:
        ax.invert_xaxis()
        ax.plot(data["energy"], data["normalized"])
        ax.set_xlabel("Energy(eV)", fontsize=12)
    else:
        ax.plot(data["wavelength"], data["normalized"])
        ax.set_xlabel("Wavelength (nm)", fontsize=12)
    ax.grid()
    return ax


def single_origin(
    ax: Axes, file: str, energyDiagram: bool, rcParDict: dict = {}
) -> Axes:
    if bool(rcParDict):
        plt.rcParams.update(rcParDict)
    data = read_data(file)
    ax.set_ylabel("Intensity(arb.u.)", fontsize=12)
    ax.tick_params(width=1.0, labelsize=12)
    plt.setp(ax.spines.values(), linewidth=1.0)
    if energyDiagram:
        ax.invert_xaxis()
        ax.plot(data["energy"], data["count"])
        ax.set_xlabel("Energy(eV)", fontsize=12)
    else:
        ax.plot(data["wavelength"], data["count"])
        ax.set_xlabel("Wavelength (nm)", fontsize=12)
    ax.grid()
    return ax


# multi lines
def multi_plot(
    ax: Axes,
    files: list,
    energyDiagram: bool = False,
    legend: list = [],
    shift: list = [],
    rcParDict: dict = {},
) -> Axes:
    if bool(rcParDict):
        plt.rcParams.update(rcParDict)
    if not legend:
        legend = [file[-8:-4] for file in files]
    if not shift:
        shift = [0] * len(files)
    ax.set_ylabel("Normalized intensity(arb.u.)", fontsize=12)
    ax.tick_params(width=1.0, labelsize=12)
    plt.setp(ax.spines.values(), linewidth=1.0)
    if energyDiagram:
        ax.invert_xaxis()
    for idx, file in enumerate(files):
        data = read_data(file)
        if energyDiagram:
            ax.plot(data["energy"] + shift[idx], data["normalized"], label=legend[idx])
            ax.set_xlabel("Energy(eV)", fontsize=12)
        else:
            ax.plot(
                data["wavelength"] + shift[idx], data["normalized"], label=legend[idx]
            )
            ax.set_xlabel("Wavelength (nm)", fontsize=12)
    ax.legend()
    ax.grid()
    return ax


def overall_normalize(
    ax: Axes,
    files: list,
    energyDiagram: bool = False,
    legend: list = [],
    shift: list = [],
    rcParDict: dict = {},
) -> Axes:
    warn("Only reasonable with same exposure condition")
    if bool(rcParDict):
        plt.rcParams.update(rcParDict)
    if not legend:
        legend = [file[-8:-4] for file in files]
    if not shift:
        shift = [0] * len(files)
    # ax.set_xlim(0, 3000)
    # ax.set_ylim(0, 5)
    ax.set_ylabel("Normalized intensity(arb.u.)", fontsize=12)
    ax.tick_params(width=1.0, labelsize=12)
    plt.setp(ax.spines.values(), linewidth=1.0)
    if energyDiagram:
        ax.invert_xaxis()
    data_list = []
    all_max = []
    all_min = []
    for file in files:
        data = read_data(file)
        all_max.append(data["count"].max())
        all_min.append(data["count"].min())
        data_list.append(data)
    for idx, data in enumerate(data_list):
        data["normalized"] = (data["count"] - min(all_min)) / (
            max(all_max) - min(all_min)
        )
        if energyDiagram:
            ax.plot(data["energy"] + shift[idx], data["normalized"], label=legend[idx])
            ax.set_xlabel("Energy(eV)", fontsize=12)
        else:
            ax.plot(
                data["wavelength"] + shift[idx], data["normalized"], label=legend[idx]
            )
            ax.set_xlabel("Wavelength (nm)", fontsize=12)
    ax.legend()
    ax.grid()
    return ax


def multi_origin(
    ax: Axes,
    files: list,
    energyDiagram: bool = False,
    legend: list = [],
    shift: list = [],
    rcParDict: dict = {},
) -> Axes:
    warn("Only reasonable with same exposure condition")
    if bool(rcParDict):
        plt.rcParams.update(rcParDict)
    if not legend:
        legend = [file[-8:-4] for file in files]
    if not shift:
        shift = [0] * len(files)
    # ax.set_xlim(0, 3000)
    # ax.set_ylim(0, 5)
    ax.set_ylabel("Intensity(arb.u.)", fontsize=12)
    ax.tick_params(width=1.0, labelsize=12)
    plt.setp(ax.spines.values(), linewidth=1.0)
    if energyDiagram:
        ax.invert_xaxis()
    for idx, file in enumerate(files):
        data = read_data(file)
        if energyDiagram:
            ax.plot(data["energy"] + shift[idx], data["count"], label=legend[idx])
            ax.set_xlabel("Energy(eV)", fontsize=12)
        else:
            ax.plot(data["wavelength"] + shift[idx], data["count"], label=legend[idx])
            ax.set_xlabel("Wavelength (nm)", fontsize=12)
    ax.legend()
    ax.grid()
    return ax


## test area
if __name__ == "__main__":
    postfix = input("give me the postfix")
    energyDiagram = input("energy plot? (y/n): ").lower().strip() == "y"
    files = find("*" + postfix + ".txt", path="./raman shift compare/")
    legend = []
    print("number of files:" + str(len(files)))
    if len(files) == 0:
        raise Exception("no match file found")
    rcParams = {}
    rcParams["lines.linewidth"] = 3
    rcParams["figure.figsize"] = (5, 5)
    with plt.style.context(["science", "nature"]):
        fig, ax = plt.subplots()
        ax = multi_plot(ax, files, energyDiagram, rcParDict=rcParams)
        plt.show()
