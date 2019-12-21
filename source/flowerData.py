import pygame


class Flower(pygame.sprite.Sprite):

    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/flower_sprites/flower_sprites4.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
