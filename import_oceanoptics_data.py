import pandas as pd
import numpy as np


def import_oceanoptics_data(filename):
    data = pd.read_csv(filename, delimiter="\t", names=["wls", "counts"], skiprows=13)
    wls, counts = data["wls"], data["counts"]
    # baseline = np.median(np.sort(counts)[counts < (0.05 * np.max(counts))])
    # counts = counts - baseline
    counts = counts / np.max(counts)

    wls = wls.to_numpy(dtype=float)
    counts = counts.to_numpy(dtype=float)

    return [wls, counts]
