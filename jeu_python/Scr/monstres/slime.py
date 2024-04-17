import pygame
import random
from monstres.monster import Monster
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

class Slime(Monster):
    def __init__(self, num_monster, type_monster="slime"):
        super().__init__(type_monster, num_monster)
        self.type_monster = type_monster
        self.num_monster = num_monster
        self.animation_index = 0
        self.cooldown_timer = 0
        self.cooldown_duration = self.cooldown_duration = random.randint(2000, 3500) 
        self.animation_delay = 25
        self.sprite_sheet = pygame.image.load("../sprites/monstres/slime_move.png")
        self.images = {
            'first_row': self.get_images(6),
            'move': self.get_images(20),  # Ajouter un espacement de 10 pixels entre les rangées
            'jump': self.get_images(40)  # Ajouter un espacement de 10 pixels entre les rangées
        }
        self.move_speed = 1.1  # Réglage de la vitesse de mouvement du slime
        self.move_increment = 1.1  # Incrément de mouvement pour un déplacement progressif
        self.move_distance = 30  # Distance de déplacement souhaitée
        self.move_direction = None  # Direction de déplacement actuelle
        self.move_amount = 0  # Quantité de déplacement effectuée
        self.image = self.images['first_row'][0]
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.rect.height -= 20
        self.rect = self.rect.inflate(-5, -5)
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.feet.midbottom = self.rect.midbottom

    def change_animation(self, name="first_row", flip=False):
        self.image = self.images[name][self.animation_index // self.animation_delay]
        self.image.set_colorkey([0, 0, 0])

        # Mettre à jour la position du rectangle de collision
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        # Inverser l'image si nécessaire
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)

        # Incrémenter l'index d'animation
        self.animation_index += 1
        if self.animation_index >= len(self.images[name]) * self.animation_delay:
            self.animation_index = 0

    def get_images(self, y):
        images = []
        for i in range(8):
            x = i * (20 + 10)
            image = self.get_image(x, y)
            images.append(image)
        return images

    def get_image(self, x, y):
        # Créer une surface pour l'image du slime
        image = pygame.Surface([20, 20])
        # Charger l'image du slime depuis la feuille de sprite
        image.blit(self.sprite_sheet, (0, 0), (x, y, 20, 20))
        image = pygame.transform.scale(image, (64, 64))
        return image
    
    def animate(self):
        if pygame.time.get_ticks() - self.cooldown_timer > self.cooldown_duration:
            if self.move_direction is None:
                # Mouvements possibles
                possible_movements = [
                    ('right', 30),
                    ('left', -30),
                    ('up', -30),
                    ('down', 30),
                    ('jump_right', 40),
                    ('jump_left', -40),
                ]
                # Choisir un mouvement aléatoire
                movement, distance = random.choice(possible_movements)
                
                self.move_direction = movement
                self.move_amount = 0
                self.cooldown_timer = pygame.time.get_ticks()
            else:
                # Appliquer le mouvement choisi progressivement
                if self.move_direction == 'right':
                    self.change_animation('move')
                    self.position[0] += self.move_increment
                    self.update()
                elif self.move_direction == 'left':
                    self.change_animation('move', flip=True)
                    self.position[0] -= self.move_increment
                elif self.move_direction == 'up':
                    self.change_animation('jump')
                    self.position[1] -= self.move_increment
                elif self.move_direction == 'down':
                    self.change_animation('jump')
                    self.position[1] += self.move_increment
                elif self.move_direction == 'jump_right':
                    self.change_animation('jump')
                    self.position[0] += self.move_increment
                    self.position[1] -= self.move_increment
                elif self.move_direction == 'jump_left':
                    self.change_animation('jump', flip=True)
                    self.position[0] -= self.move_increment
                    self.position[1] -= self.move_increment
                
                self.move_amount += self.move_increment
                if self.move_amount >= self.move_distance:
                    self.move_direction = None
                
                self.cooldown_duration = self.cooldown_duration = random.randint(2000, 3500) 
        else:
            self.change_animation('first_row')
        
