import sys
import cv2
import numpy as np


def onmouse(event, x, y, flags, param):
    global seed_pt
    if flags & cv2.EVENT_FLAG_LBUTTON:
        seed_pt = x, y


def UpdateTrackbar(dummy=None):
    global lo, hi
    lo = cv2.getTrackbarPos('lo', winname)
    hi = cv2.getTrackbarPos('hi', winname)


def process_image(img):
    h, w = img.shape[:2]
    init_row, end_row = h*11/20, w*15/20
    ret_img = img[init_row:end_row, :, :]
    h, w = ret_img.shape[:2]
    if seed_pt is None:
        return ret_img
    mask = np.zeros((h+2, w+2), np.uint8)
    fixed_range = True
    
    cv2.floodFill(ret_img, mask, seed_pt, (0,0,255), (lo,)*3, (hi,)*3, 4)
    # cv2.circle(ret_img, seed_pt, 2, (0, 0, 255), -1)
    return ret_img


# UI Globals set here.
seed_pt = None
winname = 'floodFill'
lo = 20
hi = 20


def main():
    # Create UI for tweaking floodfill parameters
    cv2.namedWindow(winname)
    cv2.setMouseCallback(winname, onmouse)
    cv2.createTrackbar('lo', winname, 20, 255, UpdateTrackbar)
    cv2.createTrackbar('hi', winname, 20, 255, UpdateTrackbar)

    # Open image sequence.
    vid = cv2.VideoCapture("img%06d.jpg")
    suc, ret = vid.read()

    while suc:
        ret = process_image(ret)
        cv2.imshow(winname, ret)
        cv2.waitKey(1)
        suc, ret = vid.read()


if __name__ == '__main__':
    main()
