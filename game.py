#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 15:55:35 2021

@author: fumiyatanaka
"""
import sys

import pygame
import cv2
import game_screen
import hantei_controller

# gameの初期化
pygame.init()

first_cap = cv2.VideoCapture(1)
second_cap = cv2.VideoCapture(1)

# キャプチャの情報
cap_width = first_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cap_height = first_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

game_screen = game_screen.GameScreen(cap_width, cap_height)
first_hantei = hantei_controller.HanteiController(1)
second_hantei = hantei_controller.HanteiController(1)

count = 0

while True:
    count += 1
    if count % 100 != 0:
        continue
    first_frame = first_cap.read()[1]
    second_frame = second_cap.read()[1]
    first_command = first_hantei.command
    second_command = second_hantei.command

    finish = game_screen.updateFrame(first_command, second_command)
    if finish:
        break

first_cap.release()
second_cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
