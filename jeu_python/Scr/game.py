import pygame
from dialog import DialogBox
from map import MapManager
from player import Player
from spell_bar import SpellBar
import os


# répertoire du script actuel
current_directory = os.path.dirname(os.path.abspath(__file__))

# répertoire de travail pour inclure le dossier parent 
os.chdir(current_directory)
class Game:
    def __init__(self):
        # fenetre de jeux
        self.screen = pygame.display.set_mode((0,0), pygame.RESIZABLE)
        pygame.display.set_caption('Dream Land')
        # generer un joueur
        self.player = Player()
        self.all_projectiles = pygame.sprite.Group()
        self.map_manager = MapManager(self.screen, self.player)
        self.monsters = self.map_manager.get_map().monsters
        self.dialog_box = DialogBox()
       # self.spawn_monster()
        # Barre de sorts
        spell_icons = {
            "fireball": pygame.image.load("../sort/spell_bar/feu.PNG")
        }
        self.spell_bar = SpellBar(self.screen, spell_icons)


    def kill_monster(self):
        for monster in self.monsters:
            if monster.health <= 0:
                monster.remove()


    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_z]:
            self.player.move_up()
        elif pressed[pygame.K_s]:
            self.player.move_down()
        elif pressed[pygame.K_q]:
            self.player.move_left()
        elif pressed[pygame.K_d]:
            self.player.move_right()

    def update(self):
        self.map_manager.update()
         
        
    def run(self):

        clock = pygame.time.Clock()
        # boucle du jeu
        running = True

        while running:
            
            self.player.save_location()
            self.handle_input()
            self.update()
            # Mise à jour de la barre de sorts
            self.spell_bar.update()

            # Mise à jour du cooldown de la boule de feu
            if self.player.cd > 0:
                self.player.cd -= 1

            #dessine map, plus rectangle collisison perso et la dialog box
            self.map_manager.draw()
            self.dialog_box.render(self.screen)   

            # Affichage des coordonnées du joueur à l'écran
            text_font = pygame.font.Font(None, 36)
            text = text_font.render(f"Player: {self.player.position}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))  # Affiche les coordonnées en haut à gauche

            self.all_projectiles.draw(self.screen)
            for monster in self.monsters:
                self.player.check_collision(monster)

            # Réinitialiser l'écran
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_e:
                        self.map_manager.check_npc_collisions(self.dialog_box)
                        
                    elif pygame.key.get_pressed()[pygame.K_a]:
                        # Vérifie le cooldown avant de lancer une boule de feu
                        if self.player.cd == 0:
                            self.player.shoot()
                            for monster in self.monsters:
                                self.kill_monster()
                            # Défini le cooldown à 2 secondes (120 trames à 60 FPS)
                            self.player.cd = 120
                     
            clock.tick(70)

        pygame.quit()

