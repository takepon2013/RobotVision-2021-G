#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 12:29:11 2021

@author: fumiyatanaka
"""

import cv2
import numpy as np
import copy

class Bullet:
    frame = None
    position = (0, 0)
    fromLeft = None
    length = None

    def __init__(self, player, y, fromLeft, length):
        self.fromLeft = fromLeft
        if self.fromLeft:
            self.position = (0, y)
        else:
            self.position == (-1, y)
        self.frame = player
        self.length = length

    def moveHorizontal(self, field, x) -> np.ndarray:
        position = self.position
        if self.fromLeft:
            self.position = (position[0] + x, position[1])
        else:
            self.position = (position[0] - x, position[1])
            
        length = self.length
        position = self.position
        copy_frame = copy.deepcopy(field)
        
        copy_frame[
            position[0]:position[0] + length, 
            position[1]:position[1] + length
        ] = self.frame
        
        return copy_frame
        
    def moveVertical(self, field, y, isUp) -> np.ndarray:
        print(self.frame)
        position = self.position
        if isUp:
            self.position = (position[0], position[1] - y)
        else:
            self.position = (position[0], position[1] + y)
            
        length = self.length
        position = self.position
        copy_frame = copy.deepcopy(field)
        
        copy_frame[
            position[0]:position[0] + length, 
            position[1]:position[1] + length
        ] = self.frame
        
        return copy_frame

player_image_path = "./assets/player.png"

cap = cv2.VideoCapture(1)

cap_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cap_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

player_length = 48
first_player_frame = cv2.imread(player_image_path)
first_player_frame = cv2.resize(first_player_frame, (player_length, player_length))
second_player_frame = cv2.imread(player_image_path)
second_player_frame = cv2.resize(second_player_frame, (player_length, player_length))


first_player = 0, 0
second_player = cap_width - player_length, cap_height - player_length

size = int(cap_width), int(cap_height), 3
black_image = np.zeros(size, dtype=np.uint8)
black_image = cv2.rectangle(
    black_image, 
    (0, 0), 
    (size[0], size[1]), 
    (255, 255, 255), 
    thickness=-1
)

first_player_bullet = Bullet(first_player_frame, 200, True, player_length)
second_player_bullet = Bullet(second_player_frame, 200, False, player_length)


while True:
    key = cv2.waitKey(1)
    diff = 10
    
    bg = first_player_bullet.moveHorizontal(black_image, 10)
    
    cv2.imshow('Board', bg)
    
    if key == ord('q'):
        break
    elif key == ord('s'):
        first_player_bullet.moveVertical(black_image, diff, False)
    elif key == ord('w'):
        first_player_bullet.moveVertical(black_image, diff, True)
    
cap.release()
cv2.destroyAllWindows()
