import os
import pygame
import math

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

class Fire_ball(pygame.sprite.Sprite):
    def __init__(self, x, y, orientation="left", max_range=300):
        super().__init__()
        self.max_range = max_range
        self.orientation = orientation
        self.position =[x, y]
        self.velocity = 8
        self.damage = 50
        self.images = self.load_animation_images()
        self.image = self.images[0]  # Initialiser avec la première image
        self.rect = self.image.get_rect(topleft=self.position)
        self.current_image = 0  # Ajout de l'initialisation de current_image
        self.animation_counter = 0
        self.animation_delay = 5 
        self.angle = None

    def load_animation_images(self):
        images = []
        path = '../sort/fire_ball_'
        for num in range(1, 9):
            image_path = path + str(num) + '.png'
            img = pygame.image.load(image_path).convert()
            img.set_colorkey([0, 0, 0])
            img = pygame.transform.scale(img, (55, 35))
            images.append(img)
        return images

    def animate(self):
        # Met à jour l'image seulement toutes les N itérations
        if self.animation_counter % self.animation_delay == 0:
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image = self.images[self.current_image]
            if self.angle:
                rotated_image = pygame.transform.rotate(self.image, self.angle)

                # Update the object's image and rect with the rotated image
                self.image = rotated_image
                self.rect = rotated_image.get_rect(center=self.rect.center)

    def move3(self, x_souris, y_souris):
        # Calculate the vector between the object position and the mouse position
        dx = x_souris - self.position[0]
        dy = y_souris - self.position[1]
        # Calculate the angle in radians between the object position and the mouse position
        angle_rad = math.atan2(-dy, dx)
        # Convert the angle to degrees
        self.angle = math.degrees(angle_rad)
        # Normalize the vector (to maintain constant speed)
        magnitude = math.sqrt(dx ** 2 + dy ** 2)
        if magnitude != 0:
            dx /= magnitude
            dy /= magnitude
        # Move the object along the normalized vector
        self.position[0] += dx * self.velocity
        self.position[1] += dy * self.velocity

        # Check if the fireball has reached the target position
        if math.sqrt((self.position[0] - x_souris) ** 2 + (self.position[1] - y_souris) ** 2) < 10:
            self.kill()
