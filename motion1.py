import cv2
import  numpy as np
from cv2 import aruco
import serial
import time
import math
# import matrixc as matrix

def getCorners(img):
    #y=1
    #while y==1:
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    # img = aruco.drawMarker(aruco_dict, 11, 400)
    parameters = aruco.DetectorParameters_create()
    corners, ids, _ = aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    if(len(corners[0][0])==0):
        getCorners(img)
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

    v=np.complex(z[1]-bot_center[1],z[0]-bot_center[0])
    w=np.complex(corners[0][1]-corners[3][1],corners[0][0]-corners[3][0])
    t=(np.angle(v)-np.angle(w))
    if(t>3.14):
        t=-3.14
    if (t < -3.14):
        t = 3.14
    print('Angle:',t*180/3.14)
    if t>(3.14/18):
        #Rleft()
        Arduino('l')
        time.sleep(0.05)
        align(z)
    elif t<-(3.14 / 18):
        #Rright()
        Arduino('r')
        time.sleep(0.05)
        align(z)
    else:
        #forward()
        return

def goto(p):
    r = (p-1)//n
    c = (p-1)%n
    print('Bot to go at:',r,c)
    img = getSnapshot()
    bot_center = getCentroid(img)
    print('bot at:',bot_center)
    l, b, _ = img.shape
    print('shape:',l,b)
    z = np.array([r*(l/n)+l/(2*n),c*(b/n)+b/(2*n)])
    print('next:',z)
    dist = getDistance(bot_center, z)
    err = 10
    while dist > err:
        align(z)
        Arduino('f')
        time.sleep(0.3)
        img = getSnapshot()
        bot_center = getCentroid(img)
        dist = getDistance(bot_center, z)
        print('Distance:',dist)

def Arduino(x):

    if x == 'f':
        print("FORWARD")
        ser.write(b'f')
        time.sleep(0.3)
        print("Stop")
        ser.write(b's')
    elif x == 'l':
        ser.write(b'l')
        print("left")
        time.sleep(0.2)
        ser.write(b's')
    elif x == 'r':
        ser.write(b'r')
        print("right")
        time.sleep(0.2)
        ser.write(b's')
    elif x == 's':
        ser.write(b's')


##############################MAIN CODE####################
n = 5
cap=cv2.VideoCapture(1)
_,frame = cap.read()
#cv2.imwrite('arena_5x5.png',frame)
# frame = cv2.imread('arena_5x5.png')
r = cv2.selectROI('ROI',frame)
img = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
# mat = matrix.getMatrix(img)
path = [24,25,19]
ser = serial.Serial('COM4',9600)

for p in path:
    print('----------------------------Going to:', p,'--------------------------------')
    goto(p)
    print('arrived',p)

print('Completed')

