import pygame
import random
from monstres.monster import Monster
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

class Rabbit(Monster):
    def __init__(self, num_monster, type_monster="rabbit"):
        super().__init__(type_monster, num_monster)
        self.health = 50
        self.max_health = 50
        self.degat_collision = self.max_health * 0.05
        self.mana = 0
        self.max_mana = 0
        self.type_monster = type_monster
        self.num_monster = num_monster
        self.animation_index = 0
        self.cooldown_timer = 0
        self.cooldown_duration = self.cooldown_duration = random.randint(800, 1500) 
        self.animation_delay = 10
        self.sprite_sheet = pygame.image.load("ressources/sprites/monstres/lapin_move.png")
        self.images = {
            'down': self.get_images(0),
            'left': self.get_images(30),  
            'right': self.get_images(60),
            'up': self.get_images(90)    
        }
        self.move_speed = 1.3  # Réglage de la vitesse de mouvement
        self.move_increment = 1.15  # Incrément de mouvement pour un déplacement progressif
        self.move_distance = 50  # Distance de déplacement souhaitée
        self.move_direction = None  # Direction de déplacement actuelle
        self.move_amount = 0  # Quantité de déplacement effectuée
        self.image = self.images['down'][0]
        
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.feet.midbottom = self.rect.midbottom

    def change_animation(self, name, flip=False):
        self.image = self.images[name][self.animation_index // self.animation_delay]
        self.image.set_colorkey([0, 0, 0])
        # Mettre à jour la position du rectangle de collision
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
        # Inverser l'image si nécessaire
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)
        # Incrémenter l'index d'animation
        self.animation_index += 1
        if self.animation_index >= len(self.images[name]) * self.animation_delay:
            self.animation_index = 0


    def get_images(self, y):
        images = []
        for i in range(3):
            if i < 90:
                x = i * (30)
            image = self.get_image(x, y)
            images.append(image)
        return images

    def get_image(self, x, y):
        # Créer une surface pour l'image du slime
        image = pygame.Surface([30, 30])
        # Charger l'image du slime depuis la feuille de sprite
        image.blit(self.sprite_sheet, (0, 0), (x, y, 30, 30))
        image = pygame.transform.scale(image, (48, 48))
        return image

    def animate(self, walls, player):
        self.save_location()
        self.collisions_monster(walls, player)
        if pygame.time.get_ticks() - self.cooldown_timer > self.cooldown_duration:
            if self.move_direction is None:
                # Mouvements possibles
                possible_movements = [
                    ('right', 50),
                    ('left', -50),
                    ('up', -50),
                    ('down', 50),
                ]
                # Choisir un mouvement aléatoire
                movement, distance = random.choice(possible_movements)
                
                self.move_direction = movement
                self.move_amount = 0
                self.cooldown_timer = pygame.time.get_ticks()
            else:
                # Appliquer le mouvement choisi progressivement
                if not self.repulsion:
                    if self.move_direction == 'right':
                        self.change_animation('right')
                        self.position[0] += self.move_increment
                        self.update()
                    elif self.move_direction == 'left':
                        self.change_animation('left')
                        self.position[0] -= self.move_increment
                    elif self.move_direction == 'up':
                        self.change_animation('up')
                        self.position[1] -= self.move_increment
                    elif self.move_direction == 'down':
                        self.change_animation('down')
                        self.position[1] += self.move_increment

                    self.move_amount += self.move_increment
                    if self.move_amount >= self.move_distance:
                        self.move_direction = None
                    self.cooldown_duration = random.randint(800, 1500)
                else:
                    # Appliquer la répulsion
                    self.position[0] += self.repulsion_x
                    self.position[1] += self.repulsion_y
                    self.repulsion = False

