import cv2
from autofocus.Manager import Manager

if __name__ == '__main__':
    debug = False
    pipeline = (
        "nvarguscamerasrc wbmode=1 sensor_id=1 !"
        "nvvidconv flip-method=2 ! "
        "videoconvert ! video/x-raw, format=(string)BGR !"
        "appsink"        
    )
    env = Manager()
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    if cap.isOpened():
        prev_score = 0
        moves = {
            'in': 2,
            'out': 3,
        }
        move = 'in'
        while True:
            cv2.namedWindow("Raw", cv2.WINDOW_AUTOSIZE)
            cv2.namedWindow("Proc")
            _, frame = cap.read()
            print('moved', move)
            cv2.imshow("Raw", frame)
            # cv2.imshow("Proc", proc)
            cv2.waitKey(1)
