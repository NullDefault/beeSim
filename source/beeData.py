import pygame
import random


class Bee(pygame.sprite.Sprite):
########################################################################################################################
    # Class Fields

    left_sprite = pygame.image.load("assets/bee_sprites/beeSprite_left.png")
    right_sprite = pygame.image.load("assets/bee_sprites/beeSprite_right.png")
    up_sprite = pygame.image.load("assets/bee_sprites/beeSprite_up.png")
    down_sprite = pygame.image.load("assets/bee_sprites/beeSprite_down.png")

    search_radius = 400
    wiggle = 1
    speed = 4
    roam_percentages = (0.64, 0.36)

########################################################################################################################

    def __init__(self, location, queen):

        self.queen_hive = queen
        self.queen_hive_x = queen.rect.left + 33
        self.queen_hive_y = queen.rect.top + 52
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/bee_sprites/beeSprite_down.png")
        self.target_destination = (self.queen_hive_x, self.queen_hive_y)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def update_target(self, current_state):
        if current_state == 'await orders':
            return self.check_available_orders()
        elif current_state == 'harvest':
            return self.harvest_flower()
        elif current_state == 'scout':
            return self.search_for_flowers()
        elif current_state == 'head back':
            return self.deliver_nectar_load()
        elif current_state == 'offload':
            return self.offload()
        elif current_state == 'report':
            return self.report_back_to_hive()

    def head_towards(self):

        x_distance = self.target_destination[0] - (self.rect.left + 5)
        y_distance = self.target_destination[1] - (self.rect.top + 4)

        dx = 0
        dy = 0

        movement_points_to_spend = self.speed

        while True:
            if movement_points_to_spend == 0:
                break
            coin_flip = random.randint(0, 1)
            if coin_flip == 0:
                dx = dx + 1
            else:
                dy = dy + 1

            movement_points_to_spend = movement_points_to_spend - 1

        if x_distance < 0:
            dx = -dx
        if y_distance < 0:
            dy = -dy

        if -4 < x_distance < 4:
            dx = 0
        if -4 < y_distance < 4:
            dy = 0

        random_x_offset = random.randint(-self.wiggle, self.wiggle)
        random_y_offset = random.randint(-self.wiggle, self.wiggle)
        self.rect.top = self.rect.top + dy + random_x_offset
        self.rect.left = self.rect.left + dx + random_y_offset

    def update_sprite(self):

        x_distance = self.target_destination[0] - self.rect.left
        y_distance = self.target_destination[1] - self.rect.top

        if abs(x_distance) > abs(y_distance):
            if x_distance < 0:
                self.image = self.left_sprite
            else:
                self.image = self.right_sprite
        else:
            if y_distance < 0:
                self.image = self.up_sprite
            else:
                self.image = self.down_sprite

    def validate_collision(self):
        if self.bee_states.current == 'scout' or self.bee_states.current == 'go to flower':
            return True
        else:
            return False

    def collide_with_flower(self, flower):
        if self.bee_states.current == 'scout':
            self.bee_states.trigger('found flower')
            self.remembered_flower = flower
        if self.bee_states.current == 'go to flower':
            self.bee_states.trigger('arrived at flower')
