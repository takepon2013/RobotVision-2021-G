import pygame
from bullet import Bullet
from beam import Beam
from typing import Dict


class Player(pygame.sprite.Sprite):
    # 0 ... gu, 1 ... tyoki, 2 ... pa
    command: int = 1
    fromRight: bool
    background: pygame.Surface
    bullets: Dict[int, Bullet]

    # プレイヤーのスコア
    score: int = 0
    #プレイヤーの必殺ゲージ
    gauge: int = 0
    #パーのため時間を計測するためのリスト
    par_tame = []
    #パーのレーザーを連続で食らわないようにクールタイムを設定するけどその変数
    par_cooldown: int = 0
    playerpos: int = 240
    rchosei : int = 0
    
    def __init__(self, background: pygame.Surface, fromRight: bool):
        pygame.sprite.Sprite.__init__(self)
        
        self.par_tame = []
        self.bullets = {}
        self.background = background
        if(fromRight == False):
            self.image = pygame.image.load('./assets/pl1choki.png')
        else:
            self.image = pygame.image.load('./assets/pl2choki.png')
        center_y_for_ball = (background.get_height() -
                             self.image.get_height()) // 2
        center_x_for_ball = (background.get_width() -
                             self.image.get_width()) if fromRight else 0
        self.rect = pygame.Rect(center_x_for_ball, center_y_for_ball,
                                self.image.get_width() - 10, self.image.get_height() - 20)
        self.fromRight = fromRight
        
        if self.fromRight == True:
            self.rchosei = -1201
        else:
            self.rchosei = 60

    def update(self, yolopos: int):

        if self.fromRight == False:
            xzahyou = 0
        else:
            xzahyou = 1201

        self.rect = pygame.Rect(xzahyou, yolopos,
                                self.image.get_width() - 10, self.image.get_height() - 20)
        # 画面からはみ出ないようにする
        self.playerpos = yolopos
        

        if (self.command == 0):
            if(self.fromRight == False):
                self.image = pygame.image.load('./assets/pl1goo.png')
            else:
                self.image = pygame.image.load('./assets/pl2goo.png')
        if (self.command == 1):
            if(self.fromRight == False):
                self.image = pygame.image.load('./assets/pl1choki.png')
            else:
                self.image = pygame.image.load('./assets/pl2choki.png')
        if (self.command == 2):
            if(self.fromRight == False):
                if(self.gauge >= 100):
                    self.image = pygame.image.load('./assets/pl1par.png')
                else:
                    self.image = pygame.image.load('./assets/pl1choki.png')
            else:
                if(self.gauge >= 100):
                    self.image = pygame.image.load('./assets/pl2par.png')
                else:
                    self.image = pygame.image.load('./assets/pl2choki.png')

            #パーならビーム発射準備をためる
            if self.gauge >= 100:
                self.par_tame.append(1)
                
                
            else:
                self.par_tame.append(0)
                
                
        else:
            self.par_tame.append(0)
            
            
        
        #一定期間,180フレーム分のデータを蓄積
        if len(self.par_tame) > 150 :
            del self.par_tame[0]
        
            
            
            
            
    # シュートする
    def generate_bullet(self) -> Bullet:
        # コマンドがtyokiの場合のみ行う
        if self.command != 1:
            print("contradictory to own command")
            return None
        bullet = Bullet(self.fromRight, self.rect.y + 15, self.rect.x)
        self.bullets[self.rect.y] = bullet
        return bullet
    # ビームがどかん！
    def generate_beam\
                    (self) -> Beam:
        # コマンドがparの場合のみ行う
        if (self.command == 2) and (sum(self.par_tame) >= 130) and (self.par_tame[0] == 1) and (self.gauge >= 100):
            
            beam = Beam(self.fromRight, self.rect.y -60, self.rect.x + self.rchosei)
            self.gauge = 0
            
            return beam
        else:
            return None

    def remove_bullet(self, yPosition: int):
        bullet = self.bullets.get(yPosition)
        if bullet is None:
            return
        bullet.kill()
