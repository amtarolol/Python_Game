import pygame

class SpellBar:
    def __init__(self, screen, icons, max_cooldown_time=120):
        self.screen = screen
        self.icons = icons
        self.max_cooldown_time = max_cooldown_time
        self.cooldowns = {spell: 0 for spell in icons.keys()}
        self.icon_size = 50  
        self.icon_scale = 0.5  
        self.selected_spell = None  
        self.cooldown_bar_color = (0, 0, 0)  
        self.cooldown_bar_alpha = 70  # Opacité de la barre de remplissage
        self.cooldown_bar_width = 0  

        self.bar_y = self.screen.get_height() - int(self.icon_size * self.icon_scale) - 10

    def update(self):
        for spell in self.cooldowns:
            if self.cooldowns[spell] > 0:
                self.cooldowns[spell] -= 1

    def draw_spell_bar(self):
        bar_width = 210  
        bar_height = 70  
        bar_x = (self.screen.get_width() - bar_width) // 2  
        bar_y = self.screen.get_height() - 2 - bar_height  

        bar_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
        bar_surface.fill((255, 255, 255, 0))  # Fond transparent
        pygame.draw.rect(bar_surface, (0, 0, 0), bar_surface.get_rect(), 5)

        part_width = bar_width // 3  
        for i in range(1, 3):
            pygame.draw.rect(self.screen, (0, 0, 0, 128), (bar_x + part_width * i, bar_y, 5, bar_height))  

        for spell, icon in self.icons.items():
            icon_scaled = pygame.transform.scale(icon, (self.icon_size, self.icon_size))
            spell_rect = icon_scaled.get_rect()
            spell_rect.center = (bar_x + part_width * (list(self.icons.keys()).index(spell) + 0.5), bar_y + bar_height // 2)
            self.screen.blit(icon_scaled, spell_rect)

            if spell == self.selected_spell and self.cooldowns[spell] > 0:
                cooldown_percentage = 1 - (self.cooldowns[spell] / self.max_cooldown_time)
                self.cooldown_bar_width = part_width * cooldown_percentage
                cooldown_bar_rect = pygame.Rect(spell_rect.left, spell_rect.top, self.cooldown_bar_width, bar_height)
                cooldown_bar_surface = pygame.Surface((self.cooldown_bar_width-20, bar_height-20), pygame.SRCALPHA)
                cooldown_bar_surface.set_alpha(self.cooldown_bar_alpha)  
                pygame.draw.rect(cooldown_bar_surface, self.cooldown_bar_color, cooldown_bar_surface.get_rect())  
                self.screen.blit(cooldown_bar_surface, cooldown_bar_rect)

        self.screen.blit(bar_surface, (bar_x, bar_y))

    def select_spell(self, spell, cooldown):
        self.selected_spell = spell
        self.cooldowns[spell] = cooldown  
