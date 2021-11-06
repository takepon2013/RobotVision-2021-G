import copy
import random
from typing import Callable

import cv2
import numpy as np
import pygame

from yolo_take.utils.datasets import LoadStreams


def hsv_to_bgr(h, s, v):
    bgr = cv2.cvtColor(np.array([[[h, s, v]]], dtype=np.uint8), cv2.COLOR_HSV2BGR)[0][0]
    return int(bgr[0]), int(bgr[1]), int(bgr[2])


def bgr_to_hsv(b, g, r):
    hsv = cv2.cvtColor(np.array([[[b, g, r]]], dtype=np.uint8), cv2.COLOR_BGR2HSV)[0][0]
    return int(hsv[0]), int(hsv[1]), int(hsv[2])


class ColorGame:
    count = 60 * 10 # 10秒
    first_score: int = 0
    second_score: int = 0
    first_time = 0
    second_time = 0

    finish = False
    stream1: LoadStreams
    width1: int
    height1: int

    stream2: LoadStreams
    width2: int
    height2: int

    # HSV形式
    color_lower_1: np.ndarray
    color_upper_1: np.ndarray

    # HSV形式
    color_lower_2: np.ndarray
    color_upper_2: np.ndarray

    def __init__(self):
        self.stream1 = LoadStreams(sources='0', img_size=240)
        self.stream2 = LoadStreams(sources='1', img_size=240)
        self.width1 = self.stream1.imgs[0].shape[1]
        self.height1 = self.stream1.imgs[0].shape[0]
        self.width2 = self.stream2.imgs[0].shape[1]
        self.height2 = self.stream2.imgs[0].shape[0]
        
        lower_random_hue_1, upper_random_hue_1 = self.generate_hue_color()
        self.color_upper_1 = np.array(upper_random_hue_1)
        self.color_lower_1 = np.array(lower_random_hue_1)

        lower_random_hue_2, upper_random_hue_2 = self.generate_hue_color()
        self.color_upper_2 = np.array(upper_random_hue_2)
        self.color_lower_2 = np.array(lower_random_hue_2)


    def start(
            self,
            screen: pygame.Surface,
            on_update: Callable[[int, int, int], None]
    ):
        # 繰り返しの読み込み
        for first, second in zip(self.stream1, self.stream2):
            self.count -= 1
            if self.count < 0:
                self.finish = True
                return
            _, _, first_img0, _ = first
            img = first_img0[0]
            width = self.width1
            height = self.height1
            mean_color_1 = (self.color_upper_1[0] + self.color_lower_1[0] // 2, self.color_upper_1[1], self.color_upper_1[2])
            self.draw_and_calculate(
                'Player1',
                screen,
                img,
                self.color_upper_1,
                self.color_lower_1,
                int(width),
                int(height),
                mean_color_1,
                True
            )
            _, _, second_img0, _ = second
            img = second_img0[0]
            width = self.width2
            height = self.height2
            mean_color_2 = (self.color_upper_2[0] + self.color_lower_2[0] // 2, self.color_upper_2[1], self.color_upper_2[2])
            self.draw_and_calculate(
                'Player2',
                screen,
                img,
                self.color_upper_2,
                self.color_lower_2,
                int(width),
                int(height),
                mean_color_2,
                False
            )
            on_update(self.first_score, self.second_score, self.count)

    def draw_and_calculate(
            self,
            window_name: str,
            screen: pygame.Surface,
            frame: np.ndarray,
            upper_hsv: np.ndarray,
            lower_hsv: np.ndarray,
            width: int,
            height: int,
            hsv_color: (int, int, int),
            is_first: bool
    ):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
        # output = cv2.bitwise_and(frame, frame, mask=mask)
        bgr = hsv_to_bgr(hsv_color[0], hsv_color[1], hsv_color[2])

        # スコアの計算
        detect_x, detect_y, detect_w, detect_h, score = self.calculate_score(mask)
        # 10 %以上の領域で色を検出できたら
        if score > 10:
            if is_first and score > self.first_score:
                self.first_score = score
            elif not is_first and score > self.second_score:
                self.second_score = score

        copied_frame = copy.deepcopy(frame)
        center_x = width // 2
        center_y = height // 2
        cv2.circle(copied_frame, (center_x, center_y), 60, bgr, -1)
        cv2.putText(
            copied_frame,
            'Find Same Color!',
            (center_x - 200, center_y - 80),
            cv2.FONT_HERSHEY_PLAIN,
            3,
            bgr,
            thickness=3
        )
        cv2.rectangle(copied_frame, (detect_x, detect_y), (detect_x + detect_w, detect_y + detect_h), bgr, thickness=3)
        cv2.imshow(window_name, copied_frame)

    # 結果の計算を行うメソッド。面積をそのまま結果としている。
    def calculate_score(self, bin_img: np.ndarray) -> (int, int, int, int, int):
        '''


        :param bin_img: マスクに使用したデータ
        :param surface: 検出を示す資格を表示する土台
        :param draw_color: RGB形式
        :return: 面積を返す
        '''
        num_labels, label_image, stats, center = cv2.connectedComponentsWithStats(bin_img)
        # 画面全体の黒を削除
        num_labels = num_labels - 1
        stats = np.delete(stats, 0, 0)

        area = 0
        best_index = -1
        for index in range(num_labels):
            s = stats[index][4]
            if area < s:
                best_index = index
                area = s

        if best_index == -1:
            return 0, 0, 0, 0, 0
        x = stats[best_index][0]
        y = stats[best_index][1]
        width = stats[best_index][2]
        height = stats[best_index][3]
        total_area = bin_img.shape[0] * bin_img.shape[1]
        score = area / total_area * 100
        print(score)
        return x, y, width, height, score

    def release(self):
        cv2.destroyWindow('mask1')
        cv2.destroyWindow('mask2')

    # (H, S, V)
    def generate_hue_color(self) -> ((int, int, int), (int, int, int)):
        rand_num = random.randint(0, 17)
        hue = 10 * rand_num
        return (hue, 60, 100), (hue + 10, 255, 255)

    def convert_ndarray_pygame_image(self, array: np.ndarray, width: int, height: int) -> pygame.Surface:
        opencv_image = array[:, :, ::-1]  # OpenCVはBGR、pygameはRGBなので変換してやる必要がある。
        opencv_image = opencv_image[:height, width//3:width+width//3, :]
        shape = opencv_image.shape[1::-1]  # OpenCVは(高さ, 幅, 色数)、pygameは(幅, 高さ)なのでこれも変換。
        pygame_image = pygame.image.frombuffer(opencv_image.tostring(), shape, 'RGB')
        return pygame_image
