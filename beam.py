import pygame


class Beam(pygame.sprite.Sprite):

    fromRight: bool

    def __init__(self, fromRight: bool, yPosition: int, xPosition: int):
        pygame.sprite.Sprite.__init__(self)
        self.fromRight = fromRight
        image_path = './assets/pl2beam.png' if fromRight else './assets/pl1beam.png'
        self.image = pygame.image.load(image_path)
        self.rect = pygame.Rect(xPosition, yPosition, self.image.get_width(), self.image.get_height() - 40)

    def update(self, kill: bool):
        if kill == True :
            self.kill()