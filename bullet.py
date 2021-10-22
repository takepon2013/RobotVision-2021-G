import pygame


class Bullet(pygame.sprite.Sprite):

    fromRight: bool

    def __init__(self, fromRight: bool, yPosition: int):
        pygame.sprite.Sprite.__init__(self)
        self.fromRight = fromRight
        image_path = './assets/bullet-rev.png' if fromRight else './assets/bullet.png'
        self.image = pygame.image.load(image_path)
        self.rect = pygame.Rect(0, yPosition, self.image.get_width(), self.image.get_height())

    def update(self, ):
        if not self.alive():
            return
        diff = 5 if self.fromRight else -5
        self.rect.move_ip(diff, 0)
