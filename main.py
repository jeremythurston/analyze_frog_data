# --------------------------------------------------------------
# Analyze FROG data
# Author: Jeremy Thurston
# Date: June 20, 2023
# --------------------------------------------------------------

# Imports ------------------------------------------------------
import import_frog_data
import import_oceanoptics_data
import matplotlib.pyplot as plt
# --------------------------------------------------------------


# Make the plots pretty ----------------------------------------
plt.style.use(["science", "nature", "bright"])
plt.rcParams["font.family"] = "Helvetica"
plt.rcParams["font.size"] = 11
c1, c2 = "#33BBEE", "#EE7733"
# --------------------------------------------------------------

# Parameters ---------------------------------------------------
frog_folder = "FROG retrievals/"
spectrum_file = "OceanOptics Spectra/"
wl_minimum = 700  # Minimum wavelength [nm]
wl_maximum = 900  # Maximum wavelength [nm]
t_minimum = -200  # Minimum time [fs]
t_maximum = 200  # Maximum time [fs]
# --------------------------------------------------------------


if __name__ == "__main__":
    # Import data from FROG retrieval
    FROG_data = import_frog_data(frog_folder)

    # Import data from OceanOptics spectrometer
    Spectrometer_data = import_oceanoptics_data(spectrum_file)

    # Process data

    # Generate plot
    fig, axes = plt.subplots(2, 1, figsize=(3, 3))

    axes[0].plot(wls_frog, spectral_intensity, color=c1, label="Retrieved")
    axes[0].set_ylabel("Intensity (arb)")
    axes[0].set_xlabel("Wavelength (nm)")
    axes[0].set_xlim(950, 1100)

    axes[1].plot(
        t_TL_frog,
        E_TL_frog,
        label=f"TL of FROG spectrum, {fwhm_TL_frog:.1f} fs",
        color=c1,
    )
    axes[1].plot(
        ts_frog - ts_frog[np.argmax(intensity_t)],
        intensity_t,
        label=f"Retrieved pulse, {fwhm_retrieved:.1f} fs",
        color=c4,
    )
    axes[1].set_xlabel("Time (fs)")
    axes[1].set_ylabel("Intensity (arb)")
    axes[1].set_xlim(-5.5 * fwhm_TL_direct, 10.5 * fwhm_TL_direct)
    axes[1].legend()

    fig.tight_layout()
    plt.savefig("figures/frog/combined_frog_plot.jpg", dpi=500)
    plt.show()
