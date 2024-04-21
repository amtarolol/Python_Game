import pygame
import os
from monstres.monster import Monster
from Spell.state import Etats

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

class Mommy(Monster):
    def __init__(self, num_monster, type_monster="mommy"):
        super().__init__(type_monster, num_monster)
        self.type_monster = type_monster
        self.num_monster = num_monster
        self.position = [0, 0]
        self.attack = 10
        self.health = 100
        self.max_health = 100
        self.mana = 100
        self.moving_left = True
        self.animation_images_left = self.load_animation_images(True)
        self.animation_images_right = self.load_animation_images(False)
        self.animation_index = 0
        self.animation_delay = 2
        if self.moving_left:
            self.animation_images = self.animation_images_left
        else:
            self.animation_images = self.animation_images_right
        self.image = self.animation_images[0]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x =  self.position[0]
        self.rect.y = self.position[1]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.speedx = 1.1
        self.speedy = 1.1
        self.feet.midbottom = self.rect.midbottom
        self.old_position = self.position.copy()

    def collisions_monster(self, walls, player):
        new_x = self.position[0] - self.speedx
        new_y = self.position[1] - self.speedy

        # Créer de nouveaux rectangles pour la nouvelle position
        new_rect = self.rect.copy()
        new_rect.midbottom = (new_x, new_y)
        new_feet_rect = self.feet.copy()
        new_feet_rect.midbottom = (new_x, new_y)

        # Vérifier les collisions avec les murs sur l'axe y
        for wall in walls:
            if new_feet_rect.colliderect(wall):
                self.speedy = -self.speedy
                new_y = self.position[1]  # Revenir à la position précédente en y
                new_rect.midbottom = (new_x, new_y)
                new_feet_rect.midbottom = (new_x, new_y)

        if new_rect.x <= 0:
            self.speedx = -self.speedx
            self.moving_left = not self.moving_left
            self.animation_index = 0 

        if player.rect.colliderect(new_rect):
            if (player.rect.top >= new_rect.top and player.rect.top <= new_rect.bottom) or (player.rect.bottom <= new_rect.top and player.rect.bottom >= new_rect.bottom):
                self.speedy = -self.speedy
                new_y = self.position[1]
                new_rect.midbottom = (new_x, new_y)
                new_feet_rect.midbottom = (new_x, new_y)
            if (player.rect.right >= new_feet_rect.left and player.rect.right <= new_feet_rect.right) or (player.rect.left >= new_feet_rect.left and player.rect.left <= new_feet_rect.right):
                self.speedx = -self.speedx
                self.moving_left = not self.moving_left
                self.animation_index = 0 

        # Mettre à jour la position et les rectangles après les collisions
        self.position = [new_x, new_y]
        self.rect = new_rect
        self.feet = new_feet_rect
        self.save_location()

    def load_animation_images(self, moving_left):
        animation_images = []
        for i in range(1, 25):
            image_path = (
                f'ressources/sprites/monstres/mummy/mummy{i}.png'
                if moving_left
                else f'ressources/sprites/monstres/mummy/mummy_back_{i}.png'
            )
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (50, 50))
            animation_images.append(image)
        return animation_images

    def animate(self):
        if self.moving_left:
            animation_images = self.animation_images_left
        else:
            animation_images = self.animation_images_right

        self.image = animation_images[self.animation_index // self.animation_delay]
        self.animation_index += 1
        if self.animation_index >= len(animation_images) * self.animation_delay:
            self.animation_index = 0
