# --------------------------------------------------------------
# Analyze FROG data
# Author: Jeremy Thurston
# Date: June 20, 2023
# --------------------------------------------------------------

# ----------------------- Imports ------------------------------
from import_frog_data import import_frog_data
from import_oceanoptics_data import import_oceanoptics_data
from calculate_transform_limit import calculate_transform_limit
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------------------


# ---------------- Make the plots pretty -----------------------
plt.style.use(["science", "nature", "bright", "no-latex"])
plt.rcParams["font.family"] = "Helvetica"
plt.rcParams["font.size"] = 11
c1, c2 = "#33BBEE", "#EE7733"
# --------------------------------------------------------------

# ---------------------- Parameters ----------------------------
frog_folder = "FROG retrievals/FROG8"
spectrum_file = "OceanOptics Spectra/FROG8_spectrum.txt"
wl_minimum = 1400  # Minimum wavelength [nm]
wl_maximum = 1700  # Maximum wavelength [nm]
t_minimum = -300  # Minimum time [fs]
t_maximum = 300  # Maximum time [fs]
FROG_threshold = 0.03  # Phase data below this threshold is not shown
pulse_energy = 1  # Pulse energy [mJ]
# --------------------------------------------------------------


if __name__ == "__main__":
    # Import data from FROG retrieval
    FROG_data = import_frog_data(frog_folder)
    ROI = np.where(FROG_data[1] > FROG_threshold)
    ROI_t = np.where(FROG_data[4] > FROG_threshold)

    # Import data from OceanOptics spectrometer
    Spectrometer_data = import_oceanoptics_data(spectrum_file)

    # Calculate transform limit of OceanOptics spectrum
    TL_data = calculate_transform_limit(
        Spectrometer_data[0], Spectrometer_data[1], wl_minimum, wl_maximum
    )

    # Normalize temporal data
    # TODO: incorporate pulse_energy to calculate peak powers
    FROG_Et = FROG_data[4] / np.sum(
        FROG_data[4] * np.abs(FROG_data[0][-1] - FROG_data[0][-2])
    )
    TL_Et = TL_data[1] / np.sum(TL_data[1] * np.abs(TL_data[0][-1] - TL_data[0][-2]))

    max = np.max([np.max(FROG_Et), np.max(TL_Et)])

    FROG_Et = FROG_Et / max
    TL_Et = TL_Et / max

    # peak_power = np.sum(TL_Et * np.abs(TL_data[0][-1] - TL_data[0][-2])) * pulse_energy * 1e3  # [GW]
    peak_power = 1  # [GW]

    # Generate plot
    fig, axes = plt.subplots(2, 1, figsize=(3, 4))

    # ------------------ Generate spectrum figure ------------------
    ax2 = axes[0].twinx()

    axes[0].plot(
        FROG_data[0], FROG_data[1], color=c1, label="Retrieved", linewidth=0.75
    )
    axes[0].fill_between(
        Spectrometer_data[0],
        0,
        Spectrometer_data[1],
        color=c1,
        label="Measured",
        alpha=0.3,
        linewidth=0,
    )
    axes[0].plot(
        Spectrometer_data[0],
        Spectrometer_data[1],
        color=c1,
        linewidth=0.75,
        linestyle="--",
    )
    ax2.plot(FROG_data[0][ROI], FROG_data[2][ROI], color=c2, linewidth=0.75)

    axes[0].set_ylabel("Intensity (arb)")
    ax2.set_ylabel("Phase (rad)")
    axes[0].set_xlabel("Wavelength (nm)")
    axes[0].set_xlim(wl_minimum, wl_maximum)
    axes[0].legend()
    # --------------------------------------------------------------

    # ------------------ Generate temporal figure ------------------
    ax3 = axes[1].twinx()

    axes[1].plot(
        FROG_data[3], FROG_Et * peak_power, label="Retrieved", color=c1, linewidth=0.75
    )
    axes[1].fill_between(
        TL_data[0],
        0,
        TL_Et * peak_power,
        color=c1,
        label="FTL",
        alpha=0.3,
        linewidth=0,
    )
    axes[1].plot(
        TL_data[0], TL_Et * peak_power, color=c1, linewidth=0.75, linestyle="--"
    )
    ax3.plot(FROG_data[3][ROI_t], FROG_data[5][ROI_t], color=c2, linewidth=0.75)

    # axes[1].set_ylabel("Power (GW)")
    axes[1].set_ylabel("Power (arb)")
    ax3.set_ylabel("Phase (rad)")
    axes[1].set_xlabel("Time (fs)")
    axes[1].set_xlim(t_minimum, t_maximum)
    axes[1].legend()
    # --------------------------------------------------------------

    fig.tight_layout()
    plt.savefig("figures/combined_frog_plot.jpg", dpi=500)
    plt.show()
