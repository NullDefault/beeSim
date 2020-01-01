import pygame
import random


class BeeHive(pygame.sprite.DirtySprite):

    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/beeHive_sprites/beeHive_red.png")
        self.nectar_storage = 0
        self.rect = self.image.get_rect()
        self.known_flowers = []
        self.workers = []
        self.scouts = []
        self.rect.left, self.rect.top = location

    def add_worker_bee(self, bee):
        self.workers.append(bee)

    def add_scout_bee(self, bee):
        self.scouts.append(bee)

    def get_bees(self):
        # 0: workers, 1: scouts
        return len(self.workers), len(self.scouts)

    def get_nectar(self):
        return self.nectar_storage

    def gain_nectar(self, nectar_amount):
        self.nectar_storage = self.nectar_storage + nectar_amount

    def remember_flower(self, flower):
        self.known_flowers.append(flower)

    def has_orders(self):
        if len(self.known_flowers) < 1:
            return False
        else:
            return True

    def get_order(self):
        random_index = random.randint(0, len(self.known_flowers)-1)
        flower = self.known_flowers[random_index]
        return flower.rect.left, flower.rect.top




