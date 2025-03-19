import cv2

# Load the image
image_path = "data/lower camera 0.jpg"  # Your provided image path
image = cv2.imread(image_path)
clone = image.copy()

# Set a maximum width for displaying
max_width = 1800  # Maximum width for displaying (adjust as needed)
height, width = image.shape[:2]
aspect_ratio = width / float(height)

# Calculate new dimensions based on the maximum width
new_width = max_width
new_height = int(new_width / aspect_ratio)

# Resize the image to fit the screen while maintaining the aspect ratio
resized_image = cv2.resize(image, (new_width, new_height))

crop_count = 3  # Start naming from 3.jpg
crops_needed = 15  # Number of crops

def select_roi():
    global crop_count, resized_image, clone
    
    while crop_count <= 17:
        # Reset the image to the original each time
        image_to_show = resized_image.copy()
        
        # Select the region of interest (ROI) manually
        roi = cv2.selectROI("Select Crop Area", image_to_show, showCrosshair=True, fromCenter=False)
        
        # If a valid ROI is selected, save it
        if roi[2] > 0 and roi[3] > 0:  # Ensure width & height are positive
            x, y, w, h = roi

            # Map the resized coordinates back to the original image
            scale_x = width / float(new_width)
            scale_y = height / float(new_height)

            # Correct the coordinates based on the scaling
            x_original = int(x * scale_x)
            y_original = int(y * scale_y)
            w_original = int(w * scale_x)
            h_original = int(h * scale_y)

            # Crop from the original image
            cropped_image = clone[y_original:y_original+h_original, x_original:x_original+w_original]

            # Rotate the cropped image 90 degrees clockwise
            rotated_image = cv2.rotate(cropped_image, cv2.ROTATE_90_CLOCKWISE)

            # Save the rotated crop
            cv2.imwrite(f"{crop_count}.jpg", rotated_image)
            print(f"Saved {crop_count}.jpg")
            crop_count += 1
        else:
            print("Invalid ROI selected, try again.")
        
        # If the crop count reaches 18, break the loop
        if crop_count > 17:
            break

    cv2.destroyAllWindows()

print("Click and drag to select a region to crop, press 'ESC' when done.")
select_roi()
print("Cropping completed!")
