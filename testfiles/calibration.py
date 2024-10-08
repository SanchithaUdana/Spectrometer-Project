# Convert the list to NumPy arrays for easier calculations
raw = np.array(raw)
white = np.array(whiteData)
dark = np.array(darkData)

# Avoid division by zero by adding a very small number (epsilon) where the denominator is zero
# Small constant to avoid division by zero
epsilon = 1e-10

denominator = white - dark
denominator[denominator == 0] = epsilon  # Replace 0 in the denominator with a small number

calibrated = (raw - dark) / denominator

# mask the NAN values as 0
calibrated = np.where(np.isnan(calibrated), 0, calibrated)

print(calibrated)  # or return this array for further processing

# Plot the calibrated values
plt.figure(figsize=(10, 6))
plt.plot(calibrated, marker='1', color='b')
plt.title('Calibrated Values')
plt.xlabel('Index')
plt.ylabel('Calibrated Value')
plt.grid(True)
plt.show()

# Invert the raw data
rawInvert = 1 - raw
#
# Plot the calibrated values
plt.figure(figsize=(10, 6))
plt.plot(raw, marker='1', color='c')
plt.title('Calibrated Values')
plt.xlabel('Index')
plt.ylabel('Calibrated Value')
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(rawInvert, marker='1', color='c')
plt.title('Calibrated Values')
plt.xlabel('Index')
plt.ylabel('Calibrated Value')
plt.grid(True)
plt.show()

# print("raw data")
# print("raw data")
# print(len(raw))
# for i in raw:
#     print(i, end=',')
#
# print("")
# print("invert data")
# print("invert data")
# print(len(rawInvert))
# for i in rawInvert:
#     print(i, end=',')
