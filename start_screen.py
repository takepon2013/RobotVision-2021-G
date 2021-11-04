# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 14:01:55 2021

@author: E
"""

import pygame



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
    
