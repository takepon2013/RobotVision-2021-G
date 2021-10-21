#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 15:55:35 2021

@author: fumiyatanaka
"""

import pygame
import cv2

pygame.init()

cap = cv2.VideoCapture(1)

cap_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cap_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


screen = pygame.display.set_mode((cap_width, cap_height))
ball = cv2.imread('./')
finish = False




while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
            
    

pygame.display.flip()