import numpy as np
import matplotlib.pyplot as plt

# Constants
b = 140
f = 4.0
pixel_size = 1.85 * 10**-3
k = 1 / pixel_size
alpha = 25 * np.pi / 180

# Define the function g(a, d)
def g(a, d):
    numerator = a / d - np.tan(alpha)
    denominator = 1 + np.tan(alpha) * a / d
    return numerator / denominator

# Define the equation function
def equation(a, d, dx):
    lhs = d**2 + a**2
    rhs = (b * f * g(a, d) / (k * dx))**2 + (b * k * f / dx)**2
    return lhs - rhs

# Range of a, d, and dx
a_range = np.linspace(-140, 460, 10000)  # Fine discretization for a
d_range = np.linspace(10, 350, 10000)   # Fine discretization for d
dx_values = range(400, 4024)

# Tolerance for numerical comparison
tolerance = 0.1

# Store solutions
solutions = []

# Iterate over dx values and check for (a, d) solutions
for dx_val in dx_values:
    if dx_val == 0:  # Avoid division by zero
        continue
    for a_val in a_range:
        for d_val in d_range:
            if abs(equation(a_val, d_val, dx_val)) < tolerance:
                solutions.append((dx_val, a_val, d_val))

# Extract data for plotting
dx_vals = [s[0] for s in solutions]
a_vals = [s[1] for s in solutions]
d_vals = [s[2] for s in solutions]

# Scatter plot
plt.figure(figsize=(10, 6))
scatter = plt.scatter(d_vals, a_vals, c=dx_vals, cmap='Reds', edgecolor='k', s=100)

# Add colorbar
cbar = plt.colorbar(scatter)
cbar.set_label('dx (integer)', rotation=270, labelpad=15)

# Label the axes
plt.xlabel('d')
plt.ylabel('a')
plt.title('Scatter Plot of Solutions (d, a) with dx Color Intensity')
plt.grid(True)

plt.show()
