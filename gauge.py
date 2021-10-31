import pygame


class Gauge(pygame.sprite.Sprite):

    fromRight: bool

    def __init__(self, fromRight: bool):
        pygame.sprite.Sprite.__init__(self)
        self.fromRight = fromRight
        image_path = './assets/gauge/2gauge0.png' if fromRight else './assets/gauge/1gauge0.png'
        self.image = pygame.image.load(image_path)
        xPosition = 800 if fromRight else 400
        self.rect = pygame.Rect(xPosition, 485, self.image.get_width(), self.image.get_height())

    def update(self, gauge: int):
        if self.fromRight == False:
            if gauge < 10:
                self.image = pygame.image.load('./assets/gauge/1gauge0.png')
            elif gauge < 20:
                self.image = pygame.image.load('./assets/gauge/1gauge1.png')
            elif gauge < 30:
                self.image = pygame.image.load('./assets/gauge/1gauge2.png')
            elif gauge < 40:
                self.image = pygame.image.load('./assets/gauge/1gauge3.png')
            elif gauge < 50:
                self.image = pygame.image.load('./assets/gauge/1gauge4.png')
            elif gauge < 60:
                self.image = pygame.image.load('./assets/gauge/1gauge5.png')
            elif gauge < 70:
                self.image = pygame.image.load('./assets/gauge/1gauge6.png')
            elif gauge < 80:
                self.image = pygame.image.load('./assets/gauge/1gauge7.png')
            elif gauge < 90:
                self.image = pygame.image.load('./assets/gauge/1gauge8.png')
            elif gauge < 100:
                self.image = pygame.image.load('./assets/gauge/1gauge9.png')
            elif gauge == 100:
                self.image = pygame.image.load('./assets/gauge/1gauge10.png')
        
        else:
            if gauge < 10:
                self.image = pygame.image.load('./assets/gauge/2gauge0.png')
            elif gauge < 20:
                self.image = pygame.image.load('./assets/gauge/2gauge1.png')
            elif gauge < 30:
                self.image = pygame.image.load('./assets/gauge/2gauge2.png')
            elif gauge < 40:
                self.image = pygame.image.load('./assets/gauge/2gauge3.png')
            elif gauge < 50:
                self.image = pygame.image.load('./assets/gauge/2gauge4.png')
            elif gauge < 60:
                self.image = pygame.image.load('./assets/gauge/2gauge5.png')
            elif gauge < 70:
                self.image = pygame.image.load('./assets/gauge/2gauge6.png')
            elif gauge < 80:
                self.image = pygame.image.load('./assets/gauge/2gauge7.png')
            elif gauge < 90:
                self.image = pygame.image.load('./assets/gauge/2gauge8.png')
            elif gauge < 100:
                self.image = pygame.image.load('./assets/gauge/2gauge9.png')
            elif gauge == 100:
                self.image = pygame.image.load('./assets/gauge/2gauge10.png')
            