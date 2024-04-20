from Spell.fire_ball import Fire_ball
from Spell.explosion import Explosion
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

class Spell:
    def __init__(self, player_screen_x, player_screen_y):
        self.player_screen_x = player_screen_x
        self.player_screen_y = player_screen_y
        self.spells = {
            "explosion": Explosion,
            "fire_ball": Fire_ball
            # Ajoutez d'autres sorts ici selon vos besoins
        }

    def use_spell(self, spell_name):
        # Vérifie si le sort existe dans le dictionnaire, sinon retourne None
        spell_class = self.spells.get(spell_name)
        if spell_class:
            # Créer une instance du sort avec les coordonnées du joueur
            return spell_class(self.player_screen_x, self.player_screen_y)
        else:
            return None