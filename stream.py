import cv2
import matplotlib.pyplot as plt

# Open the webcam (0 = default camera, change if needed)
cap = cv2.VideoCapture(1)

# Check if the webcam is opened
if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

# Capture a single frame
ret, frame = cap.read()

# Release the webcam
cap.release()

# Check if frame was captured
if not ret:
    print("Error: Could not capture image")
    exit()

# Convert BGR (OpenCV default) to RGB (for Matplotlib)
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Show the image using Matplotlib
plt.imshow(frame)
plt.axis("off")  # Hide axis
plt.title("Captured Image")
plt.show()
