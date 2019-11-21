import pygame
import random


class Flower(pygame.sprite.Sprite):

    test = True
    max_growth_stage = 6

    def __init__(self, location, flower_type):
        pygame.sprite.Sprite.__init__(self)
        if flower_type == 1:
            self.flowerType = "red_flower"
        elif flower_type == 2:
            self.flowerType = "blue_flower"
        else:
            self.flowerType = "purple_flower"

        self.growth_tick = random.randint(0, 100)
        self.current_growth_stage = random.randint(0, 5)
        self.load_sprite()
        self.pollen = 100
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def grow(self, tick):
        if tick == self.growth_tick:
            self.current_growth_stage = self.current_growth_stage + 1
            if self.current_growth_stage == self.max_growth_stage:
                self.current_growth_stage = 0
            self.load_sprite()

    def lose_pollen(self, bee):
        self.pollen = self.pollen - bee.nectar_collection_rate

    def load_sprite(self):
        if self.test:
            self.image = pygame.image.load("assets/Flowers/red_flower/red_flower_5.png")
        else:
            self.image = pygame.image.load("assets/Flowers/" + self.flowerType + "/" + self.flowerType + "_"
                                           + str(self.current_growth_stage) + ".png")


class FlowerSmell(pygame.sprite.Sprite):

    test = True

    def __init__(self, flower):
        pygame.sprite.Sprite.__init__(self)
        if self.test:
            self.image = pygame.image.load("assets/Flowers/flowerSmell_visible.png")
        else:
            self.image = pygame.image.load("assets/Flowers/flowerSmell.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = flower.rect.left-8, flower.rect.top-10
        self.flower = flower
