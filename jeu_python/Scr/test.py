import pygame
import pytmx
import os

# Initialiser Pygame
pygame.init()

# Définir le mode vidéo
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.SRCALPHA)

# Chemin du fichier TMX
tmx_file_path = "c:\\Users\\bauch\\Documents\\cours\\projets_git\\Python_Game\\jeu_python\\map\\test_minimap.tmx"

# Créer une instance de pytmx.TiledMap en passant le chemin du fichier TMX
tile_map = pytmx.TiledMap(tmx_file_path)

# Boucle principale du jeu
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Effacer l'écran
    screen.fill((0, 0, 0))

    # Dessiner les tuiles de chaque couche visible
    for layer in tile_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile_info = tile_map.get_tile_image_by_gid(gid)
                if tile_info:
                    tile_image = tile_info[0]  # Récupérer l'image de la tuile
                    screen.blit(tile_image, (x * tile_map.tilewidth, y * tile_map.tileheight))

    # Rafraîchir l'écran
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
