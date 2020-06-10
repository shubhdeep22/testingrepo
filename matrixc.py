#dijkstar running output in string + shape detection running

import numpy as np
import cv2
# oimg = cv2.imread('img2.jpeg', 1)
thr=0
thy=0
#oimg=0
b=0

def getMatrix(oimg):
    global thr,thy,b
    oimg= cv2.resize(oimg, (700,700))
    # r = cv2.selectROI('ROI',oimg)
    # oimg = oimg[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
    a = (5, 5)
    a = np.zeros(a)
    b = np.array([oimg.shape])

    # 1=RED SQUARE
    # 2=RED CIRCLE
    # 3=YELLOW SQUARE
    # 4=YELLOW CIRCLE
    # 5=BLUE SQUARE
    # 6-BLUE CIRCLE
    # 7=WHITE SQUARE
    # 8=WHITE CIRCLE
    # 9=GREEN SQUARE
    # 10=GREEN CIRCLE
    # 11=GREEN WITH RED SQUARE
    # 15=GREEN WITH RED CIRCLE
    # 12=GREEN WITH YELLOW SQUARE
    # 16=GREEN WITH YELLOW CIRCLE
    # 13=GREEN WITH BLUE SQUARE
    # 17=GREEN WITH BLUE CIRCLE
    # 14=GREEN WITH WHITE SQUARE
    # 18=GREEN WITH WHITE CIRCLE

    def imshow():
        cv2.imshow('thresolded', threshold)
        cv2.waitKey()
        cv2.destroyAllWindows()

    # SELECT RED COLOR
    r = cv2.selectROI('ROI', oimg)
    imcrop = oimg[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

    thresh = 50
    bmin = max(0, imcrop[:, :, 0].min() - thresh)
    gmin = max(0, imcrop[:, :, 1].min() - thresh)
    rmin = max(0, imcrop[:, :, 2].min() - thresh)

    bmax = min(255, imcrop[:, :, 0].max() + thresh)
    gmax = min(255, imcrop[:, :, 1].max() + thresh)
    rmax = min(255, imcrop[:, :, 2].max() + thresh)
    rlower = np.array([bmin, gmin, rmin])
    rupper = np.array([bmax, gmax, rmax])
    threshold = cv2.inRange(oimg, rlower, rupper)
    kernel = np.ones((3, 3), np.uint8)
    threshold = cv2.erode(threshold, kernel, iterations=2)
    threshold = cv2.dilate(threshold, kernel, iterations=1)
    thr=threshold
    contours, hirarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)

        cen = cv2.moments(cnt)
        # Area = cv2.contourArea(cnt)
        # Perimeter = cv2.arcLength(contours[index], True)
        # if Area >500:
        if len(approx) < 7:
            cv2.drawContours(oimg, cnt, -1, ([255, 0, 0]), 2)
            print('', end='')
            cx = int(cen['m10'] / cen['m00'])
            cy = int(cen['m01'] / cen['m00'])

            x = (cx * 5) // b[0][1]
            y = (cy * 5) // b[0][0]

            a[y][x] = 1
        else:
            cv2.drawContours(oimg, cnt, -1, ([0, 255, 0]), 3)
            cx = int(cen['m10'] / cen['m00'])
            cy = int(cen['m01'] / cen['m00'])
            x = (cx * 5) // b[0][1]
            y = (cy * 5) // b[0][0]
            a[y][x] = 2

    imshow()
    # SELECT YELLOW COLOR
    r = cv2.selectROI('ROI', oimg)
    imcrop = oimg[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

    thresh = 50
    bmin = max(0, imcrop[:, :, 0].min() - thresh)
    gmin = max(0, imcrop[:, :, 1].min() - thresh)
    rmin = max(0, imcrop[:, :, 2].min() - thresh)

    bmax = min(255, imcrop[:, :, 0].max() + thresh)
    gmax = min(255, imcrop[:, :, 1].max() + thresh)
    rmax = min(255, imcrop[:, :, 2].max() + thresh)
    rlower = np.array([bmin, gmin, rmin])
    rupper = np.array([bmax, gmax, rmax])
    threshold = cv2.inRange(oimg, rlower, rupper)
    kernel = np.ones((3, 3), np.uint8)
    threshold = cv2.erode(threshold, kernel, iterations=2)

    threshold = cv2.dilate(threshold, kernel, iterations=1)
    thy=threshold
    contours, hirarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)

        cen = cv2.moments(cnt)
        # Area = cv2.contourArea(contours[index])
        # Perimeter = cv2.arcLength(contours[index], True)
        # Area = cv2.contourArea(cnt)
        # if Area > 500:
        if len(approx) < 7:
            cv2.drawContours(oimg, cnt, -1, ([255, 0, 0]), 2)
            print('', end='')
            cx = int(cen['m10'] / cen['m00'])
            cy = int(cen['m01'] / cen['m00'])
            x = (cx * 5) // b[0][1]
            y = (cy * 5) // b[0][0]
            a[y][x] = 3
        else:
            cv2.drawContours(oimg, cnt, -1, ([0, 255, 0]), 3)
            cx = int(cen['m10'] / cen['m00'])
            cy = int(cen['m01'] / cen['m00'])
            x = (cx * 5) // b[0][1]
            y = (cy * 5) // b[0][0]
            a[y][x] = 4

    imshow()
    # FOR BLUE COLOR
    r = cv2.selectROI('ROI', oimg)
    imcrop = oimg[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

    thresh = 50
    bmin = max(0, imcrop[:, :, 0].min() - thresh)
    gmin = max(0, imcrop[:, :, 1].min() - thresh)
    rmin = max(0, imcrop[:, :, 2].min() - thresh)

    bmax = min(255, imcrop[:, :, 0].max() + thresh)
    gmax = min(255, imcrop[:, :, 1].max() + thresh)
    rmax = min(255, imcrop[:, :, 2].max() + thresh)
    rlower = np.array([bmin, gmin, rmin])
    rupper = np.array([bmax, gmax, rmax])
    threshold = cv2.inRange(oimg, rlower, rupper)
    kernel = np.ones((3, 3), np.uint8)
    threshold = cv2.erode(threshold, kernel, iterations=2)
    threshold = cv2.dilate(threshold, kernel, iterations=1)
    contours, hirarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)

        cen = cv2.moments(cnt)
        # Area = cv2.contourArea(contours[index])
        # Perimeter = cv2.arcLength(contours[index], True)
        # Area = cv2.contourArea(cnt)
        # if Area > 500:

        if len(approx) < 7:
            cv2.drawContours(oimg, cnt, -1, ([255, 0, 0]), 2)
            print('', end='')
            cx = int(cen['m10'] / cen['m00'])
            cy = int(cen['m01'] / cen['m00'])

            x = (cx * 5) // b[0][1]
            y = (cy * 5) // b[0][0]
            a[y][x] = 5
        else:
            cv2.drawContours(oimg, cnt, -1, ([0, 255, 0]), 3)
            cx = int(cen['m10'] / cen['m00'])
            cy = int(cen['m01'] / cen['m00'])
            x = (cx * 5) // b[0][1]
            y = (cy * 5) // b[0][0]
            a[y][x] = 6

    imshow()
    # SELECT WHITE COLOR
    r = cv2.selectROI('ROI', oimg)
    imcrop = oimg[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

    thresh = 50
    bmin = max(0, imcrop[:, :, 0].min() - thresh)
    gmin = max(0, imcrop[:, :, 1].min() - thresh)
    rmin = max(0, imcrop[:, :, 2].min() - thresh)

    bmax = min(255, imcrop[:, :, 0].max() + thresh)
    gmax = min(255, imcrop[:, :, 1].max() + thresh)
    rmax = min(255, imcrop[:, :, 2].max() + thresh)
    rlower = np.array([bmin, gmin, rmin])
    rupper = np.array([bmax, gmax, rmax])
    threshold = cv2.inRange(oimg, rlower, rupper)
    kernel = np.ones((3, 3), np.uint8)
    threshold = cv2.erode(threshold, kernel, iterations=2)
    threshold = cv2.dilate(threshold, kernel, iterations=1)
    contours, hirarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)

        cen = cv2.moments(cnt)
        # Area = cv2.contourArea(contours[index])
        # Perimeter = cv2.arcLength(contours[index], True)
        # Area = cv2.contourArea(cnt)
        # if Area > 500:

        if len(approx) < 7:
            cv2.drawContours(oimg, cnt, -1, ([255, 0, 0]), 2)
            print('', end='')
            cx = int(cen['m10'] / cen['m00'])
            cy = int(cen['m01'] / cen['m00'])

            x = (cx * 5) // b[0][1]
            y = (cy * 5) // b[0][0]
            a[y][x] = 7
        else:
            cv2.drawContours(oimg, cnt, -1, ([0, 255, 0]), 3)
            cx = int(cen['m10'] / cen['m00'])
            cy = int(cen['m01'] / cen['m00'])
            x = (cx * 5) // b[0][1]
            y = (cy * 5) // b[0][0]
            a[y][x] = 8

    imshow()
    # FOR GREEN COLOR
    r = cv2.selectROI('ROI', oimg)
    imcrop = oimg[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

    thresh = 35
    bmin = max(0, imcrop[:, :, 0].min() - thresh)
    gmin = max(0, imcrop[:, :, 1].min() - thresh)
    rmin = max(0, imcrop[:, :, 2].min() - thresh)

    bmax = min(255, imcrop[:, :, 0].max() + thresh)
    gmax = min(255, imcrop[:, :, 1].max() + thresh)
    rmax = min(255, imcrop[:, :, 2].max() + thresh)
    rlower = np.array([bmin, gmin, rmin])
    rupper = np.array([bmax, gmax, rmax])
    threshold = cv2.inRange(oimg, rlower, rupper)
    kernel = np.ones((3, 3), np.uint8)
    threshold = cv2.erode(threshold, kernel, iterations=3)
    threshold = cv2.dilate(threshold, kernel, iterations=3)
    contours, hirarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.imshow('htresh', threshold)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

        cen = cv2.moments(cnt)
        # Area = cv2.contourArea(contours[index])
        # Perimeter = cv2.arcLength(contours[index], True)
        # Area = cv2.contourArea(cnt)
        # if Area > 100:

        if len(approx) < 7:
            cv2.drawContours(oimg, cnt, -1, ([255, 0, 0]), 2)
            print('', end='')
            cx = int(cen['m10'] / cen['m00'])
            cy = int(cen['m01'] / cen['m00'])

            x = (cx * 5) // b[0][1]
            y = (cy * 5) // b[0][0]
            i = 9
            if (i - a[y][x]) == 8:
                a[y][x] = 11
            if i - a[y][x] == 6:
                a[y][x] = 12
            if i - a[y][x] == 4:
                a[y][x] = 13
            if i - a[y][x] == 2:
                a[y][x] = 14


        else:
            cv2.drawContours(oimg, cnt, -1, ([0, 255, 0]), 3)
            cx = int(cen['m10'] / cen['m00'])
            cy = int(cen['m01'] / cen['m00'])
            x = (cx * 5) // b[0][1]
            y = (cy * 5) // b[0][0]
            i = 50
            if (i - a[y][x]) == 48:
                a[y][x] = 15
            if i - a[y][x] == 46:
                a[y][x] = 16
            if i - a[y][x] == 44:
                a[y][x] = 17
            if i - a[y][x] == 42:
                a[y][x] = 18
    imshow()

    # cv2.imshow('img', oimg)
    # cv2.imshow('im', threshold)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    print(a)
    return a
# oimg=cv2.imread('img2.jpeg')
# print(getMatrix(oimg))





