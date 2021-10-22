import pygame
from bullet import Bullet
from typing import Dict

class Player(pygame.sprite.Sprite):
    # 0 ... gu, 1 ... tyoki, 2 ... pa
    command: int = 1
    fromRight: bool
    background: pygame.Surface
    bullets: Dict[int, Bullet]

    def __init__(self, background: pygame.Surface, fromRight: bool):
        pygame.sprite.Sprite.__init__(self)
        self.bullets = {}
        self.background = background
        self.image = pygame.image.load('./assets/player.png')
        center_y_for_ball = (background.get_height() - self.image.get_height()) // 2
        self.rect = pygame.Rect(0, center_y_for_ball, self.image.get_width(), self.image.get_height())
        self.fromRight = fromRight

    def update(self, key: str):
        if key == 's':
            print("s is pressed")
            self.rect.move_ip(0, 30)
            # 画面からはみ出ないようにする
            self.rect = self.rect.clamp(self.background.get_rect())
        elif key == 'w':
            print("w is pressed")
            self.rect.move_ip(0, -30)
            # 画面からはみ出ないようにする
            self.rect = self.rect.clamp(self.background.get_rect())

    # シュートする
    def generate_bullet(self) -> Bullet:
        # コマンドがtyokiの場合のみ行う
        if self.command != 1:
            print("contradictory to own command")
            return None
        bullet = Bullet(self.fromRight, self.rect.y)
        self.bullets[self.rect.y] = bullet
        return bullet

    def remove_bullet(self, yPosition: int):
        bullet = self.bullets.get(yPosition)
        if bullet is None:
            return
        bullet.kill()