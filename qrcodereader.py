import cv2
from qreader import QReader
import time

# Initialize qreader detector
qr_detector = QReader()

def detect_qr(image):
    # Detect QR code using qreader
    detections = qr_detector.detect_and_decode(image, return_detections=True)
    detected_codes = detections[0]
    information_detected_codes = detections[1]

    # Plot result
    if len(detected_codes) > 1:
        print("WARNING: MULTIPLE QR CODES DETECTED")

    for i in range(len(detected_codes)):

        detected_code = detected_codes[i]
        if detected_code is not None:
            detected_code = detected_code.replace('/', '_')
        information = information_detected_codes[i]
        x, y = information['cxcy']
        confidence = round(information['confidence'], 2)

        # Draw a point at the center of the detected QR code
        cv2.circle(image, (int(x), int(y)), 10, (0, 255, 0), -1)  # Green dot
        cv2.imwrite(f"confidence {confidence}, detected_code {detected_code}.png", image)  #log either date, or have a txt file with the date and time of the image
        #this repo stays private, just 


image = cv2.imread("2 qr codes.jpg")
time_taken = []

for i in range (1):
    before = time.time()
    detect_qr(image)
    after = time.time()
    time_taken.append(after - before)

for i in range(len(time_taken)):
    print(f"Time taken for iteration {i+1}: {time_taken[i]} seconds")
