import cv2
import numpy as np

# Load the image
image = cv2.imread('qr-code5.png', cv2.IMREAD_GRAYSCALE)  # Load in grayscale

# Apply binary thresholding
_, binary_image = cv2.threshold(image, 40, 255, cv2.THRESH_BINARY)  #

# Stack the original and binary images side by side
combined_image = np.hstack((image, binary_image))

# Resize the combined image for better viewing (if needed)
scale_percent = 200  # Scale up to 200% of the original size
width = int(combined_image.shape[1] * scale_percent / 100)
height = int(combined_image.shape[0] * scale_percent / 100)
resized_image = cv2.resize(combined_image, (width, height), interpolation=cv2.INTER_AREA)

# Display the combined image
cv2.imshow("Original and Binary Image", resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

