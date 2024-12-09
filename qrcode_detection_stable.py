import cv2

def calculate_triangle_area(points):
    """
    Calculate the area of a triangle using the shoelace formula.
    :param points: List of three points (x, y) forming the triangle.
    :return: Area of the triangle.
    """
    x1, y1 = points[0]
    x2, y2 = points[1]
    x3, y3 = points[2]
    
    # Shoelace formula
    area = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2
    return area

def detect_qr_code(image_number):
    # Load the image
    image = cv2.imread(f'data/yolo/{image_number}.png')

    # Initialize QR Code Detector
    qr_detector = cv2.QRCodeDetector()

    # Detect QR codes in the image
    data, points, _ = qr_detector.detectAndDecode(image)
    if points is not None:
        # `points` is an array of four corner points of the QR code
        points = points[0]
        print("QR Code detected!")

        # Define the triangle points (top-left, top-right, bottom-left)
        triangle_points = [
            tuple(map(int, points[0])),  # Top-left
            tuple(map(int, points[1])),  # Top-right
            tuple(map(int, points[3]))   # Bottom-left
        ]

        # Calculate the area of the triangle
        area = calculate_triangle_area(triangle_points)
        print(f"Area of the triangle: {area} pixels²")

        # Draw the triangle
        for i in range(3):
            start_point = triangle_points[i]
            end_point = triangle_points[(i + 1) % 3]
            cv2.line(image, start_point, end_point, (0, 255, 0), 2)

        # Display the image with the triangle
        cv2.imshow("QR Code Detection", image)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
    else:
        print("No QR Code detected!")

# Test with images
images = ["far", "close", "far2"]
for i in range(1, 27):
    detect_qr_code(i)
