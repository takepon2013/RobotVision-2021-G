import copy
import random
from typing import Callable

import cv2
import numpy as np
import pygame

import start_screen
from yolo_take.utils.datasets import LoadStreams


def hsv_to_bgr(h, s, v):
    bgr = cv2.cvtColor(np.array([[[h, s, v]]], dtype=np.uint8), cv2.COLOR_HSV2BGR)[0][0]
    return int(bgr[0]), int(bgr[1]), int(bgr[2])


def bgr_to_hsv(b, g, r):
    hsv = cv2.cvtColor(np.array([[[b, g, r]]], dtype=np.uint8), cv2.COLOR_BGR2HSV)[0][0]
    return int(hsv[0]), int(hsv[1]), int(hsv[2])


class ColorGame:
    first_cleared = False
    second_cleared = False
    can_show_color: bool = False
    duration = 60 * 30  # 10秒固定
    count = 60 * 30  # 10秒。0になったら終わり
    first_score: int = 0
    second_score: int = 0
    first_time = 0
    second_time = 0

    finish = False
    streams: LoadStreams
    width1: int
    height1: int

    width2: int
    height2: int

    # HSV形式
    color_lower_1: np.ndarray
    color_upper_1: np.ndarray

    # HSV形式
    color_lower_2: np.ndarray
    color_upper_2: np.ndarray

    def __init__(self):
        self.streams = LoadStreams(sources=['0', '1'], img_size=256)
        self.width1 = self.streams.imgs[0].shape[1]
        self.height1 = self.streams.imgs[0].shape[0]
        self.width2 = self.streams.imgs[1].shape[1]
        self.height2 = self.streams.imgs[1].shape[0]
        
        lower_random_hue_1, upper_random_hue_1 = self.generate_hue_color()
        self.color_upper_1 = np.array(upper_random_hue_1)
        self.color_lower_1 = np.array(lower_random_hue_1)

        lower_random_hue_2, upper_random_hue_2 = self.generate_hue_color()
        self.color_upper_2 = np.array(upper_random_hue_2)
        self.color_lower_2 = np.array(lower_random_hue_2)

    def prepare(self, screen: pygame.Surface,):
        for _, _, imgs, _ in self.streams:
            if self.can_show_color:
                break
            cv2.imshow('Player1', imgs[0])
            cv2.imshow('Player2', imgs[1])
            start_screen.show_setup_camera_screen(screen)
            key = cv2.waitKey(1)
            if key == ord('s'):
                self.can_show_color = True

    def start(
            self,
            on_update: Callable[[int, int, int], None]
    ):
        # 繰り返しの読み込み
        clock = pygame.time.Clock()
        for _, _, imgs, _ in self.streams:
            clock.tick(60)
            self.count -= 1
            self.first_time += 1
            self.second_time += 1
            if self.count < 0:
                self.finish = True
                return

            img = imgs[0]
            width = self.width1
            height = self.height1
            mean_color_1 = (self.color_upper_1[0] + self.color_lower_1[0]) // 2, self.color_upper_1[1], self.color_upper_1[2]
            self.draw_and_calculate(
                'Player1',
                img,
                self.color_upper_1,
                self.color_lower_1,
                int(width),
                int(height),
                mean_color_1,
                True
            )
            img = imgs[1]
            width = self.width2
            height = self.height2
            mean_color_2 = (self.color_upper_2[0] + self.color_lower_2[0]) // 2, self.color_upper_2[1], self.color_upper_2[2]
            self.draw_and_calculate(
                'Player2',
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
        detect_x, detect_y, detect_w, detect_h, area = self.calculate_score(mask)

        # 描画用のフレーム
        copied_frame = copy.deepcopy(frame)

        center_x = width // 2
        center_y = height // 2

        cleared = self.first_cleared if is_first else self.second_cleared

        if cleared:
            cv2.putText(
                copied_frame,
                'CLEAR!!',
                (center_x, center_y),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                bgr,
                thickness=3
            )
        else:
            # 20 %以上の領域で色を検出できたら
            if area > 20:
                score = (self.duration - self.first_time) // 60 if is_first else (
                                                                                             self.duration - self.second_time) // 60
                if is_first and score > self.first_score:
                    self.first_score = score
                    cleared = True
                elif not is_first and score > self.second_score:
                    self.second_score = score
                    cleared = True
            else:
                cv2.putText(
                    copied_frame,
                    'Too small or not detected',
                    (center_x - 300, center_y + 160),
                    cv2.FONT_HERSHEY_PLAIN,
                    3,
                    bgr,
                    thickness=3
                )
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

        if is_first:
            self.first_cleared = cleared
        else:
            self.second_cleared = cleared

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
        area = width * height
        total_area = bin_img.shape[0] * bin_img.shape[1]
        area_score = area / total_area * 100
        print(f'Score {area_score}, area {area}')
        return x, y, width, height, area_score

    def release(self):
        cv2.destroyWindow('mask1')
        cv2.destroyWindow('mask2')

    # (H, S, V)
    def generate_hue_color(self) -> ((int, int, int), (int, int, int)):
        rand_num = random.randint(0, 17)
        hue = 10 * rand_num
        return (hue, 60, 150), (hue + 10, 255, 255)

    def convert_ndarray_pygame_image(self, array: np.ndarray, width: int, height: int) -> pygame.Surface:
        opencv_image = array[:, :, ::-1]  # OpenCVはBGR、pygameはRGBなので変換してやる必要がある。
        opencv_image = opencv_image[:height, width//3:width+width//3, :]
        shape = opencv_image.shape[1::-1]  # OpenCVは(高さ, 幅, 色数)、pygameは(幅, 高さ)なのでこれも変換。
        pygame_image = pygame.image.frombuffer(opencv_image.tostring(), shape, 'RGB')
        return pygame_image
