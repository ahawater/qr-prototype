import cv2
from qreader import QReader
from datetime import datetime
from math import sqrt
import os

# Initialize qreader detector
qr_detector = QReader()
LOWER_CAMERA = 0
UPPER_CAMERA = 1

def detect_qr(image, camera_type: int):

    detections = qr_detector.detect_and_decode(image, return_detections=True)
    detected_codes = detections[0]
    information_detected_codes = detections[1]

    if len(detected_codes) == 0:
        print("WARNING: NO QR CODES DETECTED")
        error = True
        return error, 0, 0, "Error" #TODO: maybe change?

    elif len(detected_codes) > 1: #TODO: sometimes the crop will get a qr code underneath, should not get an error but get the one higher up, to be tested specifically
        print("WARNING: MULTIPLE QR CODES DETECTED")
        error = True
        return error, 0, 0, "Error" #TODO: maybe change?


    detected_code = detected_codes[0]
    if detected_code is not None:
        detected_code = detected_code.replace('/', '_')
    else:
        detected_code = "None"

    information = information_detected_codes[0]
    confidence = round(information['confidence'], 2)
    error = False
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path = f"../output/time {time}, confidence {confidence}, detected_code {detected_code}.png"

    if camera_type == LOWER_CAMERA:
        x, y = information['cxcy']
        cv2.circle(image, (int(x), int(y)), 10, (0, 255, 0), -1) 
        cv2.imwrite(path, image)
        return error, x, y, detected_code #TODO: maybe change?
    elif camera_type == UPPER_CAMERA:
        x1,y1,x2,y2 = information['bbox_xyxy']
        y2 = y1 #diagonal to upper side (more accurate)
        u = sqrt((x1-x2)**2 + (y1-y2)**2)
        cv2.line(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
        cv2.imwrite(path, image)
        return error, u, detected_code
    else:
        raise ValueError(f"Invalid camera type: {camera_type}")

#OUTDATED CODE: to test inference time
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

#NOTE: shorter inference for smaller images, logging takes an extra 20ms.