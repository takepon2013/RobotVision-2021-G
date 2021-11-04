# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 14:01:55 2021

@author: E
"""

import pygame

def s(screen: pygame.Surface, first_color: (int, int, int), second_color: (int, int, int), first_total: int, second_total: int):
  
    first_surface = font.render("Score :" + str(first_total), True, (50, 50, 255))
    second_surface = font.render("Score :" + str(second_total), True, (255, 50, 50))
    countdown_surface = font.render(str((count // 60)), True, (200, 150, 0))
    
    pygame.draw.circle(screen, first_color, (300, 240), 60)
    

    screen.blit(scoreboard, (0, 480))
    screen.blit(first_surface, (50, 505))
    screen.blit(second_surface, (980, 505))
    screen.blit(countdown_surface, (600, 505))

    print(first_total, second_total)

    pygame.display.update()

def show_wait_screen(screen: pygame.Surface, color_game.color_lower_1, color_game.color_upper_1, color_game.color_lower_2, color_game.color_upper_2):
    font = pygame.font.Font(None, 70)
    pygame.display.set_caption('ボーナスゲーム')
    background = pygame.image.load('./assets/bg.png')
    background = pygame.transform.scale(background, (1200, 480))
    
    clock = pygame.time.Clock()
    
    screen.blit(background, (0, 0))
    
    text = font.render("Tap S key to start bonus game", True, (200, 150, 0))
    screen.blit(text, (100, 400))
        
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
        
      
        
    


    
if __name__ == '__main__':
    pygame.init()
    display = pygame.display.set_mode((1280, 580))
    show_start_screen(display)
    
