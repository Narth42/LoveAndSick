import pygame
import random

from plateforme import Plateforme
from settings import Settings

param = Settings()


class Generation(pygame.sprite.Group):
    def __init__(self, game):
        """
        Generation des plateformes
        :param game: Class du jeu
        """
        pygame.sprite.Group.__init__(self)
        self.histoire = game.histoire
        self.game = game

    def groupe(self, plateforme):
        """
        Fonction qui ajoute des entitees au groupe des plateformes
        :param plateforme: (list) plateforme a ajoute dans le groupe
        """
        for i in plateforme:
            self.add(i)

    def start_generation(self):
        """
        Generation des platfomres du debut
        """
        start_plateforme = [Plateforme(param.plateforme["start_plateforme"], self.histoire.get_level(), self.game, (i-1) * param.plateforme["base_plateforme_size"][0], 450, False) for i in range(12)]
        self.groupe(start_plateforme)

    def auto_generation(self):
        """
        Generation automatique des platfomres au cour du jeu
        """
        auto_plateforme = [Plateforme((random.randint(1, 10), 1), self.histoire.get_level(), self.game, param.game["taille_fenetre"][0] + ((i + 1) * param.game["taille_fenetre"][0] // 10), 450) for i in range(12)]
        self.groupe(auto_plateforme)

    def death_generation(self):
        """
        Generation des platfomres apres la mort
        """
        death_platform = [Plateforme(param.plateforme["start_plateforme"], self.histoire.get_level(), self.game, (i-1) * param.game["taille_fenetre"][0] // 10, 450, False) for i in range(12)]
        self.groupe(death_platform)

    def story_generation(self):
        """
        Generation des platfomres au moment de l'histoire
        """
        story_platform = [Plateforme(param.plateforme["start_plateforme"], self.histoire.get_level(), self.game, (i-1) * param.game["taille_fenetre"][0] // 10, 450, False) for i in range(12)]
        self.groupe(story_platform)


