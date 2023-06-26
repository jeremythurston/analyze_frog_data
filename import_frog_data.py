import numpy as np


def import_frog_data(foldername):
    frog_data_spec = np.genfromtxt(foldername + "/Speck.dat", delimiter="  ")
    frog_data_ts = np.genfromtxt(foldername + "/Ek.dat", delimiter="  ")

    wls = frog_data_spec[:, 0]
    spec_A = frog_data_spec[:, 1]
    spec_phi = frog_data_spec[:, 2]

    ts = frog_data_ts[:, 0]
    t_A = frog_data_ts[:, 1]
    t_phi = frog_data_ts[:, 2]

    spec_A = spec_A / np.max(spec_A)
    t_A = t_A / np.max(t_A)

    return [wls, spec_A, spec_phi, ts, t_A, t_phi]
