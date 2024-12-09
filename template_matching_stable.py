import cv2
import numpy as np

# Load the image and template
image = cv2.imread('qr-code6.png')  # Main image
template = cv2.imread('template.jpg')  # Template to match

# Convert the image and template to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# Get the dimensions of the template
template_height, template_width = gray_template.shape

# Set the fixed scaling factor 
scale_factor = 1  

# Resize the template to the scaling factor (7 times smaller)
resized_template = cv2.resize(gray_template, 
                              (int(template_width * scale_factor), int(template_height * scale_factor)))

# Apply template matching
result = cv2.matchTemplate(gray_image, resized_template, cv2.TM_CCOEFF_NORMED)

# Find the locations where the result has a high correlation
threshold = 0.5  # Adjust threshold for high correlation
locations = np.where(result >= threshold)

# List to store the top matches
matches = []

# Loop through all matches
for loc in zip(*locations[::-1]):
    top_left = loc
    bottom_right = (top_left[0] + resized_template.shape[1], top_left[1] + resized_template.shape[0])
    
    # Store the match location and score
    matches.append((result[top_left[1], top_left[0]], top_left, bottom_right))

# Sort matches by score (highest first)
matches = sorted(matches, key=lambda x: x[0], reverse=True)

# Select the top 3 matches, but make sure they are far apart
selected_matches = []
min_distance = 10  # Minimum distance (in pixels) between selected matches

for match in matches:
    score, top_left, bottom_right = match
    
    # Check if the current match is far enough from the selected ones
    if len(selected_matches) == 0:
        selected_matches.append(match)
    else:
        # Check the distance between the current match and all selected matches
        distance_ok = True
        for selected in selected_matches:
            selected_top_left = selected[1]
            distance = np.linalg.norm(np.array(top_left) - np.array(selected_top_left))
            if distance < min_distance:
                distance_ok = False
                break
        
        if distance_ok:
            selected_matches.append(match)
    
    # Stop once we have 3 matches
    if len(selected_matches) == 3:
        break

# Draw rectangles around the top matches
for i, (score, top_left, bottom_right) in enumerate(selected_matches):
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)  # Green rectangle

    # Optionally, print the score of each match
    print(f"Match {i+1}: Score = {score}, Top-left = {top_left}, Bottom-right = {bottom_right}")

# Display the image with rectangles around the selected matches
cv2.imshow("Top 3 Matches (Far Apart)", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
