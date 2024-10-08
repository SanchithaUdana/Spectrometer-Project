import matplotlib.pyplot as plt
import numpy as np

# Example data (y-axis values between 0 and 1)
x = np.linspace(0, 10, 100)
y = np.sin(x) / 2 + 0.5  # Sample data normalized to 0-1 range

# Invert the y values by subtracting them from 1
y_inverted = 1 - y

# Plot the original and inverted data
plt.plot(x, y, label='Original Data')
plt.plot(x, y_inverted, label='Inverted Data')

# Set y-axis limits to 0-1
plt.ylim(0, 1)

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()
plt.title('Inverted Y-axis Data Plot (0-1 Range)')
plt.show()
