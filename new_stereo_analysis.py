from scipy.optimize import fsolve
import numpy as np
import matplotlib.pyplot as plt
from math import tan, pi, sqrt, cos
import math

# All units in mm
b = 140 
f = 4.0
pixel_size = 1.85 * 10 **-3 
k = 1 / pixel_size
alpha = 25 * pi / 180
d = 350

def g(a, d):
    numerator = a / d - tan(alpha)
    denominator = 1 + tan(alpha) * a / d
    return numerator / denominator

def compute_y(a, delta_x):
    """
    Compute Y values for given parameters and range of (x - x').

    Parameters:
        a (float): Parameter a.
        x_minus_x_prime_range (list or numpy array): Range of (x - x').

    Returns:
        numpy array: Computed Y values.
    """
    y = f * g(a, d)  # Use the g function to compute y
    Y = b * y / k * delta_x
    return Y

def compute_z(delta_x):
    """
    Compute Z values for given parameters and range of (x - x').

    Parameters:
        x_minus_x_prime_range (list or numpy array): Range of (x - x').

    Returns:
        numpy array: Computed Z values.
    """
    Z = b * k * f / delta_x
    return Z


# Define the equation as a function for delta_x
def variable_delta_x(delta_x):
    # Compute Y and Z for the given delta_x
    y = compute_y(a, delta_x)
    z = compute_z(delta_x)
    
    # Return the equation to be solved (should be zero when the solution is found)
    return y ** 2 + z ** 2 - d ** 2 - a ** 2

# Define the equation as a function for delta_x
def variable_d(d):
    # Compute Y and Z for the given delta_x
    y = compute_y(a, delta_x)
    z = compute_z(delta_x)
    
    # Return the equation to be solved (should be zero when the solution is found)
    return y ** 2 + z ** 2 - d ** 2 - a ** 2

# Define the range of a values
a_values = np.linspace(-b, 600 - b, 500)
d_d_est_differences = []

for a in a_values:
    # Initial guess for delta_x
    initial_guess_delta_x = [700]

    # Solve the equation for delta_x
    solution = fsolve(variable_delta_x, initial_guess_delta_x, xtol=1e-6)

    delta_x = solution[0]
    delta_x = math.floor(delta_x)

    initial_guess_d = [300]
    solution = fsolve(variable_d, initial_guess_d, xtol=1e-6)

    d_est_down = solution[0]

    delta_x = delta_x + 1
    solution = fsolve(variable_d, initial_guess_d, xtol=1e-6)
    d_est_up = solution[0]


    d_d_est_differences.append(abs(d_est_down - d_est_up))

    print(f"x - x' = {delta_x}")
    print(f"d - d_est' = {abs(d_est_down - d_est_up)}")

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(a_values, d_d_est_differences, label="$|d - d_{est}|$")
plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
plt.title("Difference between $d$ and $d_{est}$ vs. $a$")
plt.xlabel("$a$ (mm)")
plt.ylabel("$|d - d_{est}|$ (mm)")
plt.legend()
plt.grid(True)
plt.show()

# problem is that a also changes