import pygame
import random

class EcranAccueil:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.particles = []

    def run(self):
        image_accueil = pygame.image.load("../sprites/acceuil/ecran_acceuil.jpg").convert_alpha()
        image_rect = image_accueil.get_rect(center=self.screen.get_rect().center)

        zoom_factor = 1.1
        zoom_speed = 0.00055  # Vitesse de l'animation de zoom
        zoom_direction = 1
        change_direction_time = 1500  # Temps en millisecondes avant de changer la direction du zoom
        last_direction_change = pygame.time.get_ticks()  # Temps du dernier changement de direction

        font = pygame.font.Font(None, 36)
        text = font.render("Appuyez sur Espace pour commencer", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.screen.get_rect().center)

        # Liste pour stocker les particules
        particles = []

        for _ in range(200):
            particle_x = random.randint(0, self.screen.get_width())
            particle_y = random.randint(0, self.screen.get_height())
            self.particles.append(Particle((particle_x, particle_y)))

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    running = False

            current_time = pygame.time.get_ticks()

            # Si le temps écoulé depuis le dernier changement de direction est supérieur au temps spécifié
            if current_time - last_direction_change >= change_direction_time:
                # Changer la direction du zoom
                zoom_direction *= -1
                # Mettre à jour le temps du dernier changement de direction
                last_direction_change = current_time

            # Mettre à jour la taille de l'image en fonction de la direction du zoom
            zoom_factor += zoom_direction * zoom_speed
            if zoom_factor < 0.5:
                zoom_factor = 0.5  # Limiter la valeur minimale de zoom_factor

            # Utiliser pygame.transform.smoothscale() pour redimensionner l'image avec anti-aliasing
            scaled_image = pygame.transform.smoothscale(image_accueil, (int(image_rect.width * zoom_factor), int(image_rect.height * zoom_factor)))
            scaled_rect = scaled_image.get_rect(center=self.screen.get_rect().center)

            # Afficher l'image d'accueil à l'écran avec la nouvelle taille
            self.screen.fill((0, 0, 0))  # Fond noir
            self.screen.blit(scaled_image, scaled_rect)
            self.screen.blit(text, text_rect)  # Afficher le texte devant l'image

            for particle in self.particles:
                particle.update(self.screen.get_height())  # Passer la hauteur de l'écran
                particle.draw(self.screen)

            pygame.display.flip()

            self.clock.tick(120)

class Particle:
    def __init__(self, position):
        # Initialisation de la position et de la vitesse
        self.x, self.y = position
        self.vx = random.uniform(-0.5, 0.5)  # Vitesse horizontale aléatoire
        self.vy = random.uniform(-0.08, -0.15)  # Vitesse verticale vers le haut, plus légère
        self.gravity = 0.01  # Gravité ascendante réduite
        self.color = (random.randint(190, 255), random.randint(190, 255), random.randint(190, 255), 80) 
        self.size = random.randint(2, 4)  # Taille légèrement variable

    def update(self, screen_height):
        # Mettre à jour la position en fonction de la vitesse
        self.x += self.vx
        self.y += self.vy

        
        # Vérifier si la particule dépasse la limite inférieure de l'écran
        if self.y > screen_height:
            self.y = random.uniform(0, screen_height)


    def draw(self, surface):
        # Créer une surface avec une transparence alpha
        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        # Dessiner un cercle rempli sur la surface avec la couleur et la transparence appropriées
        pygame.draw.circle(particle_surface, self.color, (self.size, self.size), self.size)
        # Dessiner la surface des particules sur l'écran de jeu
        surface.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))
