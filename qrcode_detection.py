import cv2
import math
import matplotlib.pyplot as plt

def calculate_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def detect_qr_code(image_number, qr_number):
    image = cv2.imread(f'data/daheng/{image_number}_QR_{qr_number}.png')
    qr_detector = cv2.QRCodeDetector()
    data, points, _ = qr_detector.detectAndDecode(image)

    if points is not None:
        points = points[0]
        triangle_points = [
            tuple(map(int, points[0])),
            tuple(map(int, points[1])),
            tuple(map(int, points[3]))
        ]
        distances = [
            calculate_distance(triangle_points[0], triangle_points[1]),
            calculate_distance(triangle_points[1], triangle_points[2]),
            calculate_distance(triangle_points[2], triangle_points[0])
        ]
        distances.sort()
        average_length = sum(distances[:2]) / 2
        return average_length
    else:
        print(f"No QR Code detected!")
        return None

# Data storage for plotting
displacement_data = {}
X1 = 750  # Given value for the first image in mm
x_axis = [2.5, 5, 10, 20, 40, 80]  # Real displacement in mm

for qr_number in range(3):
    displacement_data[qr_number] = []
    u1 = detect_qr_code(0, qr_number)
    if u1 is None:
        continue
    for image_number in range(1, 7):
        u2 = detect_qr_code(image_number, qr_number)
        if u2 is not None:
            X2 = abs(X1 * (u1 / u2))
            displacement = X1 - X2
            displacement_data[qr_number].append(displacement)
        else:
            displacement_data[qr_number].append(None)

# Plot the data
plt.figure(figsize=(10, 6))
x_axis = [2.5, 5, 10, 20, 40, 80]
for qr_number, displacements in displacement_data.items():
    if qr_number == 1:
        displacements = [a - b for a, b in zip(displacements, x_axis)]
    plt.plot(x_axis, displacements, marker='o', label=f"QR {qr_number}")

# Set graduated x-axis ticks
plt.xticks(x_axis)  # Ensures ticks are at the data points

plt.title("Experiment: displace only QR1, u: opencv detectAndDecode")
plt.xlabel("QR1 real displacement [mm]")
plt.ylabel("Error in measured displacement [mm]")
plt.legend()
plt.grid(True)




plt.show()
