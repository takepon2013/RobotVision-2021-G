import pygame
from bullet import Bullet
from typing import Dict

class Player(pygame.sprite.Sprite):
    # 0 ... gu, 1 ... tyoki, 2 ... pa
    command: int = 1
    fromRight: bool
    background: pygame.Surface
    bullets: Dict[int, Bullet]

    # プレイヤーのスコア
    score: int = 0
    playerpos: int = 240
    

    def __init__(self, background: pygame.Surface, fromRight: bool):
        pygame.sprite.Sprite.__init__(self)
        self.bullets = {}
        self.background = background
        if(fromRight == False) :
            self.image = pygame.image.load('./assets/pl1choki.png')
        else :
            self.image = pygame.image.load('./assets/pl2choki.png')
        center_y_for_ball = (background.get_height() - self.image.get_height()) // 2
        center_x_for_ball = (background.get_width() - self.image.get_width()) if fromRight else 0
        self.rect = pygame.Rect(center_x_for_ball, center_y_for_ball, self.image.get_width(), self.image.get_height())
        self.fromRight = fromRight

    def update(self, yolopos: int):
        
        
            moving = yolopos - self.playerpos
                
            self.rect.move_ip(0, moving)
                # 画面からはみ出ないようにする
            self.playerpos = yolopos
            self.rect = self.rect.clamp(self.background.get_rect())
            
            if (self.command == 0):
                if(self.fromRight == False) :
                    self.image = pygame.image.load('./assets/pl1goo.png')
                else :
                    self.image = pygame.image.load('./assets/pl2goo.png')
            if (self.command == 1):
                if(self.fromRight == False) :
                    self.image = pygame.image.load('./assets/pl1choki.png')
                else :
                    self.image = pygame.image.load('./assets/pl2choki.png')
            if (self.command == 2):
                if(self.fromRight == False) :
                    self.image = pygame.image.load('./assets/pl1choki.png')
                else :
                    self.image = pygame.image.load('./assets/pl2choki.png')
            
               


    # シュートする
    def generate_bullet(self) -> Bullet:
        # コマンドがtyokiの場合のみ行う
        if self.command != 1:
            print("contradictory to own command")
            return None
        bullet = Bullet(self.fromRight, self.rect.y + 15, self.rect.x)
        self.bullets[self.rect.y] = bullet
        return bullet

    def remove_bullet(self, yPosition: int):
        bullet = self.bullets.get(yPosition)
        if bullet is None:
            return
        bullet.kill()
