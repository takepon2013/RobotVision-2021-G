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

game_screen = game_screen.GameScreen(first_cap)
first_hantei = hantei_controller.HanteiController(1)
second_hantei = hantei_controller.HanteiController(1)

count = 0

while True:
    count += 1
    if count % 1000 != 0:
        continue
    first_frame = first_cap.read()[1]
    second_frame = second_cap.read()[1]
    first_action_name = first_hantei.command
    second_action_name = second_hantei.command
    first_command = -1
    if first_action_name == 'rock':
        first_command = 0
    elif first_action_name == 'scissors':
        first_command = 1
    elif first_action_name == 'paper':
        first_command = 2

    second_command = -1

    if second_action_name == 'rock':
        second_command = 0
    elif second_action_name == 'scissors':
        second_command = 1
    elif second_action_name == 'paper':
        second_command = 2

    finish = game_screen.updateFrame(first_command, second_command)
    if finish:
        break

first_cap.release()
second_cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
