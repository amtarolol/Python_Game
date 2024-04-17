import pygame
import random

class EcranAccueil:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.particles = []
        self.last_sound_time = 0
        self.button_hovered = False  #
        self.transition_done = False

    def run(self):
        image_accueil = pygame.image.load("../sprites/acceuil/ecran_acceuil.jpg").convert_alpha()
        play_button = pygame.image.load("../sprites/acceuil/play_buttom2.png").convert_alpha()
        son = pygame.mixer.Sound("../sprites/acceuil/acceuil_sound.mp3")
        play_sound = pygame.mixer.Sound("../sprites/acceuil/play_buttom.wav")

        image_rect = image_accueil.get_rect(center=self.screen.get_rect().center)
        button_rect = play_button.get_rect(center=self.screen.get_rect().center)

        zoom_factor = 1.1
        zoom_speed = 0.00075  # Vitesse de l'animation de zoom
        zoom_direction = 1
        change_direction_time = 1500  # Temps en millisecondes avant de changer la direction du zoom
        last_direction_change = pygame.time.get_ticks()  # Temps du dernier changement de direction

        for _ in range(200):
            particle_x = random.randint(0, self.screen.get_width())
            particle_y = random.randint(0, self.screen.get_height())
            self.particles.append(Particle((particle_x, particle_y)))

        mouse_pos = pygame.mouse.get_pos()

        # Jouer le son
        son.play()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_pos):
                        son.stop()
                        running = False
                        if not self.transition_done:  # Vérifiez si la transition n'a pas encore été effectuée
                            self.transition_done = True
                            self.fade_transition() 
                        

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

            # Utiliser pygame.transform.smoothscale() pour redimensionner l'image de fond avec anti-aliasing
            scaled_image = pygame.transform.smoothscale(image_accueil, (int(image_rect.width * zoom_factor), int(image_rect.height * zoom_factor)))
            scaled_rect = scaled_image.get_rect(center=self.screen.get_rect().center)


            scaled_image_button = pygame.transform.smoothscale(play_button, (int(button_rect.width * 0.6), int(button_rect.height * 0.6)))
            scaled_button_rect = scaled_image_button.get_rect(center=self.screen.get_rect().center)

            # Vérifiez si la souris survole le bouton
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                scaled_image_button = pygame.transform.smoothscale_by(scaled_image_button, (1.2, 1.2))
                scaled_button_rect = scaled_image_button.get_rect(center=self.screen.get_rect().center)

                # Vérifiez si la souris vient de commencer à survoler le bouton
                if not self.button_hovered:  
                    self.button_hovered = True
                    # Si le son n'a pas été joué depuis 1 seconde
                    if current_time - self.last_sound_time >= 100:  
                        play_sound.play()
                        self.last_sound_time = current_time
            else:
                self.button_hovered = False

            # Afficher l'image d'accueil à l'écran avec la nouvelle taille
            self.screen.fill((0, 0, 0))  # Fond noir
            self.screen.blit(scaled_image, scaled_rect)
            self.screen.blit(scaled_image_button, scaled_button_rect)

            for particle in self.particles:
                particle.update(self.screen.get_height())  # Passer la hauteur de l'écran
                particle.draw(self.screen)

            pygame.display.flip()

            self.clock.tick(120)

    def fade_transition(self):
        fade_surface = pygame.Surface(self.screen.get_size())  # Surface pour le fondu enchaîné
        fade_surface.fill((0, 0, 0))  # Remplir la surface avec une couleur noire
        for alpha in range(0, 255, 10):  # Augmenter progressivement l'opacité
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(60)  # Délai pour contrôler la vitesse du fondu enchaîné
        # Une fois le fondu enchaîné terminé, commencer à afficher la fenêtre de jeu

class Particle:
    def __init__(self, position):
        # Initialisation de la position et de la vitesse
        self.x, self.y = position
        self.vx = random.uniform(-0.5, 0.5)  # Vitesse horizontale aléatoire
        self.vy = random.uniform(-0.08, -0.15)  # Vitesse verticale vers le haut, plus légère
        self.gravity = 0.01  # Gravité ascendante réduite
        self.color = (random.randint(220, 255), random.randint(180, 255), random.randint(180, 255), random.randint(55, 85)) 
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


