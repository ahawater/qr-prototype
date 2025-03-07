import matplotlib.pyplot as plt
import cv2

# Load the image
image = cv2.imread("upper camera after.jpg")  # Replace with your image
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB for correct colors

# Function to capture mouse click
def onclick(event):
    if event.xdata is not None and event.ydata is not None:  # Ensure click is within the image
        x, y = int(event.xdata), int(event.ydata)
        print(f"Selected Coordinates: ({x}, {y})")

# Display the image
fig, ax = plt.subplots()
ax.imshow(image)
fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
