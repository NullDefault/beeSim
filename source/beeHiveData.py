import pygame


class BeeHive(pygame.sprite.DirtySprite):

    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/beeHive_sprites/beeHive_red.png")
        self.dirty = 0
        self.rect = self.image.get_rect()
        self.known_flowers = ()
        self.rect.left, self.rect.top = location

    def remember_flower(self, flower):
        self.known_flowers.append(flower)


