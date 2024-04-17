import os
import pygame

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, max_range=500, projectile_type="Explosion"):
        super().__init__()
        self.projectile_type = projectile_type
        self.max_range = max_range
        self.position =[x, y]
        self.velocity = None
        self.damage = 100
        # Charger la feuille de sprite du slime
        self.sprite_sheet = pygame.image.load("../sort/explosion.png")
        self.max_range = max_range
        self.animation_index = 0
        self.clock = 0
        self.images = {
            'use': self.get_images(0) 
        }
        # Vitesse de l'animation
        self.animation_delay = 10
        self.image =  self.images['use'][0]
        # Définir le rectangle de collision
        self.rect = self.image.get_rect(topleft=self.position)

    def animate(self, name="use"):
        if self.animation_index < len(self.images[name]):
            self.image = self.images[name][self.animation_index]
            self.image.set_colorkey([0, 0, 0])
            self.clock += self.animation_delay
            if self.clock >= 100:
                self.animation_index += 1
                self.clock = 0


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
        image = pygame.transform.scale(image, (256, 256))
        return image
    
    def move(self, x, y):
        self.position[0] = x-(self.image.get_width()/2)
        self.position[1] = y-(self.image.get_width()/2)

