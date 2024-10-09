from matplotlib import pyplot as plt
from matplotlib.colors import Normalize

import whitedata
import darkdata
import rawData
import numpy as np

from whitedata import whiteData

# spectrometer_calibration.py



# Assume you also have corresponding wavelengths (you can replace this with actual values)
wavelengths = np.linspace(300, 900, len(rawData.rawData))

# Convert the lists to numpy arrays for easy manipulation
S_raw = np.array(rawData.rawData)
S_white = np.array(whitedata.whiteData)
S_black = np.array(darkdata.darkData)

# Calibration equation
def calibrate_signal(S_raw, S_white, S_black):
    return (S_raw - S_black) / (S_white - S_black)

# Apply calibration
calibrated_signal = calibrate_signal(S_raw, S_white, S_black)

# Plotting the calibrated signal against wavelength
plt.figure(figsize=(10, 6))
plt.plot(wavelengths, calibrated_signal, label='Calibrated Signal', color='b', lw=2)

# Customizing the plot
plt.title('Calibrated Spectrometer Data')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Calibrated Signal')
plt.grid(True)
plt.legend()

# Show the plot
plt.show()

