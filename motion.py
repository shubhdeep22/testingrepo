import cv2
import  numpy as np
from cv2 import aruco
import serial
import time
import math
# import matrixc as matrix

def getCorners(img):

    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    # img = aruco.drawMarker(aruco_dict, 11, 400)
    parameters = aruco.DetectorParameters_create()
    corners, ids, _ = aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    print('Aruco detected')
    print('Corners:',corners[0][0])
    array = np.array([corners[0][0][0],corners[0][0][1],corners[0][0][2],corners[0][0][3]])
    return array

def getSnapshot():
    _, frame = cap.read()
    img = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
    return img

def getCentroid(img):
    corners =getCorners(img)
    x = y = 0
    for i in range(4):
        x=x+corners[i][0]
        y=y+corners[i][1]
    return np.array([x/4, y/4])

def getDistance(x,y):
    return math.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)

def align(z):
    img = getSnapshot()
    np.array(z)
    bot_center = getCentroid(img)
    corners =getCorners(img)
    b2=z[1]-bot_center[1]
    a2=z[0]-bot_center[0]
    b1=(corners[2][1]-corners[0][1])
    a1=(corners[2][0]-corners[0][0])
    d=(a1*a2+b1*b2)/((math.sqrt(a1**2+b1**2))*(math.sqrt(a2**2+b2**2)))
    angle=math.acos(d)
    angle=angle*(180/3.14)
    print('Angle(in degrees):',angle)
    if angle>10 and angle<90:
        #Rleft()
        Arduino('r')
        time.sleep(0.05)
        align(z)
    else:
        #Rright()
        Arduino('f')
        time.sleep(0.05)
        return

def goto(p):
    r = (p-1)//n
    c = (p-1)%n
    # print('Bot at:',r,c)
    img = getSnapshot()
    bot_center = getCentroid(img)
    l, b, _ = img.shape
    z = np.array([r*(l/n)+l/(2*n),c*(b/n)+b/(2*n)])
    dist = getDistance(bot_center, z)
    err =10
    while dist > err:
        align(z)
        print('f')
        Arduino('f')
        time.sleep(0.1)
        img = getSnapshot()
        bot_center = getCentroid(img)
        dist = getDistance(bot_center, z)

def Arduino(x):

    if x == 'f':
        print("FORWARD")
        ser.write(b'f')
        time.sleep(0.1)
        print("Stop")
        ser.write(b's')
    elif x == 'l':
        ser.write(b'l')
        print("left")
        time.sleep(0.1)
        ser.write(b's')
    elif x == 'r':
        ser.write(b'r')
        print("right")
        time.sleep(0.1)
        ser.write(b's')
    elif x == 's':
        ser.write(b's')


##############################MAIN CODE####################
n = 5
cap=cv2.VideoCapture(1)
_,frame = cap.read()
r = cv2.selectROI('ROI',frame)
img = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
# mat = matrix.getMatrix(img)
path = [24,25,20,19]
ser = serial.Serial('COM3',9600)

for p in path:
    print('Going to:', p)
    goto(p)

print('Completed')

