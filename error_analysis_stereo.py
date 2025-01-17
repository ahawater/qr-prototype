import numpy as np
import matplotlib.pyplot as plt
from math import tan, pi, sqrt

# All units in mm
b = 150 
f = 4.0
pixel_size = 1.85 * 10 **-3 
k = 1 / pixel_size
x_minus_x_prime_range = np.arange(500, 4024)  # Avoid division by zero
alpha = 25 * pi / 180
a = 250  # Provided value for a
d = 300

def g(a, d):
    numerator = a / d - tan(alpha)
    denominator = 1 + tan(alpha) * a / d
    return numerator / denominator

def compute_y(a, x_minus_x_prime_range):
    """
    Compute Y values for given parameters and range of (x - x').

    Parameters:
        b (float): Parameter b.
        k_x (float): Parameter k_x.
        k_y (float): Parameter k_y.
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
        b (float): Parameter b.
        k_x (float): Parameter k_x.
        f (float): Parameter f.
        x_minus_x_prime_range (list or numpy array): Range of (x - x').

    Returns:
        numpy array: Computed Z values.
    """
    x_minus_x_prime = np.array(x_minus_x_prime_range)
    Z = b * k * f / x_minus_x_prime
    return Z

# Compute Z and Y values
z_values = compute_z(x_minus_x_prime_range)
y_values = compute_y(a, x_minus_x_prime_range)

# Compute sqrt(Z^2 + Y^2)
sqrt_values = np.sqrt(z_values**2 + y_values**2)

# Plot sqrt(Z^2 + Y^2)
plt.plot(x_minus_x_prime_range, sqrt_values, marker='o', label='sqrt(Z^2 + Y^2) vs (x - x\')')
plt.xlabel('x - x\'')
plt.ylabel('sqrt(Z^2 + Y^2)')
plt.title('Plot of sqrt(Z^2 + Y^2) as a function of (x - x\')')
plt.legend()
plt.grid()
plt.show()
