import pygame, pytmx, pyscroll
from dataclasses import dataclass
from Player_pnj.player import NPC
from monstres.momy import Mommy
from monstres.slime import Slime
from monstres.rabbit import Rabbit
import random
import os

# répertoire du script actuel
current_directory = os.path.dirname(os.path.abspath(__file__))

# répertoire de travail pour inclure le dossier parent
os.chdir(current_directory)

@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str

@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]
    monsters: list[Mommy, Slime, Rabbit]

@dataclass
class MonsterConfig:
    monster_type: type
    args: list
    kwargs: dict

class MapManager:

    def __init__(self, screen, player):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.initial_monster_config = {
            "future_map_1": [
                MonsterConfig(Rabbit, [3, 5, 1, 5], {}),
                MonsterConfig(Slime, [1, 5, 1, 5], {})
            ]
        }



        self.current_map = "future_map_1"
        self.map1 = self.register_map(self.current_map, portals=[
                Portal(from_world=self.current_map, origin_point="map_suivante", target_world="map_2", teleport_point="map2")
                ], npcs=[
                NPC("paul", nb_points=2, dialog=["Jeune aventurier tu est le bienvenue.","Bienvenue à 'Dream Land'.",
                                                "Prépare toi à affronter des monstres terribles."])
                ,], monsters=[
                *[Rabbit(random.randint(1, 5)) for _ in range(random.randint(3, 5))],
                *[Slime(random.randint(1, 5)) for _ in range(random.randint(1, 5))]  
                ])
        
        self.map2 = self.register_map("map_2", portals=[
                Portal(from_world="map_2", origin_point="go_map_1", target_world="future_map_1", teleport_point="map1" ),
                Portal(from_world="map_2", origin_point="enter_house", target_world="house",
                    teleport_point="spawn_house_2")
                ])
        
        self.map3 = self.register_map("house", portals=[
            Portal(from_world="house", origin_point="exit_house_2", target_world="map_2", teleport_point="enter_house_exit" )
        ])

        self.teleport_player("player")
        self.teleport_npcs()
        self.teleport_monsters()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def check_npc_collisions(self, dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                dialog_box.execute(sprite.dialog)

    def check_collisions(self):
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)
                    self.teleport_monsters2()
                    

        # collisions
        for sprite in self.get_group().sprites():
            if type(sprite) is (NPC):
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 0.5        
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()
            
    def register_map(self, name, portals=[], npcs=[], monsters=[]):
        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame(f'ressources/map/{name}.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        
        # liste qui stocke les rectangles de collisions
        walls = []

        for npc in npcs:
            walls.append(npc.rect)

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessine le groupe de calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)
        group.add(self.player)

        for npc in npcs:
            group.add(npc)

        # Ajouter les monstres à la carte
        for monster in monsters:
            group.add(monster)
            if monster.health <= 0:
                group.remove(monster)
        
        for projectile in self.player.all_projectiles:
            group.add(projectile)
        #créé objet map
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs, monsters)

    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def entity_position_and_rect(self, entity):
        # Récupérer les coordonnées de l'entité sur la carte
        entity_map_position = entity.position
        # Récupérer les coordonnées du rectangle de collision de l'entité sur la carte
        entity_map_rect = entity.rect
        # Récupérer la position de la caméra par rapport à la carte
        camera_map_position = self.get_group().view.topleft  # Récupérer le coin supérieur gauche de la caméra
        # Calculer la position de l'entité sur l'écran
        entity_screen_x = entity_map_position[0] - camera_map_position[0]
        entity_screen_y = entity_map_position[1] - camera_map_position[1]
        # Calculer le rectangle de collision de l'entité sur l'écran
        entity_screen_rect = entity_map_rect.move(-camera_map_position[0], -camera_map_position[1])
        # Retourner les coordonnées de l'entité sur l'écran et son rectangle de collision
        return entity_screen_x, entity_screen_y, entity_screen_rect
    
    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def teleport_monsters(self):
        for map in self.maps:
            map_data = self.maps[map]
            monsters = map_data.monsters
            for monster in monsters:
                spawn_point_monster = monster.load_points(map_data.tmx_data)
                monster.teleport_spawn(spawn_point_monster)

    def teleport_monsters2(self):
        # Obtenir la carte actuelle
        current_map_data = self.get_map()

        # Effacer tous les monstres actuels de la carte spécifique
        for monster in current_map_data.monsters:
            current_map_data.group.remove(monster)
        current_map_data.monsters.clear()

        # Réinitialiser les monstres en fonction de la carte actuelle
        initial_monsters_config = self.initial_monster_config.get(current_map_data.name, [])

        for config in initial_monsters_config:
            num_monsters = random.randint(config.args[0], config.args[1])
            # Créer et ajouter chaque monstre à la carte
            for _ in range(num_monsters):
                new_monster = config.monster_type(random.randint(config.args[2], config.args[3]))
                # Sélectionner un point d'apparition différent pour chaque slime
                spawn_point_new_monster = new_monster.load_points(current_map_data.tmx_data)
                new_monster.teleport_spawn(spawn_point_new_monster)
                current_map_data.group.add(new_monster)
                current_map_data.monsters.append(new_monster)

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)
        self.draw_health_bar(self.player)
        self.draw_mana_bar(self.player)
        self.draw_xp_bar()
        for monster in self.get_map().monsters:
            if monster.health > 0:
                self.draw_health_bar(monster)
                self.draw_mana_bar(monster)

        for projectile in self.player.all_projectiles:
            projectile.rect.x = projectile.position[0]
            projectile.rect.y = projectile.position[1]
            projectile.animate() 
            self.screen.blit(projectile.image, projectile.rect)

    def draw_health_bar(self, entity):
        # Calcule la position de la barre de vie
        entity_rect = self.entity_position_and_rect(entity)[-1]
        bar_width = entity_rect.width
        bar_height = 5
        bar_x = entity_rect.x
        bar_y = entity_rect.y - bar_height - 7
        # Calcule la longueur de la barre de vie en fonction de la santé de l'entité
        health_ratio = (entity.health / entity.max_health)
        bar_length = int(bar_width * health_ratio)
        bar_length_max = int(bar_width * (entity.max_health / entity.max_health))
        # Dessine la barre de vie
        pygame.draw.rect(self.screen, (0, 0, 0), (bar_x, bar_y, bar_length_max, bar_height))
        pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, bar_length, bar_height))

    def draw_mana_bar(self, entity):
        if entity.mana and entity.max_mana:
            # Calcule la position de la barre de mana
            entity_rect = self.entity_position_and_rect(entity)[-1]
            bar_width = entity_rect.width
            bar_height = 5
            bar_x = entity_rect.x
            bar_y = entity_rect.y - bar_height - 3
            # Calcule la longueur de la barre de vie en fonction de la santé de l'entité
            mana_ration = (entity.mana / entity.max_mana)
            bar_length = int(bar_width * mana_ration)
            bar_length_max = int(bar_width * (entity.max_mana / entity.max_mana))
            # Dessine la barre de vie
            pygame.draw.rect(self.screen, (0, 0, 0), (bar_x, bar_y, bar_length_max, bar_height))
            pygame.draw.rect(self.screen, (0, 0, 255), (bar_x, bar_y, bar_length, bar_height))
        else:
            pass

    def draw_xp_bar(self):
        bar_width = 100
        bar_height = 8
        bar_x = 500
        bar_y = 10
        # Calcule la longueur de la barre de vie en fonction de la santé de l'entité
        xp_ration = (self.player.xp / self.player.max_xp )
        bar_length = int(bar_width * xp_ration)
        bar_length_max = int(bar_width * (self.player.max_xp / self.player.max_xp))
        # Dessine la barre de vie
        pygame.draw.rect(self.screen, (0, 0, 0), (bar_x, bar_y, bar_length_max, bar_height))
        pygame.draw.rect(self.screen, (255, 0, 0), (bar_x, bar_y, bar_length, bar_height))

    ########################################################################################
    ###########################    DEBUG VISUEL     ########################################
    ########################################################################################

    def draw_collisions(self):
        for monster in self.get_map().monsters:
            monster_rect = self.entity_position_and_rect(monster)[-1]
            pygame.draw.rect(self.screen, (0, 255, 0), monster_rect, 2)

        for wall in self.get_walls():
            pygame.draw.rect(self.screen, (0, 0, 255), wall, 2)

    def draw_spell_range(self, max_range):
        player_rect = self.entity_position_and_rect(self.player)[-1]
        max_range = max_range
        player_center_x = player_rect.x + player_rect.width / 2
        player_center_y =player_rect.y + player_rect.height / 2
        pygame.draw.circle(self.screen, (255, 0, 0), (int(player_center_x), int(player_center_y)), max_range, 1)
    
    ########################################################################################
    ###########################    DEBUG VISUEL     ########################################
    ########################################################################################


    def update(self):
        self.get_group().update()
        self.check_collisions()

        player_x, player_y = self.entity_position_and_rect(self.player)[:2]
        for projectile in self.player.all_projectiles:      
            # Supprime le projectile s'il est hors de portée
            if (projectile.rect.center[0] < (player_x - projectile.max_range)
                or projectile.rect.center[0] > (player_x + projectile.max_range)
                or projectile.rect.center[1] < (player_y - projectile.max_range)
                or projectile.rect.center[1] > (player_y + projectile.max_range)
                ):
                self.player.all_projectiles.remove(projectile)
                
        # Liste temporaire pour stocker les monstres morts
        dead_monsters = []
        for monster in self.get_map().monsters:
            self.player.check_collision(monster, self.get_walls())
            if monster.health <= 0:
                # Ajouter les monstres morts à la liste temporaire
                dead_monsters.append(monster)
                self.player.xp += monster.give_xp
            else:
                monster.animate(self.get_walls(), self.player)            

        # Supprimer les monstres morts du groupe de sprites
        for monster in dead_monsters:
            self.get_group().remove(monster)
            self.get_map().monsters.remove(monster)

        for npc in self.get_map().npcs:
            npc.move()
