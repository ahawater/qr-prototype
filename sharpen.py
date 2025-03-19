import cv2
import numpy as np

# Define a sharpening function
def sharpen_image(image):
    # Apply sharpening using the cv2.addWeighted() method
    alpha = 2  # Higher values will sharpen more
    beta = -0.6  # Decrease for softer sharpening
    return cv2.addWeighted(image, alpha, image, beta, 0)

# Loop through the images numbered 3 to 17
for i in range(3, 18):
    # Load each image
    image_path = f"{i}.jpg"  # Image path, e.g., '3.jpg', '4.jpg', etc.
    image = cv2.imread(image_path)

    # Check if the image was loaded successfully
    if image is None:
        print(f"Could not load image {i}.jpg")
        continue

    # Sharpen the image
    sharpened_image = sharpen_image(image)

    # Save the sharpened image
    sharpened_image_path = f"{i}_sharpened.jpg"
    cv2.imwrite(sharpened_image_path, sharpened_image)

    print(f"Saved {sharpened_image_path}")
