import numpy as np
from scipy import interpolate
from scipy.interpolate import UnivariateSpline
from scipy.fft import fft, fftshift


def calculate_transform_limit(wls, intensity, wl_min, wl_max):
    intensity = np.where(np.logical_and(wls > wl_min, wls < wl_max), intensity, 0)
    phase = np.zeros(len(wls))
    Ew = np.sqrt(intensity) * np.exp(phase)
    freqs = 3e17 / wls
    df = np.abs(freqs[-1] - freqs[-2])
    freqfit = np.arange(-np.max(freqs), np.max(freqs), df)
    interp = interpolate.interp1d(
        freqs, Ew, kind="linear", bounds_error=False, fill_value=0
    )
    Ewfit = interp(freqfit)
    Ewfit = np.nan_to_num(Ewfit)
    E = fftshift(fft(Ewfit))
    E = np.abs(E) ** 2
    E = E / np.max(E)

    dt = 1 / (2 * np.max(freqs))
    t = np.linspace(-dt * len(freqfit) / 2, dt * len(freqfit) / 2, len(freqfit))
    t = t * 1e15

    # Sometimes doesn't work when the function is not well-behaved
    spline = UnivariateSpline(t, E - np.max(E) / 2, s=0)
    r1, r2 = spline.roots()
    fwhm = np.abs(r2 - r1)

    return [t, E, fwhm]
    # return [t, E]
