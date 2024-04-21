from monstres.momy import Mommy
from monstres.slime import Slime
import random
import os

# répertoire du script actuel
current_directory = os.path.dirname(os.path.abspath(__file__))

# répertoire de travail pour inclure le dossier parent
os.chdir(current_directory)
initial_monster_config = {

            "future_map_1": [
                Mommy(),
                *[Slime(random.randint(1, 5)) for _ in range(random.randint(1, 5))]
            ],
            "map_2": []
            # Ajoutez d'autres configurations pour les autres cartes si nécessaire
        }

for i in initial_monster_config["future_map_1"]:
    print(str(i))