import os
import pygame

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, max_range=1500, projectile_type="Explosion"):
        super().__init__()
        self.projectile_type = projectile_type
        self.max_range = max_range
        self.position = [x, y]
        self.velocity = None
        self.damage = 0
        self.sprite_sheet = pygame.image.load("ressources/sort/explosion.png")
        self.max_range = max_range
        self.animation_index = 0
        self.clock = 0
        self.images = {
            'use': self.get_images(0) 
        }
        self.animation_delay = 10
        self.image = self.images['use'][0]
        self.rect = self.image.get_rect(center=self.position)
        self.rect.height -= 10
        self.cd = 0
        self.finished = False  # Ajouter une variable pour suivre l'état de l'explosion
        self.state = None

    def animate(self, name="use"):
        if self.finished:
            self.kill()
        else:
            if self.animation_index < len(self.images[name]):
                self.image = self.images[name][self.animation_index]
                self.image.set_colorkey([0, 0, 0])
                self.clock += self.animation_delay
                if self.clock >= 100:
                    self.animation_index += 1
                    self.clock = 0
                    if self.animation_index >= len(self.images[name]):
                        self.finished = True  # L'animation est terminée


    def animate(self, name="use"):
            if self.finished:
                self.kill()
            else:
                if self.animation_index < len(self.images[name]):
                    self.image = self.images[name][self.animation_index]
                    self.image.set_colorkey([0, 0, 0])
                    self.clock += self.animation_delay
                    if self.clock >= 100:
                        self.animation_index += 1
                        self.clock = 0
                        if self.animation_index >= len(self.images[name]):
                            self.finished = True  
                            self.damage = 200
                            self.finished = True
            

    def get_images(self, y):
        images = []
        for i in range(8):
            x = i * 108
            image = self.get_image(x, y)
            images.append(image)
        return images

    def get_image(self, x, y):
        # Créer une surface pour l'image du slime
        image = pygame.Surface([108, 108])
        # Charger l'image du slime depuis la feuille de sprite
        image.blit(self.sprite_sheet, (0, 0), (x, y, 108, 108))
        image = pygame.transform.scale(image, (150, 150))
        return image

    def move(self, x, y):
        self.position[0] = x-(self.image.get_width()/2)
        self.position[1] = y-(self.image.get_width()/2)
