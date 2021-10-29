import pygame


class Bullet(pygame.sprite.Sprite):

    fromRight: bool

    def __init__(self, fromRight: bool, yPosition: int, xPosition: int):
        pygame.sprite.Sprite.__init__(self)
        self.fromRight = fromRight
<<<<<<< HEAD
        image_path = './assets/pl2tama.png' if fromRight else './assets/pl1tama.png'
=======
        image_path = './assets/bullet-rev.png' if fromRight else './assets/bullet.png'
>>>>>>> origin/main
        self.image = pygame.image.load(image_path)
        self.rect = pygame.Rect(xPosition, yPosition, self.image.get_width(), self.image.get_height())

    def update(self, ):
        if not self.alive():
            return
<<<<<<< HEAD
        diff = -13 if self.fromRight else 13
=======
        diff = -5 if self.fromRight else 5
>>>>>>> origin/main
        self.rect.move_ip(diff, 0)
