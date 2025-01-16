import numpy as np
import matplotlib.pyplot as plt
from math import tan, pi

# All units in mm
b = 150 
f = 4.0
pixel_size = 1.85 * 10 **-3 
k_x = 1 / pixel_size
x_minus_x_prime_range = np.arange(500, 4024)  # Avoid division by zero
alpha = 25 * pi / 180

def g(a, d):
    numerator = a / d - tan(alpha)
    denominator = 1 + tan(alpha) * a / d
    return numerator / denominator


def compute_z(b, k_x, f, x_minus_x_prime_range):
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
    Z = b * k_x * f / x_minus_x_prime
    return Z



# Compute Z values
z_values = compute_z(b, k_x, f, x_minus_x_prime_range)

# Plot Z values
plt.plot(x_minus_x_prime_range, z_values, marker='o', label='Z vs (x - x\')')
plt.xlabel('x - x\'')
plt.ylabel('Z')
plt.title('Plot of Z = b * k_x * f / (x - x\')')
plt.legend()
plt.grid()
plt.show()

