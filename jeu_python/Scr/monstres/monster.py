import pygame
import os
from Spell.state import Etats

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

class Monster(pygame.sprite.Sprite):
    def __init__(self, type_monster, num_monster):
        super().__init__()
        self.type_monster = type_monster
        self.num_monster = num_monster
        self.position = [0, 0]
        self.attack = 10
        self.health = 100
        self.max_health = 100
        self.mana = 100
        self.max_mana = 100
        self.give_xp = 20
        self.animation_index = 0
        self.animation_delay = 2
        self.image = None
        self.rect = None
        self.feet = None
        self.mask = None
        self.mask_image = None
        self.old_position = self.position.copy()
        self.states = []
        self.states_properties = Etats()
        self.states_properties_copy =  Etats()
        self.repulsion_cooldown = 0
        self.repulsion_duration = 10
        self.repulsion_amount = 0
        self.repulsion = False
        self.repulsion_x = 0
        self.repulsion_y = 0
        

    def apply_state(self):
        current_time = pygame.time.get_ticks()
        for state in self.states[:]:
            if state in self.states_properties_copy.states:
                state_details = self.states_properties_copy.states[state]
                start = state_details["start_time"]
                duration = state_details["duration"]
                if current_time - start >= 1000:  # Vérifier si une seconde s'est écoulée
                    # Appliquer les dégâts par seconde
                    self.health -= state_details["damage_per_second"]
                    # Mettre à jour le temps de début de l'état pour le prochain cycle
                    state_details["start_time"] = current_time
                    # Décrémenter la durée restante
                    duration -= 1
                    if duration <= 0:  # Vérifier si la durée est écoulée
                        self.states.remove(state)
                    else:
                        state_details["duration"] = duration  # Mettre à jour la durée dans le dictionnaire

    def handle_state(self, state_name):
        if state_name is not None:
            # Vérifiez si le monstre a déjà cet état
            if state_name in self.states:
                return
            # Ajoutez l'état au monstre avec sa durée initiale
            state_details = self.states_properties.states[state_name].copy()
            state_details["start_time"] = pygame.time.get_ticks()  # Définir le temps de début
            self.states_properties_copy.states[state_name] = state_details 
            self.states.append(state_name)

    def update_state_times(self):
        current_time = pygame.time.get_ticks()
        for state in self.states_properties.states:
            self.states_properties.states[state]["start_time"] = current_time

    def load_points(self, tmx_data):
            point = tmx_data.get_object_by_name(f"{self.type_monster}_{self.num_monster}")
            return pygame.Rect(point.x, point.y, point.width, point.height)
        
    def update(self):
        self.rect.topleft = self.position
        if self.feet:  # Vérifier si self.feet est initialisé
            self.feet.midbottom = self.rect.midbottom
        
    def handle_periodic_damage(self, event):
        damage_per_second = event.damage_per_second
        # Appliquer des dégâts périodiques au monstre
        self.health -= damage_per_second
        # Vérifier si le monstre est mort
        if self.health <= 0:
            self.kill()

    def save_location(self):
        self.old_position = self.position.copy()

    def teleport_spawn(self, spawn_point):
        self.position[0] = spawn_point.x
        self.position[1] = spawn_point.y
        self.save_location()

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        if self.feet:  # Vérifier si self.feet est initialisé
            self.feet.midbottom = self.rect.midbottom

    def collisions_monster(self, walls, player):
        player_mask_offset_x = self.rect.x - player.rect.x
        player_mask_offset_y = self.rect.y - player.rect.y
        if player.mask.overlap(self.mask, (player_mask_offset_x, player_mask_offset_y)):
            self.repulsion = True
            self.repulsion_amount = 0

            diff_x = self.rect.centerx - player.rect.centerx
            diff_y = self.rect.centery - player.rect.centery

            # Répulsion du monstre
            if abs(diff_x) > abs(diff_y):
                if diff_x > 0:
                    self.repulsion_x = 15
                else:
                    self.repulsion_x = -15
                self.repulsion_y = 0
            else:
                self.repulsion_y = 0
                if diff_y > 0:
                    self.repulsion_y = 15
                else:
                    self.repulsion_y = -15
                self.repulsion_x = 0

        else:
            self.repulsion = False

        if self.repulsion:
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.repulsion = False
                    break

            if self.repulsion:
                distance_x = self.repulsion_x / 10
                distance_y = self.repulsion_y / 10

                current_time = pygame.time.get_ticks()
                if current_time - self.repulsion_cooldown > self.repulsion_duration:
                    if self.repulsion_amount < 10 and self.repulsion:
                        self.old_position[0] += distance_x
                        self.old_position[1] += distance_y
                        self.repulsion_amount += 1
                        self.repulsion_cooldown = current_time
                        self.move_back()

                    else:
                        self.repulsion = False
