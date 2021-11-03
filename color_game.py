import random

import cv2
import numpy as np


def hsv_to_bgr(h, s, v):
    bgr = cv2.cvtColor(np.array([[[h, s, v]]], dtype=np.uint8), cv2.COLOR_HSV2BGR)[0][0]
    return int(bgr[0]), int(bgr[1]), int(bgr[2])


def bgr_to_hsv(b, g, r):
    hsv = cv2.cvtColor(np.array([[[b, g, r]]], dtype=np.uint8), cv2.COLOR_BGR2HSV)[0][0]
    return int(hsv[0]), int(hsv[1]), int(hsv[2])


class ColorGame:

    clear1: bool = False
    clear2: bool = False

    cap1: cv2.VideoCapture
    width1: int
    height1: int

    cap2: cv2.VideoCapture
    width2: int
    height2: int

    # HSV形式
    color_lower_1: np.ndarray
    color_upper_1: np.ndarray

    # HSV形式
    color_lower_2: np.ndarray
    color_upper_2: np.ndarray

    def __init__(self):
        self.cap1 = cv2.VideoCapture(1)
        self.cap2 = cv2.VideoCapture(1)
        self.width1 = self.cap1.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height1 = self.cap1.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width2 = self.cap2.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height2 = self.cap2.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # あとで10引かれるので最小値を10にする
        self.color_upper_1 = np.array([random.randint(10, 179), random.randint(10, 255), random.randint(10, 255)])
        self.color_lower_1 = self.color_upper_1 - 10
        # あとで10引かれるので最小値を10にする
        self.color_upper_2 = np.array([random.randint(10, 179), random.randint(10, 255), random.randint(10, 255)])
        self.color_lower_2 = self.color_upper_2 - 10

    def update(self):
        ret, frame1 = self.cap1.read()
        width1 = self.width1
        height1 = self.height1

        ret, frame2 = self.cap2.read()
        width2 = self.width2
        height2 = self.height2

        self.draw_color(
            'mask1',
            frame1,
            int(width1),
            int(height1),
            (self.color_upper_1[0], self.color_upper_1[1], self.color_upper_1[2])
        )

        self.draw_color(
            'mask2',
            frame2,
            int(width2),
            int(height2),
            (self.color_upper_2[0], self.color_upper_2[1], self.color_upper_2[2])
        )

    def draw_color(self, window_name: str, frame: np.ndarray, width: int, height: int, hsv_color: (int, int, int)):
        # mask = cv2.inRange(frame, np.array([0, 0, 0]), self.color_upper_1)
        # bgr = hsv_to_bgr(hsv_color[0], hsv_color[1], hsv_color[2])
        # cv2.circle(mask, (width // 2 - 30, height // 2 - 30), 60, bgr, -1)
        cv2.imshow(window_name, frame)

    def release(self):
        cv2.destroyWindow('mask1')
        cv2.destroyWindow('mask2')
