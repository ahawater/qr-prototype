import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread("data/template.jpg")
if image is None:
    print("Error: Could not load image.")
    exit()

# Define the 3x3 homography matrix (example values, replace with your own)
H = np.array([
    [0.5, 0, 0],  # Shrinks and translates to the right
    [0, 0.5, 0],  # Shrinks and translates down
    [0, 0, 1]      # Homogeneous coordinate (no change)
], dtype=np.float32)

# Get image dimensions
h, w = image.shape[:2]

# Define the corners of the image
corners = np.array([
    [0, 0],
    [w-1, 0],
    [w-1, h-1],
    [0, h-1]
], dtype=np.float32)

# Apply the homography to the corners to get the new bounds
transformed_corners = cv2.perspectiveTransform(np.array([corners]), H).squeeze()

# Get the bounding box of the transformed corners
min_x, min_y = transformed_corners.min(axis=0)
max_x, max_y = transformed_corners.max(axis=0)

# Compute the translation needed to make the whole transformed image fit
translation = [-min_x, -min_y]

# Apply the homography with translation to avoid cropping
H_translate = np.array([
    [1, 0, translation[0]],
    [0, 1, translation[1]],
    [0, 0, 1]
], dtype=np.float32)

# Apply the homography transformation with translation
transformed_image = cv2.warpPerspective(image, H @ H_translate, (int(max_x - min_x), int(max_y - min_y)))

# Convert image from BGR to RGB (for displaying with matplotlib)
transformed_image_rgb = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB)

# Plot the transformed image using matplotlib
plt.imshow(transformed_image_rgb)
plt.axis('off')  # Hide axes for a cleaner view
plt.show()

# Optionally save the transformed image
cv2.imwrite("output.jpg", transformed_image)

