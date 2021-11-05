#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 15:55:35 2021

@author: fumiyatanaka
"""
import sys
import time

import numpy as np
import pygame
import player
import color_game
from gauge import Gauge
from yolo_take import detect
import cv2
from events import first_display_event_type, second_display_event_type
import start_screen
import multiprocessing


def main():
    # gameの初期化
    pygame.init()

    # キャプチャの撮影
    # cap = cv2.VideoCapture(0)

    game_width = 1280
    game_height = 580

    game_center_y = 240

    choki_damage = 5
    par_damage = 30

    first_par_count = 0
    second_par_count = 0

    # スクリーンとバックグランドの設定
    screen = pygame.display.set_mode((int(game_width), int(game_height)))
    background = pygame.image.load('./assets/bg.png')
    background = pygame.transform.scale(
        background, (int(game_width), int(game_height) - 100))

    scoreboard = pygame.image.load('./assets/scoreboard.png')
    scoreboard = pygame.transform.scale(
        scoreboard, (int(game_width), 100))

    print((int(game_width), int(game_height)))
    finish = False

    # ゲージの描画

    p1_gauge = Gauge(False)
    p2_gauge = Gauge(True)

    # フォントの設定

    font = pygame.font.Font(None, 70)

    # テキストファイルの初期化
    texs = open('out.txt', 'w')
    texs.write('goo')
    texs.close()
    tex = open('out1.txt', 'w')
    tex.write('goo')
    tex.close()

    texs = open('zahyou.txt', 'w')
    texs.write('0.5')
    texs.close()
    texs = open('zahyou1.txt', 'w')
    texs.write('0.5')
    texs.close()

    # プレイヤーと弾丸の設定
    player_group = pygame.sprite.Group()
    gauge_group = pygame.sprite.Group()
    first_bullet_group = pygame.sprite.Group()
    second_bullet_group = pygame.sprite.Group()

    first_beam_group = pygame.sprite.Group()
    second_beam_group = pygame.sprite.Group()

    first_player = player.Player(background, False)
    second_player = player.Player(background, True)

    player_group.add(first_player)
    player_group.add(second_player)

    gauge_group.add(p1_gauge)
    gauge_group.add(p2_gauge)

    player_group.update(240)
    yolozahyou = 240
    yolozahyou2 = 240

    count = 0

    Clockclock = pygame.time.Clock()

    manager = multiprocessing.Manager()
    returned_dict = manager.dict()

    # yolov5 detectをスレッドで起動
    first_detector = detect.Detector()
    first_detecting = multiprocessing.Process(
        target=first_detector.run,
        kwargs={
            'source': 0,
            'weights': 'yolo_take/runs/train/Deeplearning-result3/weights/best.pt',
            'imgsz': 256,
            'returned_dict': returned_dict,
            'dict_index': 0
        }
    )
    first_detecting.start()

    # カメラの起動を待機する
    time.sleep(1)

    # yolov5 detectをスレッドで起動
    second_detector = detect.Detector()
    second_detecting = multiprocessing.Process(
        target=second_detector.run,
        kwargs={
            'source': 1,
            'weights': 'yolo_take/runs/train/Deeplearning-result3/weights/best.pt',
            'imgsz': 256,
            'Player1': False,
            'returned_dict': returned_dict,
            'dict_index': 1
        }
    )
    second_detecting.start()

    start_screen.show_start_screen(screen)

    screen.blit(background, (0, 0))
    screen.blit(scoreboard, (0, 480))

    while not finish:

        player_group.clear(screen, background)
        first_bullet_group.clear(screen, background)
        second_bullet_group.clear(screen, background)
        first_beam_group.clear(screen, background)
        second_beam_group.clear(screen, background)

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

        detect_text2 = open('out1.txt', 'r')
        second_player_command = detect_text2.read()
        detect_text2.close()

        if firstplayerhand == 'goo':
            first_player.command = 0
        elif firstplayerhand == 'choki':
            first_player.command = 1
        elif firstplayerhand == 'par':
            first_player.command = 2

        if second_player_command == 'goo':
            second_player.command = 0
        elif second_player_command == 'choki':
            second_player.command = 1
        elif second_player_command == 'par':
            second_player.command = 2

        # ユーザー入力
        for event in pygame.event.get():
            # print('event')
            if event.type == pygame.QUIT:
                finish = True

        if len(returned_dict) > 1:
            img, w_name = returned_dict[0]
            cv2.imshow(w_name, img)
            cv2.waitKey(1)
            img, w_name = returned_dict[1]
            cv2.imshow(w_name, img)
            cv2.waitKey(1)

            # テキストデータから　座標受け取って移動　First player
        detecttxt2 = open('zahyou.txt', 'r')
        # プレイヤーのy座標の比率（0~1）
        height_ratio = detecttxt2.read()
        detecttxt2.close()

        if height_ratio == '':
            yolozahyou = yolozahyou
        else:
            # 感度をあげている
            height_ratio2 = float(height_ratio)
            height_ratio2 = height_ratio2 - 0.5

            # 感度を上げる具体的な数値height_ratio * n　でn倍の感度になる
            height_ratio2 = height_ratio2 * 3.0

            yolozahyou = int(((game_height - 180) / 2 / 0.5) * height_ratio2 + ((game_height - 180) / 2))

            if yolozahyou < 0:
                yolozahyou = 0
            if yolozahyou > 400:
                yolozahyou = 400

        # テキストデータから　座標受け取って移動　Second player
        detecttxt2 = open('zahyou1.txt', 'r')
        # プレイヤーのy座標の比率（0~1）
        height_ratio = detecttxt2.read()
        detecttxt2.close()

        if height_ratio == '':
            yolozahyou2 = yolozahyou2
        else:
            # 感度をあげている
            height_ratio2 = float(height_ratio)
            height_ratio2 = height_ratio2 - 0.5

            # 感度を上げる具体的な数値height_ratio * n　でn倍の感度になる
            height_ratio2 = height_ratio2 * 3.0

            yolozahyou2 = int(((game_height - 180) / 2 / 0.5) * height_ratio2 + ((game_height - 180) / 2))

            if yolozahyou2 < 0:
                yolozahyou2 = 0
            if yolozahyou2 > 400:
                yolozahyou2 = 400

        # 必殺ゲージに関する処理
        if count % 20 == 0:
            first_player.gauge += 1
            second_player.gauge += 1

        if first_player.gauge > 100:
            first_player.gauge = 100
        if second_player.gauge > 100:
            second_player.gauge = 100

        if first_player.command == 2:
            new_beam = first_player.generate_beam()
            if new_beam != None:
                first_beam_group.add(new_beam)
                first_par_count = 0
        if second_player.command == 2:
            new_beam = second_player.generate_beam()
            if new_beam != None:
                second_beam_group.add(new_beam)
                second_par_count = 0

        # スコアボードに記載

        first_player_score = font.render("Score :" + str(first_player.score), True, (50, 50, 255))
        second_player_score = font.render("Score :" + str(second_player.score), True, (255, 50, 50))
        countdown = font.render(str(int(120 - (count / 60))), True, (200, 150, 0))

        screen.blit(scoreboard, (0, 480))
        screen.blit(first_player_score, (50, 505))
        screen.blit(second_player_score, (1010, 505))
        screen.blit(countdown, (600, 505))

        # 衝突判定
        first_colid = pygame.sprite.spritecollide(first_player, second_bullet_group, True)

        if first_colid != []:
            if first_player.command == 0:
                second_player.gauge += 5

            if first_player.command == 1:
                second_player.score += choki_damage
                second_player.gauge += 3

            if first_player.command == 2:

                if first_player.gauge >= 100:
                    second_player.score += choki_damage * 3
                    first_player.gauge = 0
                else:
                    second_player.score += choki_damage

        second_colid = pygame.sprite.spritecollide(second_player, first_bullet_group, True)

        if second_colid != []:
            if second_player.command == 0:
                first_player.gauge += 5

            if second_player.command == 1:
                first_player.score += choki_damage
                first_player.gauge += 3

            if second_player.command == 2:

                if second_player.gauge >= 100:
                    first_player.score += choki_damage * 3
                    second_player.gauge = 0
                else:
                    first_player.score += choki_damage

        first_par_colid = pygame.sprite.spritecollide(first_player, second_beam_group, False)
        second_par_colid = pygame.sprite.spritecollide(second_player, first_beam_group, False)

        if first_par_colid != []:
            if second_player.par_cooldown > 240:
                second_player.score += par_damage
                second_player.par_cooldown = 0

        if second_par_colid != []:
            if first_player.par_cooldown > 240:
                first_player.score += par_damage
                first_player.par_cooldown = 0

        # プレイヤー全体のアップデート　大事！
        first_player.update(yolozahyou)
        second_player.update(yolozahyou2)

        first_bullet_group.update()
        second_bullet_group.update()

        if first_par_count > 180:
            first_beam_group.update(True)
        else:
            first_beam_group.update(False)

        if second_par_count > 180:
            second_beam_group.update(True)

        else:
            second_beam_group.update(False)

        p1_gauge.update(first_player.gauge)
        p2_gauge.update(second_player.gauge)

        gauge_group.draw(screen)

        first_bullet_group.draw(screen)
        second_bullet_group.draw(screen)

        first_beam_group.draw(screen)
        second_beam_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()

        count += 1
        first_par_count += 1
        second_par_count += 1
        # クールダウンタイムの経過
        first_player.par_cooldown += 1
        second_player.par_cooldown += 1

        Clockclock.tick(60)

        if count > 360:
            finish = True

    # 画面を真っ暗にする
    screen.fill((0, 0, 0))

    pygame.display.flip()

    pygame.display.set_caption('ボーナスゲーム！')

    # ボーナスゲーム
    bonus_game = color_game.ColorGame()

    start_screen.show_wait_screen(screen)

    # 画面を真っ暗にする
    screen.fill((0, 0, 0))

    def on_update_color_game(
            bonus_first_score: int,
            bonus_second_score: int,
            count: int
    ):
        first_total = int(bonus_first_score + first_player.score)
        second_total = int(bonus_second_score + second_player.score)

        # H S V
        first_color = [
            bonus_game.color_upper_1[0] + bonus_game.color_lower_1[0] // 2,
            bonus_game.color_upper_1[1],
            bonus_game.color_upper_1[2]
        ]
        # R G Bに変換
        first_color = cv2.cvtColor(np.array([[first_color]], dtype=np.uint8), cv2.COLOR_HSV2BGR)[0][0]
        first_color = (first_color[2], first_color[1], first_color[0])

        # H S V
        second_color = [
            bonus_game.color_upper_2[0] + bonus_game.color_lower_2[0] // 2,
            bonus_game.color_upper_2[1],
            bonus_game.color_upper_2[2]
        ]
        # R G Bに変換
        second_color = cv2.cvtColor(np.array([[second_color]], dtype=np.uint8), cv2.COLOR_HSV2BGR)[0][0]
        second_color = (second_color[2], second_color[1], second_color[0])

        start_screen.show_bonus_window(
            screen,
            scoreboard,
            font,
            first_color,
            second_color,
            first_total,
            second_total,
            count
        )

    bonus_game.start(screen, on_update_color_game)

    pygame.display.quit()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
