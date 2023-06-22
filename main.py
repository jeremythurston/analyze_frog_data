# --------------------------------------------------------------
# Analyze FROG data
# Author: Jeremy Thurston
# Date: June 20, 2023
# --------------------------------------------------------------

# ----------------------- Imports ------------------------------
from import_frog_data import import_frog_data
from import_oceanoptics_data import import_oceanoptics_data
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
t_minimum = -500  # Minimum time [fs]
t_maximum = 500  # Maximum time [fs]
FROG_threshold = 0.03  # Phase data below this threshold is not shown
# --------------------------------------------------------------


if __name__ == "__main__":
    # Import data from FROG retrieval
    FROG_data = import_frog_data(frog_folder)
    ROI = np.where(FROG_data[1] > FROG_threshold)

    # Import data from OceanOptics spectrometer
    Spectrometer_data = import_oceanoptics_data(spectrum_file)

    # Process data
    # Calculate TL

    # Generate plot
    fig, axes = plt.subplots(2, 1, figsize=(3, 3))

    # Generate spectrum figure
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
        linestyle="--",
    )
    ax2.plot(FROG_data[0][ROI], FROG_data[2][ROI], color=c2, linewidth=0.75)
    axes[0].set_ylabel("Intensity (arb)")
    ax2.set_ylabel("Phase (rad)")
    axes[0].set_xlabel("Wavelength (nm)")
    axes[0].set_xlim(wl_minimum, wl_maximum)
    axes[0].legend()

    # Generate temporal figure
    # axes[1].plot(
    #     t_TL_frog,
    #     E_TL_frog,
    #     label=f"TL of FROG spectrum, {fwhm_TL_frog:.1f} fs",
    #     color=c1,
    # )
    # axes[1].plot(
    #     ts_frog - ts_frog[np.argmax(intensity_t)],
    #     intensity_t,
    #     label=f"Retrieved pulse, {fwhm_retrieved:.1f} fs",
    #     color=c4,
    # )
    # axes[1].set_xlabel("Time (fs)")
    # axes[1].set_ylabel("Intensity (arb)")
    # axes[1].set_xlim(t_minimum, t_maximum)
    # axes[1].legend()

    fig.tight_layout()
    plt.savefig("figures/combined_frog_plot.jpg", dpi=500)
    plt.show()
