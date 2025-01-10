import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the two images
def qr_area(image_number, qr_number):
    image1_path = f"data/daheng/0_QR_{qr_number}.png"  # Replace with your first image path
    image2_path = f"data/daheng/{image_number}_QR_{qr_number}.png"  # Replace with your second image path
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Initialize SIFT
    sift = cv2.SIFT_create()

    # Detect and compute keypoints and descriptors
    keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

    # Match descriptors using BFMatcher
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)
    matches = sorted(matches, key=lambda x: x.distance)

    # Extract matched points
    points1 = np.float32([keypoints1[m.queryIdx].pt for m in matches])
    points2 = np.float32([keypoints2[m.trainIdx].pt for m in matches])

    # Compute the homography matrix
    H, _ = cv2.findHomography(points1, points2, cv2.RANSAC)

    # Extract scale from the homography matrix
    scale_x = np.sqrt(H[0, 0]**2 + H[0, 1]**2)
    scale_y = np.sqrt(H[1, 0]**2 + H[1, 1]**2)
    scale = (scale_x + scale_y) / 2  # Average scale factor

    # Compute displacement
    X1 = 750
    u1_over_u2 = 1 / scale
    X2 = X1 * u1_over_u2
    displacement = round(X1 - X2, 1)
    return displacement

# Initialize data storage
displacement_data = {}

# Collect displacement data for each QR code and image number
for qr_number in range(3):
    displacement_data[qr_number] = []
    for image_number in range(1, 7):
        displacement = qr_area(image_number, qr_number)
        displacement_data[qr_number].append(displacement)

# Plot the data
plt.figure(figsize=(10, 6))
x_axis = [2.5, 5, 10, 20, 40, 80]
for qr_number, displacements in displacement_data.items():
    plt.plot(x_axis, displacements, marker='o', label=f"QR {qr_number}")

plt.title("Displacement vs. Image Number")
plt.xlabel("QR1 real displacement [mm]")
plt.ylabel("Measured displacement")
plt.legend()
plt.grid(True)
plt.show()
