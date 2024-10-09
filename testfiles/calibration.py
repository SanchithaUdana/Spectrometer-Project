from matplotlib import pyplot as plt
from matplotlib.colors import Normalize

import whitedata
import darkdata
import rawData
import numpy as np

# Convert the list to NumPy arrays for easier calculations
raw = np.array(rawData.rawData)
white = np.array(whitedata.whiteData)
dark = np.array(darkdata.darkData)

# Small constant to avoid division by zero
epsilon = 1e-10

# Calculate the denominator and replace zeros with epsilon
denominator = white - dark
denominator[denominator == 0] = epsilon  # Replace 0 in the denominator with a small number

# Calibrate the data
calibrated = (raw - dark) / denominator

# Mask NaN values as 0
calibrated = np.where(np.isnan(calibrated), 0, calibrated)

norm = Normalize(vmin=min(calibrated), vmax=max(calibrated))

# Create a plot using Matplotlib
plt.figure(figsize=(6, 4))  # Set the figure size (equivalent to 480x320 in pixels)
plt.scatter(np.arange(len(calibrated)), norm(calibrated), marker='x', color='blue')  # Use 'x' markers for the plot
plt.xlabel('Index')
plt.ylabel('Calibrated Value')
plt.grid(True)
plt.title('Calibrated Data Plot')
plt.show()
