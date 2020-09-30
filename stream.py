import cv2
from controls.Verifocal import Focuser

if __name__ == '__main__':
    pipeline = (
        "nvarguscamerasrc wbmode=1 !"
        "nvvidconv flip-method=2 ! "
        "videoconvert ! video/x-raw, format=(string)BGR !"
        "appsink"        
    )
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    if cap.isOpened():
        while True:
            cv2.namedWindow("Raw", cv2.WINDOW_AUTOSIZE)
            cv2.namedWindow("Proc")
            _, frame = cap.read()
            proc = frame.copy()
            proc = cv2.Laplacian(frame, cv2.CV_64F)
            score = cv2.mean(proc)[0]
            print('proc score', score)
            cv2.imshow("Raw", frame)
            cv2.imshow("Proc", proc)
            cv2.waitKey(1)
