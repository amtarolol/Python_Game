
import pygame

class Player:
    def __init__(self):
        self.attack = 10
        self.health = 100
        self.max_health = 100
        self.power = 1
        self.magic_power = 1
        self.mana = 100
        self.max_mana = 100
        self.level = 1
        self.xp = 0
        self.max_xp = 100
        self.current_speed = 3
        self.speed = self.current_speed
        self.current_frame = 0
        self.cdr = 1

player = Player()


spell_properties = {
    "fireball": {"icon": "bleu", "max_range": 300,
                 "cd": 0, "wait_cd": 250 , "level_required": 1},
    "iceball": {"icon": "bleu", "max_range": 500,
                "cd": 0, "wait_cd": 80 * player.cdr, "level_required": 1},
    "lave": {"icon": "bleu", "max_range": 800,
             "cd": 0, "wait_cd": 20 * player.cdr, "level_required": 2}
}
# Créer un dictionnaire pour stocker les icônes de sorts
spell_icons = {}
# Filtrer les sorts en fonction du niveau requis du joueur
for spell_name, properties in spell_properties.items():
    if player.level  >= properties["level_required"]:
        spell_icons[spell_name] = properties["icon"]

print(len(spell_icons))