import pygame

from Player_pnj.animation import AnimateSprite
from Spell.projectile import Fire_ball
import os

# répertoire du script actuel
current_directory = os.path.dirname(os.path.abspath(__file__))

# répertoire de travail pour inclure le dossier parent
os.chdir(current_directory)

class Entity(AnimateSprite):

    def __init__(self, name, x, y):
        super().__init__(name)
        self.position = [x, y]
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()

        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()

    def save_location(self): self.old_position = self.position.copy()

    def move_right(self):
        self.change_animation("right")
        self.position[0] += self.speed

    def move_left(self):
        self.change_animation("left")
        self.position[0] -= self.speed

    def move_up(self):
        self.change_animation("up")
        self.position[1] -= self.speed

    def move_down(self):
        self.change_animation("down")
        self.position[1] += self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


class Player(Entity):
    def __init__(self):
        super().__init__("player", 0, 0)
        self.attack = 10
        self.health = 100
        self.max_health = 100
        self.mana = 100
        self.current_speed = 5
        self.speed = self.current_speed
        self.current_frame = 0
        self.all_projectiles = pygame.sprite.Group()
        self.cd = 0.0

    def shoot(self, orientation, map_manager):
        # Récupérer les coordonnées et le rectangle de collision du joueur sur l'écran
        player_screen_x, player_screen_y, player_screen_rect = map_manager.entity_position_and_rect(map_manager.player)
        # Utiliser les coordonnées du joueur sur l'écran pour le tir
        projectile = Fire_ball(player_screen_x, player_screen_y, orientation)
        # Ajouter le projectile au groupe des projectiles du joueur
        self.all_projectiles.add(projectile)


    def check_collision(self, monster):
        collision_rect = monster.rect.copy()  # Copier le rectangle de collision du monstre

        if self.rect.colliderect(collision_rect):
            self.speed = 0  # Arrête le joueur en cas de collision avec le monstre
            self.move_back()
        else:
            self.speed = self.current_speed


class NPC(Entity):

    def __init__(self, name, nb_points, dialog):
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        self.dialog = dialog
        self.points = []
        self.name = name
        self.current_point = 0
        self.speed = 0.5

    def move(self):
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_up()
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_left()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_right()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        for num in range(1, self.nb_points+1):
            point = tmx_data.get_object_by_name(f'{self.name}_path{num}')
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)