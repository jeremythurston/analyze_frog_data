import numpy as np


def import_frog_data(foldername):
    frog_data = np.genfromtxt(foldername + "/Speck.dat", delimiter="  ")

    wls = frog_data[:, 0]
    spec_A = frog_data[:, 1]
    spec_phi = frog_data[:, 2]

    spec_A = spec_A / np.max(spec_A)

    return [wls, spec_A, spec_phi]
