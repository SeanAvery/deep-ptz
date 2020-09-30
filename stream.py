import cv2

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
            window = cv2.namedWindow("Camera")
            _, frame = cap.read()
            cv2.imshow("Camera", frame)
            cv2.waitKey(1)
