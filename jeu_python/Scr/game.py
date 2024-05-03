import pygame
from dialog import DialogBox
from map import MapManager
from Player_pnj.player import Player
from Spell.spell_bar import SpellBar
from Spell.state import Etats
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

class Game:
    def __init__(self):
        # initialisation de pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        # fenetre de jeux
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.SRCALPHA)
        pygame.display.set_caption('Dream Land')
        # generer un joueur
        self.player = Player()
        self.all_projectiles = pygame.sprite.Group()
        self.etats = Etats()
        self.map_manager = MapManager(self.screen, self.player)
        self.monsters = self.map_manager.get_map().monsters
        self.dialog_box = DialogBox()
        self.spell_use = set() 

        # Spell properties
        self.spell_properties = {
            "fireball": {"icon": pygame.image.load("ressources/sort/spell_bar/feu.PNG"), "max_range": 300,
                         "cd": 0, "wait_cd": 250 * self.player.cdr},
            "iceball": {"icon": pygame.image.load("ressources/sort/spell_bar/glace.JPG"), "max_range": 500,
                        "cd": 0, "wait_cd": 80 * self.player.cdr},
            "lave": {"icon": pygame.image.load("ressources/sort/spell_bar/lave.JPG"), "max_range": 800,
                     "cd": 0, "wait_cd": 20 * self.player.cdr}
        }
        spell_icons = {spell_name: properties["icon"] for spell_name, properties in self.spell_properties.items()}
        self.spell_bar = SpellBar(self.screen, spell_icons)

    def handle_input(self):
        # Réinitialiser les touches enfoncées lors de chaque itération
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_z]:
            if self.player.repulsion == False:
                self.player.move_up()
        elif keys_pressed[pygame.K_s]:
            if self.player.repulsion == False:
                self.player.move_down()
        elif keys_pressed[pygame.K_q]:
            if self.player.repulsion == False:
                self.player.move_left()
        elif keys_pressed[pygame.K_d]:
            if self.player.repulsion == False:
                self.player.move_right()

    def update(self):
        self.map_manager.update()
    
    def run(self):
        clock = pygame.time.Clock()
        bullet = pygame.Surface((10, 10))
        bullet.fill((255, 0, 0))
        col = (0, 255, 0)

        # boucle du jeu
        running = True

        while running:
            
            self.player.save_location()
            self.handle_input()
            self.update()
            pos = pygame.mouse.get_pos()
            self.player.level_up()
            
            for monster in self.map_manager.get_map().monsters:
                monster.apply_state()        

            # Boucle sur les projectiles du joueur
            for projectile in self.player.all_projectiles:
                projectile.move(mouse_x, mouse_y)

                # Vérifier les collisions avec les monstres
                for monster in self.map_manager.get_map().monsters:
                    monster.update_state_times()
                    monster_rect = self.map_manager.entity_position_and_rect(monster)[-1]
                    monster_rect_x, monster_rect_y = self.map_manager.entity_position_and_rect(monster)[:2]
                    # Vérifier la collision avec les masques de collision
                    if monster.mask.overlap(projectile.mask, (projectile.rect.x - monster_rect_x, projectile.rect.y - monster_rect_y)):
                        # Ajouter la logique de collision ici
                        monster.handle_state(projectile.state)
                        monster.health -= projectile.damage

                        if projectile.projectile_type != "Explosion":
                            self.player.all_projectiles.remove(projectile)


            # Dessiner la carte, les collisions et la boîte de dialogue
            self.map_manager.draw()
            self.map_manager.draw_collisions()

            self.dialog_box.render(self.screen)

            # Affichage des coordonnées du joueur à l'écran
            text_font = pygame.font.Font(None, 36)
            text = text_font.render(f"Player: {self.player.position}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))  # Affiche les coordonnées en haut à gauche

                        # Affichage des coordonnées du joueur à l'écran
            text_lvl = pygame.font.Font(None, 36)
            lvl = text_lvl.render(f"Player: {self.player.level}", True, (255, 255, 255))
            self.screen.blit(lvl, (10, 50))  # Affiche les coordonnées en haut à gauche

            # Dessiner la barre de sorts
            self.spell_bar.draw_spell_bar()
            for spell in self.spell_use:
                self.spell_bar.select_spell(spell, self.spell_properties[spell]["cd"])
            
            for spell, properties in self.spell_properties.items():
                if properties["cd"] != 0:
                    properties["cd"] -= 1


            # Dessiner la surface bullet au-dessus de tout
            bullet.fill(col)
            self.screen.blit(bullet, pos)

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.map_manager.check_npc_collisions(self.dialog_box)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        if self.spell_properties["fireball"]["cd"] == 0:
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            self.spell_use.add("fireball")
                            # Supprimer le plus ancien s'il est en double
                            if len(self.spell_use) > 1:
                                self.spell_use.remove(next(iter(self.spell_use)))
                            self.player.use_spell("fire_ball", self.map_manager)
                            # Définir le cooldown à 2 secondes (120 trames à 60 FPS)
                            self.spell_properties["fireball"]["cd"] = self.spell_properties["fireball"]["wait_cd"]
                    if event.key == pygame.K_t:
                        if self.spell_properties["lave"]["cd"] == 0:
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            # Supprimer le plus ancien s'il est en double
                            if len(self.spell_use) > 1:
                                self.spell_use.remove(next(iter(self.spell_use)))
                            self.spell_use.add("lave")
                            self.player.use_spell("explosion", self.map_manager)
                            self.spell_properties["lave"]["cd"] = self.spell_properties["lave"]["wait_cd"]

            # Dessiner la portée des sorts si les touches appropriées sont enfoncées
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_a]:
                self.map_manager.draw_spell_range(self.spell_properties["fireball"]["max_range"])
            if keys_pressed[pygame.K_t]:
                self.map_manager.draw_spell_range(self.spell_properties["lave"]["max_range"])

            # Dessiner les rectangles de collision des projectiles du joueur
            for projectile in self.player.all_projectiles:
                pygame.draw.rect(self.screen, (200, 0, 0), projectile.rect, 1)

            # Réinitialiser l'écran
            pygame.display.flip()
            clock.tick(120)

        pygame.quit()

# Lancer le jeu
if __name__ == "__main__":
    game = Game()
    game.run()
