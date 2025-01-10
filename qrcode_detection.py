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

def detect_qr_code(image_number, qr_number):
    """
    Detect QR code in an image and calculate the average length of the two shortest lines
    from the detected triangle points.
    :param image_path: Path to the image.
    :return: Average length of the two shortest lines if QR code detected; otherwise None.
    """
    # Load the image
    image = cv2.imread(f'data/daheng/{image_number}_QR_{qr_number}.png')

    # Initialize QR Code Detector
    qr_detector = cv2.QRCodeDetector()

    # Detect QR codes in the image
    data, points, _ = qr_detector.detectAndDecode(image)
    if points is not None:
        # `points` is an array of four corner points of the QR code
        points = points[0]

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


        plt.figure()
        plt.title(f"QR code {image_number} cm displaced")
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        #plt.show()
        plt.axis('off')

        return average_length
    else:
        print(f"No QR Code detected!")
        return None

# Test with images and calculate X2
X1 = 750  # Given value for the first image in mm
print("without sift")
for i in range (3):
    print(f"QR {i}")
    u1 = detect_qr_code(0, i)
    for j in range (1, 7):
        u2 = detect_qr_code(j, i)
        X2 = X1 * (u1 / u2)
        print(f"For image {j}: displacement = {X1 - X2:.1f} mm")

#plt.show()

