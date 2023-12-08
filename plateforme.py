import pygame
import random

from settings import Settings

param = Settings()


class Plateforme(pygame.sprite.Sprite):
    def __init__(self, item_identity, level, game, x=0, y=0, auto=True):
        """
        Groupe des plateformes.
        :param item_identity: (tuple) id de l'entitee
        :param level: (int) Level de la partie
        :param game: Class du jeu
        :param x: (float) position de la platforme en x
        :param y: (float) position de la platforme en y
        """
        super(Plateforme, self).__init__()

        self.game = game
        self.level = level

        # Specification de la plateforme
        if auto:
            if item_identity[0] <= 6 - self.level:
                self.item = (1, item_identity[1])
            else:
                self.item = (2, item_identity[1])
        else:
            self.item = item_identity

        # Definition des paramettres de la plateforme en fonction de leur id
        if self.item[0] == param.plateforme["start_plateforme"][0] and self.item[1] == param.plateforme["start_plateforme"][1]:
            self.image = pygame.image.load(param.images['plateforme' + str(self.level)]).convert_alpha()
            self.image = pygame.transform.scale(self.image, param.plateforme["base_plateforme_size"])
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        elif self.item[0] == param.plateforme["base_plateforme"][0] and self.item[1] == param.plateforme["base_plateforme"][1]:
            taille = random.randint(0, 10)
            self.image = pygame.image.load(param.images['plateforme' + str(self.level)]).convert_alpha()
            self.image = pygame.transform.scale(self.image, param.plateforme["base_plateforme_size"])
            self.rect = self.image.get_rect()
            self.rect.x = x - 10
            if taille < 2:
                self.rect.y = y + 50
            else:
                self.rect.y = y

        elif self.item[0] == param.plateforme["base_fly_plateforme"][0] and self.item[1] == param.plateforme["base_fly_plateforme"][1]:
            self.image = pygame.image.load(param.images['flyplateforme' + str(self.level)]).convert_alpha()
            self.image = pygame.transform.scale(self.image, param.plateforme["fly_plateforme_size"])
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        else:
            move = random.randint(0, 15)
            casse = random.randint(0, 10)
            ice = random.randint(0, 15)

            if self.level >= 2 and move < self.level - 1:
                self.item = param.plateforme["move_splateforme"]
                self.image = pygame.image.load(param.images['flyplateforme' + str(self.level)]).convert_alpha()
            elif casse < self.level:
                self.item = param.plateforme["break_plateforme"]
                self.image = pygame.image.load(param.images['breakplateforme' + str(self.level)]).convert_alpha()
            elif self.level >= 4 and ice < self.level - 1:
                self.item = param.plateforme["ice_plateforme"]
                self.image = pygame.image.load(param.images['iceplateforme']).convert_alpha()
            else:
                self.item = param.plateforme["fly_plateforme"]
                self.image = pygame.image.load(param.images['flyplateforme' + str(self.level)]).convert_alpha()

            self.image = self.image = pygame.transform.scale(self.image, param.plateforme["fly_plateforme_size"])
            self.rect = self.image.get_rect()
            self.rect.x = x + 15
            self.rect.y = y + random.randrange(-60, 60, 10)

        self.breaklevel = 0

        # Definition de la direction de mouvement des plateformes mouvantes
        if random.randint(0, 1) == 1:
            self.up = True
            self.down = False
        else:
            self.up = False
            self.down = True

        self.move_speed = random.randint(1, 2)

        # Generation des decorations
        if random.randint(1, 2) == 1 and self.item[0] == param.plateforme["base_plateforme"][0]:
            self.game.deco.generation(self.rect)
        elif random.randint(1, 40 - self.level * 2) == 1 and self.level >= 2 and self.item != param.plateforme["move_splateforme"]:
            self.game.enemy_group.bakubaku_generation(self.rect.x, self.rect.y, self.rect)
        elif random.randint(1, 50) == 1 and self.item != param.plateforme["move_splateforme"]:
            boost = random.randint(1, 10)
            if boost <= 5:
                self.game.boost_group.speed_generation(self.rect)
            elif boost <= 8:
                self.game.boost_group.jump_generation(self.rect)
            else:
                self.game.boost_group.vie_generation(self.rect)

    def update(self, player):
        """
        Met a jour la plateforme
        :param player: Class joueur
        """
        self.rect.x -= player.speed + player.speed_boost

        # Suppression de la plateforme
        if self.item[0] == param.plateforme["base_fly_plateforme"][0]:
            if self.rect.x < - self.rect.width - 15:
                self.remove()
        elif self.rect.x < - self.rect.width:
            self.remove()

    def move(self, player, bottom_collision):
        """
        Fait bouger les plateformes volante
        :param player: class joueur
        :param bottom_collision: (bool) collision entre le bas du joueur et le haut d'une plateforme
        """
        if self.item[1] == param.plateforme["move_splateforme"][1]:
            # Mouvement de la plateforme en y si plateforme mouvante
            if  self.rect.y >= param.game["taille_fenetre"][1] - 200:
                self.up = True
                self.down = False
            elif self.rect.y <= 200:
                self.up = False
                self.down = True

            if self.up:
                self.rect.y -= self.move_speed
            elif self.down:
                self.rect.y += self.move_speed

            # Collision de la plateforme avec le joueur
            if self.rect.colliderect(player.rect) and bottom_collision:
                # Met le joueur au meme niveau que la plateforme quand elle bouge
                player.rect.y = self.rect.y - player.rect.height

    def casse(self, player):
        """
        Regarde et detruit les plateformes destructibles
        :param player: Position du joueur
        """
        if self.item[1] == param.plateforme["break_plateforme"][1] and self.rect.colliderect(player):
            self.breaklevel += 1
        if self.breaklevel >= 25 - self.level * 3:
            self.remove()

    def glace(self, player):
        """
        Met un effet glissant au joueur quand il marche sur une plateforme glissante
        :param player: Position du joueur
        """
        if self.item[1] == param.plateforme["ice_plateforme"][1] and self.rect.colliderect(player):
            player.x += self.move_speed + self.level

    def remove(self):
        """
        Suppression de la plateforme
        """
        self.kill()
