import numpy as np
import matplotlib.pyplot as plt
from math import tan, pi, sqrt, cos

# All units in mm
b = 140 
f = 4.0
pixel_size = 1.85 * 10 **-3 
k = 1 / pixel_size
x_minus_x_prime_range = np.arange(500, 4024)  # Avoid division by zero
alpha = 25 * pi / 180
d = 300
a_range = np.arange(-150, 451, 0.1)  # Range for a from -150 to 450

def g(a, d):
    numerator = a / d - tan(alpha)
    denominator = 1 + tan(alpha) * a / d
    return numerator / denominator

def compute_y(a, x_minus_x_prime_range):
    """
    Compute Y values for given parameters and range of (x - x').

    Parameters:
        a (float): Parameter a.
        x_minus_x_prime_range (list or numpy array): Range of (x - x').

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

# Compute the difference between sqrt(Z^2 + Y^2) of two integers around x-x' that satisfy the condition
def compute_resolution(a):
    z_values = compute_z(x_minus_x_prime_range)
    y_values = compute_y(a, x_minus_x_prime_range)
    discrete_possible_measurments = cos (alpha) * np.sqrt(z_values**2 + y_values**2)

    # Find the index where sqrt(Z^2 + Y^2) is closest to the target value
    closest_index = np.argmin(np.abs(discrete_possible_measurments - d))

    # Get the two integers around the closest x-x'
    if closest_index == 0 or closest_index == len(x_minus_x_prime_range) - 1:
        return 0  # Edge case where no two integers are around the solution

    lower_value = discrete_possible_measurments[closest_index]
    upper_value = discrete_possible_measurments[closest_index + 1]
    return abs(d- lower_value)

# Compute differences for all a in the range
differences = [compute_resolution(a) for a in a_range]

# Plot the differences
plt.plot(a_range, differences)
plt.xlabel('a [mm]')
plt.ylabel('Resolution [mm]')
plt.grid()
plt.show()
