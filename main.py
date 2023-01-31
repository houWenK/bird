from detector import Detector
import cv2

if __name__ == '__main__':
    detector = Detector()
    im = cv2.imread('./images/3.jpg')
    bboxes = detector.detect(im)
    print(bboxes)

