import sys

import pygame
import cv2
import player

class GameScreen:
    width: int
    height: int
    screen: pygame.Surface
    background: pygame.Surface
    finish: bool
    first_bullet_group: pygame.sprite.Group
    second_bullet_group: pygame.sprite.Group
    player_group: pygame.sprite.Group

    def __init__(self, cap_width: int, cap_height: int):

        # スクリーンとバックグランドの設定
        self.screen = pygame.display.set_mode((int(cap_width), int(cap_height)))
        self.background = pygame.image.load('./assets/bg.png')
        self.background = pygame.transform.scale(self.background, (int(cap_width), int(cap_height)))
        self.screen.blit(self.background, (0, 0))
        print((int(cap_width), int(cap_height)))
        self.finish = False

        # プレイヤーと弾丸の設定
        self.player_group = pygame.sprite.Group()
        self.first_bullet_group = pygame.sprite.Group()
        self.second_bullet_group = pygame.sprite.Group()

        self.first_player = player.Player(self.background, False)
        self.second_player = player.Player(self.background, True)

        self.player_group.add(self.first_player)
        self.player_group.add(self.second_player)

        # キーボードの入力キーがないので空文字を渡している
        self.player_group.update('')

    def updateFrame(self, first_command: int, second_command: int) -> bool:
        self.first_player.command = first_command
        self.second_player.command = second_command
        self.player_group.clear(self.screen, self.background)
        self.first_bullet_group.clear(self.screen, self.background)
        self.second_bullet_group.clear(self.screen, self.background)

        if self.first_player.can_action() and self.first_player.command == 1:
            new_bullet = self.first_player.generate_bullet()
            self.first_bullet_group.add(new_bullet)
        if self.second_player.can_action() and self.second_player.command == 1:
            new_bullet = self.second_player.generate_bullet()
            self.second_bullet_group.add(new_bullet)

        # ユーザー入力
        for event in pygame.event.get():
            print('event')
            if event.type == pygame.QUIT:
                self.finish = True
            elif event.type == pygame.KEYDOWN:
                self.player_group.update(event.key)

        # 衝突判定

        self.first_bullet_group.update()
        self.second_bullet_group.update()

        self.first_bullet_group.draw(self.screen)
        self.second_bullet_group.draw(self.screen)
        self.player_group.draw(self.screen)

        pygame.display.flip()

        return self.finish
