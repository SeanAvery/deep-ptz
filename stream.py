import cv2
from autofocus.Manager import Manager

if __name__ == '__main__':
    pipeline = (
        "nvarguscamerasrc wbmode=1 !"
        "nvvidconv flip-method=2 ! "
        "videoconvert ! video/x-raw, format=(string)BGR !"
        "appsink"        
    )
    env = Manager()
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    if cap.isOpened():
        prev_score = 0
        moves = {
            'in': 3,
            'out': 4,
        }
        move = 'in'
        while True:
            cv2.namedWindow("Raw", cv2.WINDOW_AUTOSIZE)
            cv2.namedWindow("Proc")
            _, frame = cap.read()
            proc = frame.copy()
            proc = cv2.Laplacian(frame, cv2.CV_64F)
            score = cv2.mean(proc)[0]
            print('proc score', score)
            diff = score - prev_score
            print('diff', diff)
            if diff >= 0:
                env.move(move)
            if diff < 0:
                if move == 'in':
                    move = 'out'
                    env.move(moves[move])
                if move == 'out':
                    move = 'in'
                    env.move(moves[move])
            cv2.imshow("Raw", frame)
            cv2.imshow("Proc", proc)
            cv2.waitKey(1)
