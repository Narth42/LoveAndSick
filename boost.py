import pygame
import random

from settings import Settings

param = Settings()


class Boost_group(pygame.sprite.Group):
    def __init__(self, game):
        """
        Group des boosts
        :param game: Class du jeu
        """
        pygame.sprite.Group.__init__(self)
        self.game = game
        self.effect_time = 0
        self.speed_effect = False
        self.jump_effect = False

    def group(self, boost):
        """
        Fonction qui ajoute des boosts au groupe des boosts
        :param boost: (list) boost a ajoute dans le groupe
        """
        for i in boost:
            self.add(i)

    def vie_generation(self, rect):
        """
        Generation d'un boost de vie
        """
        vie = [Vie(self.game, rect)]
        self.group(vie)

    def speed_generation(self, rect):
        """
        Generation d'un boost de vitesse
        """
        speed = [Speed(self.game, rect)]
        self.group(speed)

    def jump_generation(self, rect):
        """
        Generation d'un boost de saut
        """
        jump = [Jump(self.game, rect)]
        self.group(jump)

    def boost_effect(self, player):
        """
        Effet des boosts
        :param player: Class joueur
        """
        # Boost de vitesse
        if self.speed_effect and self.effect_time > 0:
            player.set_speed_boost(3)
            self.effect_time -= 1
        else:
            player.set_speed_boost(0)
            self.speed_effect = False

        # Boost de saut
        if self.jump_effect and self.effect_time > 0:
            player.set_jump_boost(2)
            self.effect_time -= 1
        else:
            player.set_jump_boost(0)
            self.jump_effect = False


class Boost(pygame.sprite.Sprite):

    def __init__(self, game, name, rect):
        """
        Class des boosts
        :param game: Class du jeu
        :param name: (str) Nom du boost
        :param rect: dimension d'une entitee
        """
        super(Boost, self).__init__()
        self.game = game
        self.name = name
        self.image = pygame.image.load(param.images[self.name]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = rect.x + (rect.w - self.rect.w) // 2
        self.rect.y = rect.y - self.rect.h

    def move(self):
        """
        Mouvement du boost
        """
        self.rect.x -= self.game.player.speed + self.game.player.speed_boost

    def update(self, player):
        """
        Met a jour du boost
        :param player: Class joueur
        """
        if self.rect.x <= -self.rect.w:
            self.remove()

        self.collision(player)

        # Deplacement du boosts
        self.move()

    def collision(self, player):
        """
        Collission avec le joueur
        :param player: Class joueur
        """
        if self.rect.colliderect(player.rect):
            if self.name == "vie":
                player.health += 1
                self.game.histoire.game_score += 2
            elif self.name == "speed":
                self.game.boost_group.effect_time = random.randint(500, 1000)
                self.game.boost_group.jump_effect = False
                self.game.boost_group.speed_effect = True
                self.game.histoire.game_score += 4
            elif self.name == "jump":
                self.game.boost_group.effect_time = random.randint(500, 1000)
                self.game.boost_group.speed_effect = False
                self.game.boost_group.jump_effect = True
                self.game.histoire.game_score += 4
            self.remove()

    def remove(self):
        """
        Supression du boost
        """
        self.kill()

    def group_collision(self, group):
        """
        Collision du boost avec un group
        :param group: group avec lequel verifier la collision
        :return: True ou False en fonction de si il y a collision
        """
        if pygame.sprite.spritecollide(self, group, False):
            return True
        else:
            return False


class Vie(Boost):
    def __init__(self, game, rect):
        """
        Class des slimes
        :param game: Class du jeu
        :param rect: dimension d'une entitee
        """
        super(Vie, self).__init__(game, "vie", rect)


class Speed(Boost):
    def __init__(self, game, rect):
        """
        Class des slimes
        :param game: Class du jeu
        :param rect: dimension d'une entitee
        """
        super(Speed, self).__init__(game, "speed", rect)


class Jump(Boost):
    def __init__(self, game, rect):
        """
        Class des slimes
        :param game: Class du jeu
        :param rect: dimension d'une entitee
        """
        super(Jump, self).__init__(game, "jump", rect)
