import pygame

class AnimateSlime(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        # Charger la feuille de sprite du slime
        self.sprite_sheet = pygame.image.load("../sprites/monstres/slime_move.png")
        self.animation_index = 0
        self.clock = 0
        self.images = {
            'first_row': self.get_images(0),
            'move': self.get_images(20),  # Ajouter un espacement de 10 pixels entre les rangées
            'jump': self.get_images(40)  # Ajouter un espacement de 10 pixels entre les rangées
        }
        # Vitesse de l'animation
        self.speed = 25
        self.move_speed = 5
        # Définir le rectangle de collision
        self.rect = self.images['first_row'][0].get_rect()
        # Largeur et hauteur de l'écran
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Position initiale du slime
        self.x_pos = 15
        self.y_pos = 300

    def change_animation(self, name, flip=False):
        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey([0, 0, 0])
        self.clock += self.speed

        if self.clock >= 100:
            self.animation_index += 1
            if self.animation_index >= len(self.images[name]):
                self.animation_index = 0
            self.clock = 0
            # Si le slime sort de l'écran, revenir au début
            if self.x_pos >= self.screen_width:
                self.x_pos = 0

        # Mettre à jour la position du rectangle de collision
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos  # Mettre à jour la position y du rectangle de collision

        # Inverser l'image si nécessaire
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)


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

# Initialiser Pygame
pygame.init()

# Définir les dimensions de la fenêtre
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Créer le slime avec les dimensions de l'écran
slime = AnimateSlime(WINDOW_WIDTH, WINDOW_HEIGHT)

# Configuration de la fenêtre
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Animation de slime")

# Couleur de fond
WHITE = (255, 255, 255)

# Boucle de jeu
running = True
clock = pygame.time.Clock()
while running:
    window.fill(WHITE)

    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Animation par défaut si aucune touche n'est enfoncée
    slime.change_animation('first_row')

    # Vérifier les touches enfoncées
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        slime.change_animation('move') 
        slime.x_pos += 10  # Déplacer le slime vers la droite
    elif keys[pygame.K_q]:
        slime.change_animation('move', flip=True)  # Inverser l'animation
        slime.x_pos -= 10  # Déplacer le slime vers la gauche
    elif keys[pygame.K_z]:
        slime.y_pos -= 10  # Déplacer le slime vers le haut
    elif keys[pygame.K_s]:
        slime.y_pos += 10  # Déplacer le slime vers le bas
    if keys[pygame.K_SPACE]:
        slime.change_animation('jump')

    # Mettre à jour la position y du rectangle de collision
    slime.rect.y = slime.y_pos

    # Centrer l'image du slime sur l'écran
    image_rect = slime.rect
    image_rect.center = (slime.x_pos, slime.y_pos)

    # Afficher le slime
    window.blit(slime.image, image_rect)

    # Actualiser l'écran
    pygame.display.flip()

    # Réguler la vitesse de la boucle
    clock.tick(30)

pygame.quit()
