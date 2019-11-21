import pygame


class BeeHive(pygame.sprite.Sprite):

    known_flowers = ()

    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/beeHive_red.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.position = (self.rect.left, self.rect.top)

    def remember_flower(self, flower):
        self.known_flowers.append(flower)


