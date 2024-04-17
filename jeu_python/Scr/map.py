import pygame, pytmx, pyscroll
from dataclasses import dataclass
from Player_pnj.player import NPC
from monstres.momy import Mommy
from monstres.slime import Slime
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
    monsters: list[Mommy]

class MapManager:

    def __init__(self, screen, player):
        # Générez les monstres et ajoutez-les à la liste des monstres
        
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "future_map_1"
        self.register_map(self.current_map, portals=[
            Portal(from_world=self.current_map, origin_point="map_suivante", target_world="map_2", teleport_point="spawn_map_suivante")
        ], npcs=[
            NPC("paul", nb_points=2, dialog=["Jeune aventurier tu est le bienvenue.","Bienvenue à 'Dream Land'.",
                                             "Prépare toi à affronter des monstres terribles."])
        ,], monsters=[
        Mommy(),
        *[Slime(random.randint(1, 5)) for _ in range(random.randint(1, 5))]  
        ])
        self.register_map("map_2", portals=[
            Portal(from_world="map_2", origin_point="go_map_1", target_world="future_map_1", teleport_point="spawn_map_1" ),
            Portal(from_world="map_2", origin_point="enter_house", target_world="house",
                   teleport_point="spawn_house_2")
        ])
        self.register_map("house", portals=[
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

        # collisions
        for sprite in self.get_group().sprites():
            if type(sprite) is (NPC):
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 0.5
            if type(sprite) is not (Mommy):            
                if sprite.feet.collidelist(self.get_walls()) > -1:
                    sprite.move_back()
            
    def register_map(self, name, portals=[], npcs=[], monsters=[]):
        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame(f'../map/{name}.tmx')
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

        for monster in monsters:
            group.add(monster)
        
        for monster in monsters:
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

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)
        self.draw_health_bar(self.player)
        for monster in self.get_map().monsters:
            if monster.health > 0:
                self.draw_health_bar(monster)

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
        health_ratio = entity.health / entity.max_health
        bar_length = int(bar_width * health_ratio)
        bar_length_max = int(bar_width * (entity.max_health / entity.max_health))
        # Dessine la barre de vie
        pygame.draw.rect(self.screen, (0, 0, 0), (bar_x, bar_y, bar_length_max, bar_height))
        pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, bar_length, bar_height))

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
        # Liste temporaire pour stocker les monstres morts
        dead_monsters = []
        
        for monster in self.get_map().monsters:
            if monster.health <= 0:
                # Ajoutez d'abord les monstres morts à la liste
                dead_monsters.append(monster)
            else:
                # Mettez à jour et animez les monstres vivants
                self.draw_health_bar(monster)
                monster.collisions_monster(self.get_walls(), self.player)
                monster.animate()

        for monster in dead_monsters:
            self.get_group().remove(monster)
            # Supprimez également le monstre de la liste des monstres de la carte
            self.get_map().monsters.remove(monster)

        for npc in self.get_map().npcs:
            npc.move()
