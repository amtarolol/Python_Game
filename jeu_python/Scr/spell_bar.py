import pygame
import os

# répertoire du script actuel
current_directory = os.path.dirname(os.path.abspath(__file__))

# répertoire de travail pour inclure le dossier parent
os.chdir(current_directory)
class SpellBar:
    def __init__(self, screen, icons, max_cooldown_time=120):
        self.screen = screen
        self.icons = icons
        self.max_cooldown_time = max_cooldown_time
        self.cooldowns = {"fireball": 0}

        self.icon_size = 50  # Taille des icônes de sorts
        self.icon_scale = 0.5  # Facteur de redimensionnement pour l'icône de la boule de feu
        self.icon_padding = 10  # Espacement entre les icônes
        self.bar_x = 100  # Position horizontale de la barre de sorts
        self.bar_y = self.screen.get_height() - int(self.icon_size * self.icon_scale) - 10

    def update(self):
        for spell in self.cooldowns:
            if self.cooldowns[spell] > 0:
                self.cooldowns[spell] -= 1

    def draw(self):
        x = self.bar_x
        for spell in self.cooldowns:
            if self.cooldowns[spell] > 0:
                icon = self.icons[spell]
                icon = pygame.transform.scale(icon, (int(self.icon_size * self.icon_scale), int(self.icon_size * self.icon_scale)))

                # Crée une surface semi-transparente pour assombrir l'icône
                surface = pygame.Surface(icon.get_size(), pygame.SRCALPHA)
                pygame.draw.rect(surface, (0, 0, 0, 128), surface.get_rect())
                icon = pygame.transform.scale(icon, (int(self.icon_size * self.icon_scale), int(self.icon_size * self.icon_scale)))

                # Blit l'icône assombrie sur la barre de sorts
                self.screen.blit(surface, (x, self.bar_y))
                self.screen.blit(icon, (x, self.bar_y))
            else:
                icon = pygame.transform.scale(self.icons[spell], (int(self.icon_size * self.icon_scale), int(self.icon_size * self.icon_scale)))
                self.screen.blit(icon, (x, self.bar_y))
            x += int(self.icon_size * self.icon_scale) + self.icon_padding

    def cast_spell(self, spell, cooldown_time):
        if self.cooldowns[spell] <= 0:
            # Utiliser le sort
            self.cooldowns[spell] = cooldown_time
