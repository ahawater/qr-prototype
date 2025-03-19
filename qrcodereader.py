import cv2
from qreader import QReader
from datetime import datetime
from math import sqrt

# Initialize qreader detector
qr_detector = QReader()
LOWER_CAMERA = 0
UPPER_CAMERA = 1

def detect_qr(image, camera_type: int):

    detections = qr_detector.detect_and_decode(image, return_detections=True)
    detected_codes = detections[0]
    information_detected_codes = detections[1]

    for i in range(len(detected_codes)):
        information = information_detected_codes[i]
        detected_code = detected_codes[i]
        if detected_code is not None:
            detected_code = detected_code.replace('/', '_')

        if detected_code is None:
            detected_code = "None"

        confidence = round(information['confidence'], 2)
        error = False
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        path = f"output/{i}, time {time}, confidence {confidence}, detected_code {detected_code}.png"

        if camera_type == LOWER_CAMERA:
            x, y = information['cxcy']
            cv2.circle(image, (int(x), int(y)), 10, (0, 255, 0), -1) 
            cv2.imwrite(path, image)
        elif camera_type == UPPER_CAMERA:
            x1,y1,x2,y2 = information['bbox_xyxy']
            y2 = y1 #diagonal to upper side (more accurate)
            u = sqrt((x1-x2)**2 + (y1-y2)**2)
            cv2.line(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
            cv2.imwrite(path, image)
        else:
            raise ValueError(f"Invalid camera type: {camera_type}")
    return
        
if __name__ == "__main__":
    image = cv2.imread('data/multiple qr codes.png')
    detect_qr(image, LOWER_CAMERA)
    print("Done")