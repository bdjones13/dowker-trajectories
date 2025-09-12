import numpy as np
import importlib.resources as ir

def load_lorenz63():
    # point to the package where the file lives
    with ir.files("dowker_trajectories.Data.Lorenz63").joinpath("lorenz_10k_raw.npy").open("rb") as f:
        l63 = np.load(f).T[:, 10000:100000]
    return l63

def load_lorenz96():
    with ir.files("dowker_trajectories.Data.Lorenz96").joinpath("lorenz96_raw.txt").open("r") as f:
        return np.loadtxt(f)

def load_cdv():
    with ir.files("dowker_trajectories.Data.CDV").joinpath("cdv_deterministic.npy").open("r") as f:
        return np.fromfile(f).reshape(6,-1)#[:3,10000:90000] #6x2000000, use first three dimensions and cut down on length a lot


def load_jetlat():
    with ir.files("dowker_trajectories.Data.JetLat").joinpath("JetLat.txt").open("r") as f:
        return  np.loadtxt(f, delimiter = ",").T #3x9809 this one is either already reduced by Kristian et al or just fine as is