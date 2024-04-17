import pygame
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

class Monster(pygame.sprite.Sprite):
    def __init__(self, type_monster, num_monster):
        super().__init__()
        self.type_monster = type_monster
        self.num_monster = num_monster
        self.position = [0, 0]
        self.attack = 10
        self.health = 100
        self.max_health = 100
        self.mana = 100
        self.animation_index = 0
        self.animation_delay = 2
        self.image = None
        self.rect = None
        self.feet = None
        self.old_position = self.position.copy()


    def load_points(self, tmx_data):
            point = tmx_data.get_object_by_name(f"{self.type_monster}_{self.num_monster}")
            return pygame.Rect(point.x, point.y, point.width, point.height)
    
    def update(self):
        self.rect.topleft = self.position
        if self.feet:  # Vérifier si self.feet est initialisé
            self.feet.midbottom = self.rect.midbottom

    def save_location(self):
        self.old_position = self.position.copy()

    def teleport_spawn(self, spawn_point):
        self.position[0] = spawn_point.x
        self.position[1] = spawn_point.y
        self.save_location()

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        if self.feet:  # Vérifier si self.feet est initialisé
            self.feet.midbottom = self.rect.midbottom

    def collisions_monster(self, walls, player):
        pass