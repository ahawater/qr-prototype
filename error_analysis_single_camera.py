import numpy as np
import matplotlib.pyplot as plt
from math import tan, pi

# Constants
f = 6
d = 160
alpha =  47 * pi / 180
qr_size = 18
pixel_size = 2 * 10**-3 
b = 140 

# Functions
def g(a, d):
    numerator = a / d - tan(alpha)
    denominator = 1 + tan(alpha) * a / d
    return numerator / denominator

def equation_qr_side_length_measurment(a, d_res):
    return f * (g(a + qr_size, d - d_res) - g(a, d - d_res) - g(a + qr_size, d) + g(a, d)) - pixel_size

def equation_qr_center_location_measurment(a, d_res):
    result = np.where(
        a < 0,
        f * (g(a, d - d_res) - g(a, d)) + pixel_size,
        f * (g(a, d - d_res) - g(a, d)) - pixel_size
    )
    return result

# Grid setup
x = np.linspace(-b, 600 - b, 1000)  # Range for x
y = np.linspace(0, 20, 1000)   # Range for y
X, Y = np.meshgrid(x, y)

# Evaluate equations
Z1 = equation_qr_side_length_measurment(X, Y)
Z2 = equation_qr_center_location_measurment(X, Y)

# Plotting
plt.figure(figsize=(8, 6))
contour1 = plt.contour(X , Y, Z1, levels=[0], colors='blue', linewidths=2)  # Contour for equation 1
contour2 = plt.contour(X, Y, Z2, levels=[0], colors='red', linewidths=2)   # Contour for equation 2

# Add labels for axes
plt.xlabel("a: where the QR code is located [mm]")
plt.ylabel("d_res: resolution of the detected displacement [mm]")

# Add a dotted vertical line at x=0
plt.axvline(x=0, color='black', linestyle='--', linewidth=1)

# Set x-axis ticks every 40 mm
x_ticks = np.arange(-b, 600 -b + 1, 40)  # From -150 to 450, step of 40
plt.xticks(x_ticks)

plt.grid()

# Add legend
legend_handles = [
    plt.Line2D([], [], color='blue', label='qr side length measurment, equation 8'),
    plt.Line2D([], [], color='red', label='feature location measurment, equation 7')
]
plt.legend(handles=legend_handles)

plt.show()
