import cv2
from urllib.request import urlopen
import sys
host = "169.254.43.128:8080"
if len(sys.argv)>1:
    host = sys.argv[1]
hoststr = 'http://' + host + '/?action=stream'
print ('Streaming ' + hoststr)
print ('Print Esc to quit')
stream=urlopen(hoststr)
cap = cv2.VideoCapture(hoststr)
while True:
    ret, frame = cap.read()
    cv2.imshow("xiaorun", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit(0)
