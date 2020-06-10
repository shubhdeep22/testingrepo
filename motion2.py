import cv2
import  numpy as np
from cv2 import aruco
import serial
import time
import math
import matrixc as matrix
import dijkstras as dj

def getCorners(img):
    #y=1
    #while y==1:
    while True:
        img = getSnapshot()
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        # img = aruco.drawMarker(aruco_dict, 11, 400)
        parameters = aruco.DetectorParameters_create()
        # try:
        corners, ids, _ = aruco.detectMarkers(img, aruco_dict, parameters=parameters)
        # if corners[0][0]:
        try:
            print('ignore')
            print(corners[0][0][0])
        except:
            continue
        print('Corners:',corners[0][0])
        array = np.array([corners[0][0][0],corners[0][0][1],corners[0][0][2],corners[0][0][3]])
        return array
    # except:
    #     getCorners(img)
        # else:
        #     print('NOoooo')

def getSnapshot():
    _, frame = cap.read()
    img = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
    return img

def getCentroid(img):
    corners =getCorners(img)
    x = y = 0
    for i in range(4):
        y=y+corners[i][0]
        x=x+corners[i][1]
    return np.array([x/4,y/4]),np.array([y/4,x/4])

def getDistance(x,y):
    return math.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)

def align(z):
    img = getSnapshot()
    np.array(z)
    bot_center,bot_center1 = getCentroid(img)
    print(bot_center1)
    corners =getCorners(img)

    v=np.complex(z[1]-bot_center1[1],z[0]-bot_center1[0])
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
        #Arduino('f')
        return

def goto(p):
    r = (p-1)//n
    c = (p-1)%n
    print('Bot to go at at:',r,c)
    img = getSnapshot()
    bot_center,bot_center1 = getCentroid(img)
    print('bot:',bot_center)
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
        print('distance=======',dist)

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
#frame = cv2.imread('img2.jpeg',1)
r = cv2.selectROI('ROI',frame)
img = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

def matrixo():
    img=getSnapshot()
    # a= matrix.getMatrix(img)
    a = np.array([[14,1,2,1,12],[2,1,4,2,3],[7,2,1,3,5],[4,3,3,3,4],[15,1,3,2,11]])
    print(a)
    return a
ser = serial.Serial('COM4', 9600)
def umatrix(x1,y1):
    #FOR RED UPPDATE
    contours, hirarchy = cv2.findContours(matrix.thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)

        cen = cv2.moments(cnt)
        # Area = cv2.contourArea(contours[index])
        # Perimeter = cv2.arcLength(contours[index], True)

        if len(approx) < 7:
            cv2.drawContours(matrix.thr, cnt, -1, ([255, 0, 0]), 2)
            print('', end='')
            cx = int(cen['m10'] / cen['m00'])
            cy = int(cen['m01'] / cen['m00'])
            x = (cx * 5) // matrix.b[0][1]
            y = (cy * 5) // matrix.b[0][0]
            if y == x1 and x == y1:
             a[y][x] = 3
        else:
            cv2.drawContours(matrix.thr, cnt, -1, ([0, 255, 0]), 3)
            cx = int(cen['m10'] / cen['m00'])
            cy = int(cen['m01'] / cen['m00'])
            x = (cx * 5) // matrix.b[0][1]
            y = (cy * 5) // matrix.b[0][0]
            if y == x1 and x == y1:
             a[y][x] = 4
    #FOR YELLOW UPDATE
    contours, hirarchy = cv2.findContours(matrix.thy, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)

        cen = cv2.moments(cnt)
        # Area = cv2.contourArea(contours[index])
        # Perimeter = cv2.arcLength(contours[index], True)

        if len(approx) < 7:
            cv2.drawContours(matrix.thy, cnt, -1, ([255, 0, 0]), 2)
            print('', end='')
            cx = int(cen['m10'] / cen['m00'])
            cy = int(cen['m01'] / cen['m00'])
            x = (cx * 5) // matrix.b[0][1]
            y = (cy * 5) // matrix.b[0][0]
            if y==x1 and x==y1:
             a[y][x] = 3
        else:
            cv2.drawContours(matrix.thy, cnt, -1, ([0, 255, 0]), 3)
            cx = int(cen['m10'] / cen['m00'])
            cy = int(cen['m01'] / cen['m00'])
            x = (cx * 5) // matrix.b[0][1]
            y = (cy * 5) // matrix.b[0][0]
            if y == x1 and x == y1:
             a[y][x] = 4
def move(path):
    for p in path:
        print('----------------------------Going to:', p, '--------------------------------')
        goto(p)
        print('arrived', p)
a=matrixo()
def findpos(k):
    c=0
    for i in range(5):
        for j in range(5):
           c=c+1
           if (a[i][j]==k):
                break
        if(a[i][j]==k):
            break
    # print(:',c)
    return c

c=0
for i in range(5):
        for j in range(5):
           c=c+1
           if (a[i][j]==14):
                x1=i
                y1=j
                break
        if(a[i][j]==14):
            break

print('---------------Start:',findpos(5))
print('---------------End:',findpos(14))
#time.sleep(5)
path =dj.getPath(a,findpos(5),findpos(14),1)
path=np.array(path)
path=np.delete(path,[0])
path = np.delete(path,[len(path)-1])
print(path)
move(path)
# Arduino('d')
print('Go back to blue')
path=dj.getPath(a,findpos(14),findpos(5),1)
path=np.delete(path,[0])
path=np.array(path)
move(path)
#Arduino('u')
umatrix(x1,y1)


if a[x1][y1]==11:
    h='srg'
elif a[x1][y1]==12:
    h='syg'
elif a[x1][y1]==13:
    h='sbg'
elif a[x1][y1]==15:
    h='crg'
elif a[x1][y1]==16:
    h='cyg'
else:
    h='cbg'

path=dj.getPath(a,findpos(5),findpos(7),h)
path=np.array(path)
move(path)
#Arduino('d')
path=dj.getPath(a,findpos(7),findpos(5),h)
path=np.array(path)
move(path)
#Arduino('u')

print('Completed')

