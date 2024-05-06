import pygame

class SpellBar:
    def __init__(self, screen, icons, max_cooldown_time=1000):
        self.screen = screen
        self.icons = icons
        self.max_cooldown_time = max_cooldown_time
        self.cooldowns = {spell: 0 for spell in self.icons.keys()}
        self.cooldown_bars = {spell: (0, 0) for spell in self.icons.keys()}  # Stocker la largeur et le cooldown restant
        self.icon_size = 50
        self.icon_scale = 0.5
        self.selected_spell = None
        self.cooldown_bar_color = (0, 0, 0)
        self.cooldown_bar_alpha = 70  # Opacité de la barre de remplissage

    def update(self):
        self.icons = self.icons
        self.cooldown_bars = {spell: (0, 0) for spell in self.icons.keys()}
        for spell in self.cooldowns:
            if self.cooldowns[spell] > 0:
                self.cooldowns[spell] -= 1
                self.cooldown_bars[spell] = (
                    max(0, self.cooldown_bars[spell][0] - self.max_cooldown_time / 120),
                    self.cooldowns[spell]
                )


    def draw_spell_bar(self):
        nb_icons = len(self.icons)
        bar_width = nb_icons * 70
        bar_height = 70
        bar_x = (self.screen.get_width() - bar_width) // 2
        bar_y = self.screen.get_height() - 2 - bar_height

        bar_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
        bar_surface.fill((255, 255, 255, 0))  # Fond transparent
        pygame.draw.rect(bar_surface, (0, 0, 0), bar_surface.get_rect(), 5)

        part_width = bar_width // nb_icons
        for i in range(1, nb_icons):
            pygame.draw.rect(self.screen, (0, 0, 0, 128), (bar_x + part_width * i, bar_y, 5, bar_height))

        for spell, icon in self.icons.items():
            icon_scaled = pygame.transform.scale(icon, (self.icon_size, self.icon_size))
            spell_rect = icon_scaled.get_rect()
            spell_rect.center = (bar_x + part_width * (list(self.icons.keys()).index(spell) + 0.5), bar_y + bar_height // 2)
            self.screen.blit(icon_scaled, spell_rect)

            # Dessiner le cooldown pour chaque sort
            cooldown_bar_width, cooldown_remaining = self.cooldown_bars[spell]
            if cooldown_remaining > 0:
                cooldown_percentage = 1 - (cooldown_remaining / self.max_cooldown_time)
                cooldown_bar_width = part_width * cooldown_percentage
                cooldown_bar_width = max(0, cooldown_bar_width)
                cooldown_bar_rect = pygame.Rect(spell_rect.left, spell_rect.top, cooldown_bar_width, bar_height)
                cooldown_bar_surface = pygame.Surface((cooldown_bar_width - 20, bar_height - 20), pygame.SRCALPHA)
                cooldown_bar_surface.set_alpha(self.cooldown_bar_alpha)
                pygame.draw.rect(cooldown_bar_surface, self.cooldown_bar_color, cooldown_bar_surface.get_rect())
                self.screen.blit(cooldown_bar_surface, cooldown_bar_rect)

        self.screen.blit(bar_surface, (bar_x, bar_y))



    def select_spell(self, spell, cooldown):
        self.selected_spell = spell
        self.cooldowns[spell] = cooldown
        self.cooldown_bars[spell] = (0, cooldown)
