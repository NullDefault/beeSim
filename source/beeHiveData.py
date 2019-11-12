import pygame

class BeeHive(pygame.sprite.Sprite):

    position = ()
    numberOfBees = 0





    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)                                                     #call Sprite initializer
        self.image = pygame.image.load("assets/beeHive.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

