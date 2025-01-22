import numpy as np
import matplotlib.pyplot as plt
from math import tan, pi, sqrt, cos

# All units in mm
b = 200
f = 4.0
pixel_size = 1.85 * 10 **-3 
k = 1 / pixel_size
alpha = 25 * pi / 180
d = 350
a_range = np.arange(-150, 451, 0.01)  # Range for a from -150 to 450

def g(a, d):
    numerator = a / d - tan(alpha)
    denominator = 1 + tan(alpha) * a / d
    return numerator / denominator

def y(a, d):
    return - f * g(a, d) * k

def compute_Y(y, dx):
    Y = b * y / dx
    return Y

def compute_Z(dx):
    Z = b * k * f / dx
    return Z

def compute_dx(a, y):
    numerator = b**2 * (y ** 2 + (k * f) **2)
    denominator = d**2 + a**2
    return sqrt(numerator / denominator)

def compute_d(y, dx, a):
    Y = compute_Y(y, dx)
    Z = compute_Z(dx)
    return sqrt(Z**2 + Y**2 - a**2)



# Compute values for a_range
y_values = np.array([round(y(a, d)) for a in a_range])  # Calculate y
dx_values = np.array([round(compute_dx(a, y_val)) for a, y_val in zip(a_range, y_values)])  # Calculate and round dx
d_values = np.array([compute_d(y_val, dx, a) for y_val, dx, a in zip(y_values, dx_values, a_range)])  # Calculate and round d
d_values = d_values - d

# Calculate the error d - 350
error_values = d_values - 350

# Find the maximum absolute error
max_error = np.max(np.abs(error_values))

# Print the maximum error
print(f"Maximum absolute error: {max_error:.2f} mm")


# Plot the results
plt.figure(figsize=(12, 8))

# Plot y
plt.subplot(3, 1, 1)
plt.plot(a_range, y_values, label="y(a)")
plt.xlabel("a (mm)")
plt.ylabel("y (pixels)")
plt.title("y(a) vs a")
plt.grid()
plt.legend()

# Plot dx
plt.subplot(3, 1, 2)
plt.plot(a_range, dx_values, label="dx(a)", color="orange")
plt.xlabel("a (mm)")
plt.ylabel("dx (pixels)")
plt.title("dx(a) vs a")
plt.grid()
plt.legend()

# Plot d
plt.subplot(3, 1, 3)
plt.plot(a_range, d_values, label="d(a)", color="green")
plt.xlabel("a (mm)")
plt.ylabel("d_err (mm)")
plt.title("d_err(a) vs a")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()
