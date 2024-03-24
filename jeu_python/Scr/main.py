import pygame
from ecran_accueil import EcranAccueil
from game import Game

if __name__ == '__main__':
    pygame.init()

    # Créer une surface pour l'écran du jeu
    screen = pygame.display.set_mode((0,0), pygame.RESIZABLE | pygame.SRCALPHA)

    # Afficher l'écran d'accueil
    ecran_accueil = EcranAccueil(screen)
    ecran_accueil.run()

    # Initialiser le jeu après la fermeture de l'écran d'accueil
    game = Game()
    game.run()
