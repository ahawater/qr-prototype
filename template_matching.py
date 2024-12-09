import cv2
import numpy as np

def template_matching(image_number):
    # Load the image and template
    image = cv2.imread(f'data/yolo/{image_number}.png')  # Main image
    template = cv2.imread('data/template.jpg')  # Template to match

    # Convert the image and template to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Get the dimensions of the template
    image_height, image_width = gray_image.shape

    # Set the fixed scaling factor 
    scale_factor = 9/33  #should be 9/33

    # Resize the template to the scaling factor (if necessary)
    resized_template = cv2.resize(gray_template, 
                                  (int(image_width * scale_factor), int(image_height * scale_factor)))

    # Apply template matching
    result = cv2.matchTemplate(gray_image, resized_template, cv2.TM_CCOEFF_NORMED)

    # Flatten the result matrix and find the top scores
    flat_result = result.flatten()
    top_indices = np.argsort(flat_result)[-50:][::-1]  # Extract 50 max scores to filter later

    # Convert indices back to 2D positions
    rows, cols = result.shape
    match_positions = [(idx % cols, idx // cols, flat_result[idx]) for idx in top_indices]

    # Ensure matches are far apart
    selected_matches = []
    min_distance = 100  # Minimum distance (in pixels) TODO: make it normalized

    for col, row, score in match_positions:
        if len(selected_matches) == 0:
            selected_matches.append(((col, row), score))
        else:
            # Check distance from already selected matches
            far_enough = all(
                np.linalg.norm(np.array((col, row)) - np.array(selected[0])) > min_distance
                for selected in selected_matches
            )
            if far_enough:
                selected_matches.append(((col, row), score))
        if len(selected_matches) == 3:
            break

    # Draw rectangles around the top matches
    for i, ((col, row), score) in enumerate(selected_matches):
        top_left = (col, row)
        bottom_right = (col + resized_template.shape[1], row + resized_template.shape[0])
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)  # Green rectangle

        # Calculate the center of the rectangle
        center = (int((col + (col + resized_template.shape[1])) / 2), 
                  int((row + (row + resized_template.shape[0])) / 2))

        # Draw a red circle at the center
        cv2.circle(image, center, 5, (0, 0, 255), -1)  # Red circle

    # Display the image with rectangles
    cv2.imshow("Top 3 Matches", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

template_matching(5)

