#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 15:55:35 2021

@author: fumiyatanaka
"""
import sys

import pygame
import cv2
import player

# gameの初期化
pygame.init()

# キャプチャの撮影
cap = cv2.VideoCapture(1)

# キャプチャの情報
cap_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cap_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# スクリーンとバックグランドの設定
screen = pygame.display.set_mode((int(cap_width), int(cap_height)))
background = pygame.image.load('./assets/bg.png')
background = pygame.transform.scale(background, (int(cap_width), int(cap_height)))
screen.blit(background, (0, 0))
print((int(cap_width), int(cap_height)))
finish = False

# プレイヤーと弾丸の設定
player_group = pygame.sprite.Group()
first_bullet_group = pygame.sprite.Group()
second_bullet_group = pygame.sprite.Group()

first_player = player.Player(background, False)
second_player = player.Player(background, True)

player_group.add(first_player)
player_group.add(second_player)

player_group.update('')

count = 0

while not finish:

    player_group.clear(screen, background)
    first_bullet_group.clear(screen, background)
    second_bullet_group.clear(screen, background)

    # 毎フレーム弾丸を出すと重いので一定間隔で間引きしたい
    if count % 100 == 0:
        if first_player.command == 1:
            new_bullet = first_player.generate_bullet()
            first_bullet_group.add(new_bullet)
        if second_player.command == 1:
            new_bullet = second_player.generate_bullet()
            second_bullet_group.add(new_bullet)

    # ユーザー入力
    for event in pygame.event.get():
        print('event')
        if event.type == pygame.QUIT:
            finish = True
        elif event.type == pygame.KEYDOWN:
            player_group.update(event.key)

    # 衝突判定


    first_bullet_group.update()
    second_bullet_group.update()

    first_bullet_group.draw(screen)
    second_bullet_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()

    count += 1

pygame.quit()
sys.exit()