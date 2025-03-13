import cv2
from qreader import QReader
import time
from datetime import datetime
from math import sqrt
import os

# Initialize qreader detector
qr_detector = QReader()

def detect_qr(image):
    lower_camera = False
    # Detect QR code using qreader
    detections = qr_detector.detect_and_decode(image, return_detections=True)
    detected_codes = detections[0]
    information_detected_codes = detections[1]

    # Plot result
    if len(detected_codes) > 1: #TODO: sometimes the crop will get a qr code underneath, should not get an error but git the one higher up, to be tested specifically
        print("WARNING: MULTIPLE QR CODES DETECTED")
        error = True
        return 0, 0, "Error", error #TODO: maybe change?

    detected_code = detected_codes[0]
    if detected_code is not None:
        detected_code = detected_code.replace('/', '_')
    else:
        detected_code = "None"
    information = information_detected_codes[0]
    confidence = round(information['confidence'], 2)
    error = False
    if lower_camera:
        x, y = information['cxcy']
        # Draw a point at the center of the detected QR code
        cv2.circle(image, (int(x), int(y)), 10, (0, 255, 0), -1)  # Green dot
        #time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #cv2.imwrite(f"output/time {time}, confidence {confidence}, detected_code {detected_code}.png", image)  #log either date, or have a txt file with the date and time of the image
        #this repo stays private, just upload the important scripts on notion
        return x, y, detected_code, error #TODO: maybe change?
    else:
        x1,y1,x2,y2 = information['bbox_xyxy']
        u = sqrt((x1-x2)**2 + (y1-y2)**2)
        cv2.line(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cv2.imwrite(f"../output/time {time}, confidence {confidence}, detected_code {detected_code}.png", image)  #log either date, or have a txt file with the date and time of the image
        return u, detected_code, error


# time_taken = []

# for i in range (10):
#     image = cv2.imread("data/v.12 lower camera crop.jpg")
#     before = time.time()
#     lower_camera = False
#     u,detected_code, error = detect_qr(image, lower_camera)
#     after = time.time()
#     time_taken.append(after - before)

# for i in range(len(time_taken)):
#    print(f"Time taken for iteration {i+1}: {time_taken[i]} seconds")

#return value of the function should be (x,y), that is it (for the lower camera)
#for the upper camera, it should be u (average of both diagonal?)
#NOTE: shorter inference for smaller images, logging tajes an extra 20ms.