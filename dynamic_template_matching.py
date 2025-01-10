import cv2
import numpy as np

def template_matching(image_number):
    # Load the image and template
    image = cv2.imread(f'data/daheng/{image_number}_QR_1.png')  # Main image
    template = cv2.imread('data/template_small.jpg')  # Template to match

    # Convert the image and template to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Define scaling factors to try
    scale_factors = np.linspace(0.2, 3, 50)  # Adjust the range and steps as needed

    best_matches = []

    for scale in scale_factors:
        # Resize the template to the current scaling factor
        resized_template = cv2.resize(
            gray_template,
            (int(gray_template.shape[1] * scale), int(gray_template.shape[0] * scale))
        )

        # Skip if the template becomes larger than the image
        if resized_template.shape[0] > gray_image.shape[0] or resized_template.shape[1] > gray_image.shape[1]:
            continue

        # Apply template matching
        result = cv2.matchTemplate(gray_image, resized_template, cv2.TM_CCOEFF_NORMED)

        # Flatten the result matrix and find the top scores
        flat_result = result.flatten()
        top_indices = np.argsort(flat_result)[-50:][::-1]  # Top 50 scores

        # Convert indices back to 2D positions
        rows, cols = result.shape
        match_positions = [(idx % cols, idx // cols, flat_result[idx]) for idx in top_indices]

        # Add matches to the overall list with scale information
        for col, row, score in match_positions:
            best_matches.append((col, row, score, scale, resized_template.shape))

    # Sort all matches by score and ensure matches are far apart
    best_matches.sort(key=lambda x: x[2], reverse=True)
    selected_matches = []
    min_distance = 50  # Minimum distance in pixels

    for col, row, score, scale, template_size in best_matches:
        if len(selected_matches) == 0:
            selected_matches.append(((col, row), score, scale, template_size))
        else:
            # Check distance from already selected matches
            far_enough = all(
                np.linalg.norm(np.array((col, row)) - np.array(selected[0])) > min_distance
                for selected in selected_matches
            )
            if far_enough:
                selected_matches.append(((col, row), score, scale, template_size))
        if len(selected_matches) == 3:
            break

    # Draw rectangles around the top matches
    for ((col, row), score, scale, template_size) in selected_matches:
        top_left = (col, row)
        bottom_right = (col + template_size[1], row + template_size[0])
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 1)  # Green rectangle

        # Calculate the center of the rectangle
        center = (int((col + (col + template_size[1])) / 2), 
                  int((row + (row + template_size[0])) / 2))

        # Draw a red circle at the center
        cv2.circle(image, center, 1, (0, 0, 255), -1)  # Red circle

    # Save the image with rectangles
    output_path = f'data/daheng/output/{image_number}_matched.png'  # Adjust the path as needed
    cv2.imwrite(output_path, image)
    print(f"Result saved to {output_path}")

if __name__ == "__main__":
    for i in range (7):
        template_matching(i)
