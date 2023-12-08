import pygame
import random

from settings import Settings

param = Settings()


class DecoGroup(pygame.sprite.Group):
    def __init__(self, game):
        """
        Group des elements de decoration
        :param game: Class du jeu
        """
        pygame.sprite.Group.__init__(self)
        self.game = game

    def add_element(self, element):
        """
        Ajoute un element au group
        :param element: (Sprite) element a ajouter
        """
        self.add(element)

    def generation(self, plateforme_rect):
        """
        Cree un nouveau Sprite
        :param plateforme_rect: coordonnee de la plateforme ou mettre la decoration
        """
        element = Deco(plateforme_rect)
        self.add_element(element)


class Deco(pygame.sprite.Sprite):
    def __init__(self, plateforme_rect):
        """
        Class des elements de decoration
        :param plateforme_rect: coordonnee de la plateforme ou mettre la decoration
        """
        super(Deco, self).__init__()

        # Choix alleatoire de la decoration
        rand = random.randint(1, 200)
        if rand <= 40:
            img = '1'
        elif rand <= 63:
            img = '2'
        elif rand <= 112:
            img = '3'
        elif rand <= 120:
            img = '4'
        elif rand <= 140:
            img = '5'
        elif rand <= 170:
            img = '6'
        else:
            img = '7'

        self.image = pygame.image.load(param.images['deco' + img]).convert_alpha()

        if int(img) > 4:
            self.image = pygame.transform.scale(self.image, (200, 80))
        else:
            self.image = pygame.transform.scale(self.image, (80, 80))

        self.rect = self.image.get_rect()
        self.rect.x = plateforme_rect.x + (plateforme_rect.w - self.rect.w) // 2

        if int(img) > 4:
            self.rect.y = plateforme_rect.y - self.rect.h - random.randint(250, 300)
        else:
            self.rect.y = plateforme_rect.y - self.rect.h

    def update(self, player):
        """
        Met a jour l'element de decoration
        :param player: Class joueur
        """
        self.rect.x -= player.speed + player.speed_boost

        if self.rect.x < - self.rect.width:
            self.remove()

    def remove(self):
        """
        Suppression de l'element de decoration
        """
        self.kill()
