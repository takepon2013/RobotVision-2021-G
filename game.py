#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 15:55:35 2021

@author: fumiyatanaka
"""
import sys

import pygame
import player
from yolo_take import detect
import threading
import cv2

# gameの初期化
pygame.init()

# キャプチャの撮影
# cap = cv2.VideoCapture(0)

game_width = 1280
game_height = 480

game_center_y = 240

# スクリーンとバックグランドの設定
screen = pygame.display.set_mode((int(game_width), int(game_height)))
background = pygame.image.load('./assets/bg.png')
background = pygame.transform.scale(
    background, (int(game_width), int(game_height)))
screen.blit(background, (0, 0))
print((int(game_width), int(game_height)))
finish = False

# プレイヤーと弾丸の設定
player_group = pygame.sprite.Group()
first_bullet_group = pygame.sprite.Group()
second_bullet_group = pygame.sprite.Group()

first_player = player.Player(background, False)
second_player = player.Player(background, True)

player_group.add(first_player)
player_group.add(second_player)

player_group.update(240)
yolozahyou = 240

count = 0

Clockclock = pygame.time.Clock()

# yolov5 detectをスレッドで起動
detecting = threading.Thread(
    target=detect.run,
    kwargs={
        'source': 1,
        'weights': 'yolo_take/runs/train/Deeplearning-result3/weights/best.pt',
        'imgsz': 240
    }
)
detecting.start()

while not finish:

    player_group.clear(screen, background)
    first_bullet_group.clear(screen, background)
    second_bullet_group.clear(screen, background)

    # 毎フレーム弾丸を出すと重いので一定間隔で間引きしたい
    if count % 30 == 0:
        if first_player.command == 1:
            new_bullet = first_player.generate_bullet()
            first_bullet_group.add(new_bullet)
        if second_player.command == 1:
            new_bullet = second_player.generate_bullet()
            second_bullet_group.add(new_bullet)

    # 手の形の判断

    detecttxt1 = open('out.txt', 'r')
    firstplayerhand = detecttxt1.read()
    detecttxt1.close()

    if firstplayerhand == 'goo':
        first_player.command = 0
    elif firstplayerhand == 'choki':
        first_player.command = 1
    elif firstplayerhand == 'par':
        first_player.command = 2

    # ユーザー入力
    for event in pygame.event.get():
        # print('event')
        if event.type == pygame.QUIT:
            finish = True


# テキストデータから　座標受け取って移動　First player
    detecttxt2 = open('zahyou.txt', 'r')
    # プレイヤーのy座標の比率（0~1）
    height_ratio = detecttxt2.read()
    detecttxt2.close()

    if height_ratio == '':
        yolozayhou = yolozahyou
    else:
        # 感度をあげている
        height_ratio = float(height_ratio)
        yolozahyou = int(game_height * height_ratio * 1.7)

        if yolozahyou < 0:
            yolozahyou = 0
        if yolozahyou > 480:
            yolozahyou = 480

    first_player.update(yolozahyou)

    # 衝突判定

    first_bullet_group.update()
    second_bullet_group.update()

    first_bullet_group.draw(screen)
    second_bullet_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()

    count += 1

    Clockclock.tick(60)

cv2.destroyAllWindows()
pygame.quit()
sys.exit()
