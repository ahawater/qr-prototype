import cv2
from qreader import QReader
from datetime import datetime
from math import sqrt

# Initialize qreader detector
qr_detector = QReader()
LOWER_CAMERA = 0
UPPER_CAMERA = 1

def detect_qr(image, camera_type: int, i):

    detections = qr_detector.detect_and_decode(image, return_detections=True)
    detected_codes = detections[0]
    information_detected_codes = detections[1]

    if len(detected_codes) == 0:
        print("WARNING: NO QR CODES DETECTED")
        error = True
        return error, 0, 0, "Error" #TODO: maybe change?
    
    #TODO: sometimes the crop will get a qr code underneath, should not get an error but get the one higher up, to be tested specifically
    elif len(detected_codes) > 1: 
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
    path = f"{i}, conf {confidence}, code {detected_code}.png"

    if camera_type == LOWER_CAMERA:
        x, y = information['cxcy']
        x1,y1,x2,y2 = information['bbox_xyxy']  
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.circle(image, (int(x), int(y)), 10, (0, 255, 0), -1) 
        cv2.imwrite(path, image)
        return
    elif camera_type == UPPER_CAMERA:
        x1,y1,x2,y2 = information['bbox_xyxy']
        y2 = y1 #diagonal to upper side (more accurate)
        u = sqrt((x1-x2)**2 + (y1-y2)**2)
        cv2.line(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
        cv2.imwrite(path, image)
        return
    else:
        raise ValueError(f"Invalid camera type: {camera_type}")


for i in range(3, 18):
    image = cv2.imread(f"{i}_sharpened.jpg")
    detect_qr(image, LOWER_CAMERA, i)