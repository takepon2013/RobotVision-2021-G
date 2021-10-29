import pygame
from bullet import Bullet
from typing import Dict

class Player(pygame.sprite.Sprite):
    # 0 ... gu, 1 ... tyoki, 2 ... pa
    command: int = -1
    previous_command: int = -1
    fromRight: bool
    background: pygame.Surface
    bullets: Dict[int, Bullet]

    # プレイヤーのスコア
    score: int = 0

    def __init__(self, background: pygame.Surface, fromRight: bool):
        pygame.sprite.Sprite.__init__(self)
        self.bullets = {}
        self.background = background
        self.image = pygame.image.load('./assets/player.png')
        center_y_for_ball = (background.get_height() - self.image.get_height()) // 2
        center_x_for_ball = (background.get_width() - self.image.get_width()) if fromRight else 0
        self.rect = pygame.Rect(center_x_for_ball, center_y_for_ball, self.image.get_width(), self.image.get_height())
        self.fromRight = fromRight

    def update(self, key: str):
        if not self.fromRight:
            if key == ord('s'):
                print("s is pressed")
                self.rect.move_ip(0, 30)
                # 画面からはみ出ないようにする
                self.rect = self.rect.clamp(self.background.get_rect())
            elif key == ord('w'):
                print("w is pressed")
                self.rect.move_ip(0, -30)
                # 画面からはみ出ないようにする
                self.rect = self.rect.clamp(self.background.get_rect())

        else:
            if key == pygame.K_DOWN:
                print("arrow-down is pressed")
                self.rect.move_ip(0, 30)
                # 画面からはみ出ないようにする
                self.rect = self.rect.clamp(self.background.get_rect())
            elif key == pygame.K_UP:
                print("arrow-up is pressed")
                self.rect.move_ip(0, -30)
                # 画面からはみ出ないようにする
                self.rect = self.rect.clamp(self.background.get_rect())

    # シュートする
    def generate_bullet(self) -> Bullet:
        # コマンドがtyokiの場合のみ行う
        if self.command != 1:
            print("contradictory to own command")
            return None
        bullet = Bullet(self.fromRight, self.rect.y, self.rect.x)
        self.bullets[self.rect.y] = bullet
        return bullet

    def remove_bullet(self, yPosition: int):
        bullet = self.bullets.get(yPosition)
        if bullet is None:
            return
        bullet.kill()

    def can_action(self) -> bool:
        return self.previous_command != self.command
