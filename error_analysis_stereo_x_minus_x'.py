import numpy as np
import matplotlib.pyplot as plt
from math import tan, pi, sqrt, cos

# All units in mm
b = 140 
f = 4.0
pixel_size = 1.85 * 10 **-3 
k = 1 / pixel_size
x_minus_x_prime_range = np.arange(400, 4024)  # Avoid division by zero
alpha = 25 * pi / 180
a = 100  # Fix a = 100
d = 350

def g(a, d):
    numerator = a / d - tan(alpha)
    denominator = 1 + tan(alpha) * a / d
    return numerator / denominator

def compute_y(a, x_minus_x_prime_range, d):
    """
    Compute Y values for given parameters and range of (x - x').

    Parameters:
        a (float): Parameter a.
        x_minus_x_prime_range (list or numpy array): Range of (x - x').
        d (float): Distance parameter.

    Returns:
        numpy array: Computed Y values.
    """
    x_minus_x_prime = np.array(x_minus_x_prime_range)
    y = f * g(a, d)  # Use the g function to compute y
    Y = b * y / x_minus_x_prime
    return Y

def compute_z(x_minus_x_prime_range):
    """
    Compute Z values for given parameters and range of (x - x').

    Parameters:
        x_minus_x_prime_range (list or numpy array): Range of (x - x').

    Returns:
        numpy array: Computed Z values.
    """
    x_minus_x_prime = np.array(x_minus_x_prime_range)
    Z = b * k * f / x_minus_x_prime
    return Z

def compute_d_est(x_minus_x_prime_range):
    z_values = compute_z(x_minus_x_prime_range)
    y_values = compute_y(a, x_minus_x_prime_range, d)
    angle = alpha + np.arctan(y_values / z_values)
    d_est = np.cos(angle) * np.sqrt(z_values**2 + y_values**2)
    return d_est

# Compute differences for all d in the range
d_est = compute_d_est(x_minus_x_prime_range)

# Plot the differences as a scatter plot with lines
plt.plot(x_minus_x_prime_range, d_est, color='blue', linewidth=1)  # Line connection
plt.scatter(x_minus_x_prime_range, d_est, s=5, color='blue')  # Larger dots
plt.xlabel('x - x\' [mm]')
plt.ylabel('d_est [mm]')
plt.legend()
plt.grid()
plt.show()
