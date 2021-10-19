import cv2
from matplotlib import pyplot as plt
cap = cv2.VideoCapture("D:/paCong/bandicam 2021-10-18 17-07-19-842.mp4")

ret, frame = cap.read()

img = cv2.imread('d:/1.jpg')#0-400 0-300
plt.imshow(frame)
plt.show()
if cv2.waitKey() == ord("q"):

    cv2.destroyAllWindows()