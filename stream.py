import cv2
from autofocus.Manager import Manager

if __name__ == '__main__':
    debug = False
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
            'in': 2,
            'out': 3,
        }
        move = 'in'
        while True:
            cv2.namedWindow("Raw", cv2.WINDOW_AUTOSIZE)
            cv2.namedWindow("Proc")
            _, frame = cap.read()
            proc = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            proc = cv2.Laplacian(proc, cv2.CV_64F)
            # proc = cv2.Sobel(proc, cv2.CV_64F, 1, 1)
            score = cv2.mean(proc)[0]
            print('proc score', score)
            diff = score - prev_score
            print('diff', score, '-', prev_score, ':', diff)
            prev_score = score
            if diff >= 0:
                env.move(moves[move])
            if diff < 0:
                if move == 'in':
                    move = 'out'
                    env.move(moves[move])
                elif move == 'out':
                    move = 'in'
                    env.move(moves[move])
            print('moved', move)
            cv2.imshow("Raw", frame)
            cv2.imshow("Proc", proc)
            cv2.waitKey(1)
