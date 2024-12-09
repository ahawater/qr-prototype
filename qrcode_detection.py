import cv2
import math
import matplotlib.pyplot as plt

def calculate_distance(p1, p2):
    """
    Calculate the Euclidean distance between two points.
    :param p1: First point (x, y).
    :param p2: Second point (x, y).
    :return: Distance between p1 and p2.
    """
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def detect_qr_code(image_number):
    """
    Detect QR code in an image and calculate the average length of the two shortest lines
    from the detected triangle points.
    :param image_path: Path to the image.
    :return: Average length of the two shortest lines if QR code detected; otherwise None.
    """
    # Load the image
    image = cv2.imread(f"data/experiment/{image_number}.jpg")

    # Initialize QR Code Detector
    qr_detector = cv2.QRCodeDetector()

    # Detect QR codes in the image
    data, points, _ = qr_detector.detectAndDecode(image)
    if points is not None:
        # `points` is an array of four corner points of the QR code
        points = points[0]
        print(f"QR Code {image_number} away")

        # Define the triangle points (top-left, top-right, bottom-left)
        triangle_points = [
            tuple(map(int, points[0])),  
            tuple(map(int, points[1])),  
            tuple(map(int, points[3]))   
        ]

        # Calculate distances between each pair of points
        distances = [
            (calculate_distance(triangle_points[0], triangle_points[1]), (0, 1)),
            (calculate_distance(triangle_points[1], triangle_points[2]), (1, 2)),
            (calculate_distance(triangle_points[2], triangle_points[0]), (2, 0))
        ]

        # Sort distances to find the two shortest
        distances.sort(key=lambda x: x[0])
        shortest_two = distances[:2]

        # Calculate the average length
        average_length = sum([dist[0] for dist in shortest_two]) / 2

        # Draw the two shortest lines
        for _, (i, j) in shortest_two:
            start_point = triangle_points[i]
            end_point = triangle_points[j]
            cv2.line(image, start_point, end_point, (0, 255, 0), 1)

        # Display the image with the lines
        # cv2.imshow("QR Code Detection", image)
        # cv2.waitKey(10000)
        # cv2.destroyAllWindows()

        plt.figure()
        plt.title(f"QR code {image_number} cm displaced")
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        return average_length
    else:
        print(f"No QR Code detected!")
        return None

# Test with images and calculate X2
image_numbers = [0, 0.25, 0.5, 1, 2, 4, 8, 81, 82]
X1 = 75  # Given value for the first image in cm
u1 = detect_qr_code(image_numbers[0])

print(f"For image {image_numbers[0]}: X1 = {X1:.2f} cm")
if u1:
    for i in range(1, len(image_numbers)):
        u2 = detect_qr_code(image_numbers[i])
        if u2:
            X2 = X1 * (u1 / u2)
            print(f"For image {image_numbers[i]}: X2 = {X2:.2f} cm")
        else:
            print(f"Skipping calculation for {image_numbers[i]} due to missing QR code.")

plt.show()

