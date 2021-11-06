# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 14:01:55 2021

@author: E
"""

import pygame


def show_bonus_window(
        screen: pygame.Surface,
        scoreboard: pygame.Surface,
        font: pygame.font.Font,
        first_color: (int, int, int),
        second_color: (int, int, int),
        first_total: int,
        second_total: int,
        countdown: int
):
    text = font.render('Find Same Color!!', True, (255, 255, 255))
    first_surface = font.render("Score :" + str(first_total), True, (50, 50, 255))
    second_surface = font.render("Score :" + str(second_total), True, (255, 50, 50))
    countdown_surface = font.render(str((countdown // 60)), True, (200, 150, 0))

    pygame.draw.circle(screen, first_color, (300, 240), 60)
    pygame.draw.circle(screen, second_color, (900, 240), 60)

    screen.blit(scoreboard, (0, 480))
    screen.blit(first_surface, (50, 505))
    screen.blit(second_surface, (980, 505))
    screen.blit(countdown_surface, (600, 505))
    screen.blit(text, (1280 // 2 - 100, 100))

    print(first_total, second_total)
    pygame.display.update()


def show_wait_screen(screen: pygame.Surface):
    font = pygame.font.Font(None, 70)
    pygame.display.set_caption('ボーナスゲーム')
    background = pygame.image.load('./assets/bg.png')
    background = pygame.transform.scale(background, (1200, 480))
    
    clock = pygame.time.Clock()
    
    screen.blit(background, (0, 0))
    
    text = font.render("Tap S key to start bonus game", True, (200, 150, 0))
    screen.blit(text, (200, 400))
        
    pygame.display.update()
    
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == ord('q'):
                return
            elif event.key == ord('s'):
                print('S')
                return
        clock.tick(60)


def show_start_screen(screen: pygame.Surface):
    font = pygame.font.Font(None, 70)
    pygame.display.set_caption('スタート画面')
    background = pygame.image.load('./assets/bg.png')
    background = pygame.transform.scale(background, (1200, 480))
    
    clock = pygame.time.Clock()
    
    screen.blit(background, (0, 0))
    
    text = font.render("Tap S key", True, (200, 150, 0))
    screen.blit(text, (500, 400))
        
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == ord('q'):
                return
            elif event.key == ord('s'):
                print('S')
                return
        clock.tick(60)
        

def show_result_screen(screen: pygame.Surface, font: pygame.font.Font, score_font: pygame.font.Font, score1: int, score2: int):
    # 真っ暗にする
    screen.fill((0, 0, 0))

    game_width = 1280
    game_height = 580
    white = (255, 255, 255)
    first_color = (50, 50, 255)
    second_color = (255, 50, 50)
    result_render = font.render('RESULT', True, white)
    first_score_render = score_font.render(str(score1), True, white)
    first_result_render = score_font.render('WIN!!' if score1 > score2 else 'Loose...', True, first_color)
    second_score_render = score_font.render(str(score2), True, white)
    second_result_render = score_font.render('WIN!!' if score2 > score1 else 'Loose...', True, second_color)

    pygame.draw.circle(screen, first_color, (game_width // 4, 300), 80)
    pygame.draw.circle(screen, second_color, (game_width // 4 * 3, 300), 80)

    screen.blit(result_render, (game_width // 2 - 35, 60))
    screen.blit(first_result_render, (game_width // 4, 60))
    screen.blit(second_result_render, (game_width // 4 * 3, 60))

    screen.blit(first_score_render, (game_width // 4 - 45, 300 + 40))
    screen.blit(second_score_render, (game_width // 4 * 3, 300 + 40))

    pygame.display.update()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == ord('q'):
                return
        clock.tick(60)