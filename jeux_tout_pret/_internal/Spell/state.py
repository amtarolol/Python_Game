import os 
import pygame

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

class Etats:
    def __init__(self):
        self.states = {
            "enflammé": {"start_time": 0, "duration": 2, "damage_per_second": 10},
            "empoisonné": {"start_time": 0, "duration": 2, "damage_per_second": 10}
        }
