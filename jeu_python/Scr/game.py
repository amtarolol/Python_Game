import pygame
from dialog import DialogBox
from map import MapManager
from Player_pnj.player import Player
from Spell.spell_bar import SpellBar
from Spell.projectile import Fire_ball
import os


# répertoire du script actuel
current_directory = os.path.dirname(os.path.abspath(__file__))

# répertoire de travail pour inclure le dossier parent 
os.chdir(current_directory)

class Game:
    def __init__(self):
        # initialisation de pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        # fenetre de jeux
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN | pygame.SRCALPHA)
        pygame.display.set_caption('Dream Land')
        
        # generer un joueur
        self.player = Player()
        self.orientation = "right"
        self.all_projectiles = pygame.sprite.Group()
        self.map_manager = MapManager(self.screen, self.player)
        self.monsters = self.map_manager.get_map().monsters
        self.dialog_box = DialogBox()
        self.spell_use = "fireball"

        # Spell properties
        self.spell_properties = {
            "fireball": {"icon": pygame.image.load("../sort/spell_bar/feu.PNG"), "max_range": 300},
            "iceball": {"icon": pygame.image.load("../sort/spell_bar/glace.JPG"), "max_range": 500},
            "lave": {"icon": pygame.image.load("../sort/spell_bar/lave.JPG"), "max_range": 300}
        }
        spell_icons = {spell_name: properties["icon"] for spell_name, properties in self.spell_properties.items()}
        self.spell_bar = SpellBar(self.screen, spell_icons)


    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_z]:
            self.player.move_up()
        elif pressed[pygame.K_s]:
            self.player.move_down()
        elif pressed[pygame.K_q]:
            self.player.move_left()
            self.orientation = "left"
        elif pressed[pygame.K_d]:
            self.player.move_right()
            self.orientation = "right"

    def update(self):
        self.map_manager.update()

    def run(self):
        clock = pygame.time.Clock()

        # boucle du jeu
        running = True

        previous_key_states = {}
        # Initialiser les touches enfoncées mais pas encore relâchées
        keys_pressed = set()

        while running:
            self.player.save_location()
            self.handle_input()
            self.update()

            #Position de la souris
            mouse_x, mous_y = pygame.mouse.get_pos()

            # Met à jour les positions des projectiles et vérifie les collisions avec les monstres
            for projectile in self.player.all_projectiles:
                projectile.move3(mouse_x, mous_y)
                for monster in self.map_manager.get_map().monsters:
                    monster_rect = self.map_manager.entity_position_and_rect(monster)[-1]
                    if monster_rect.colliderect(projectile.rect):
                        # Modifie la santé du monstre ou retire le projectile si une collision est détectée
                        monster.health -= projectile.damage
                        self.player.all_projectiles.remove(projectile)
                    
                # Supprime le projectile si hors range
                if (projectile.rect.x < (self.player.rect.x-projectile.max_range)
                    or projectile.rect.x > (self.player.rect.x+projectile.max_range)
                    or projectile.rect.y < (self.player.rect.y-projectile.max_range)
                    or projectile.rect.y > (self.player.rect.y+projectile.max_range)
                    ):
                    self.player.all_projectiles.remove(projectile)
                    
            # Mise à jour du cooldown de la boule de feu
            if self.player.cd > 0:
                self.player.cd -= 1

            #dessine map, plus rectangle collisison perso et la dialog box
            self.map_manager.draw()
            self.map_manager.draw_collisions()
            self.dialog_box.render(self.screen)   

            # Affichage des coordonnées du joueur à l'écran
            text_font = pygame.font.Font(None, 36)
            text = text_font.render(f"Player: {self.player.position}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))  # Affiche les coordonnées en haut à gauche
            
            # Dessiner la barre de sorts
            self.spell_bar.draw_spell_bar()
            self.spell_bar.select_spell(self.spell_use,self.player.cd)

            for monster in self.monsters:
                self.player.check_collision(monster)   

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.map_manager.check_npc_collisions(self.dialog_box)
                    elif event.key == pygame.K_a:
                        
                        previous_key_states[event.key] = event.key in keys_pressed
                        keys_pressed.add(event.key)
                    elif event.key == pygame.K_t:
                        previous_key_states[event.key] = event.key in keys_pressed
                        keys_pressed.add(event.key)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        previous_key_states[event.key] = event.key in keys_pressed
                        keys_pressed.remove(event.key)
                    elif event.key == pygame.K_t:
                        previous_key_states[event.key] = event.key in keys_pressed
                        keys_pressed.remove(event.key)

            if pygame.K_a in keys_pressed:
                self.map_manager.draw_spell_range(self.spell_properties["fireball"]["max_range"]) 
            if pygame.K_t in keys_pressed:
                self.map_manager.draw_spell_range(self.spell_properties["iceball"]["max_range"])

            # Vérifier si une touche a été relâchée
            for key, was_pressed in previous_key_states.items():
                if was_pressed and key not in keys_pressed:
                    # Lancer le sort approprié en fonction de la touche relâchée
                    if key == pygame.K_a:
                        self.spell_use = "fireball"
                    elif key == pygame.K_t:
                        self.spell_use = "iceball"
                    # Vérifier le cooldown avant de lancer le sort
                    if self.player.cd == 0:
                        self.player.shoot(self.orientation, self.map_manager)
                        # Définir le cooldown à 2 secondes (120 trames à 60 FPS)
                        self.player.cd = 80
                        previous_key_states
            previous_key_states.clear()
            
            # Réinitialiser l'écran
            pygame.display.flip()
            clock.tick(120)

        pygame.quit()

# Lancer le jeu
if __name__ == "__main__":
    game = Game()
    game.run()
