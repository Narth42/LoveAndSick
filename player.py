import pygame
import animation

from settings import Settings
from projectile import Projectile

param = Settings()


class Player(animation.AnimateSprite):
    def __init__(self, game):
        """
        Generation du joueur
        :param game: Class du jeu
        """
        super(Player, self).__init__(self, 'player', param.player["size"])
        self.game = game
        self.save = game.save.get_save()

        self.health = self.save["vie"]

        # Image
        self.rect = self.image.get_rect()
        self.rect.x = self.image.get_rect().w + 400
        self.rect.y = param.game["taille_fenetre"][1] - 500

        # Mouvement
        self.speed_boost = 0
        self.speed = param.player["speed"]
        self.direction = 1

        # Saut
        self.jump_boost = 0
        self.saut = 0
        self.saut_up = 0
        self.saut_down = 5
        self.a_sauter = False

        # Invincibilite
        self.invincible = False
        self.invincible_time = 0

        # Projectile
        self.projectiles = pygame.sprite.Group()
        self.a_tirer = False
        self.shoot_speed = param.player["shoot_speed"]
        self.shoot_time = 0

    '''Update'''

    def update(self):
        """
        Mise a jour du joueur
        """
        if self.a_tirer and self.shoot_time > 0:
            self.shoot_time -= 1
        else:
            self.shoot_time = self.shoot_speed
            self.a_tirer = False

    def update_animation(self):
        """
        Mise a jour des animation du joueur
        """
        if not self.a_sauter:
            self.animate()
        else:
            self.player_jump()

    '''Mouvement'''

    def move(self, direction):
        """
        Mouvement du joueur a droite et a gauche
        :param direction: (int) direction du joueur
        """
        self.direction = direction
        self.rect.x += (self.speed + self.speed_boost) * self.direction

    def jump(self):
        """
        Fait sauter le joueur
        """
        if self.a_sauter:
            if self.saut_up >= param.player['jump'] + self.jump_boost:
                self.saut_down -= 1
                self.saut = self.saut_down
            else:
                self.saut_up += 0.5
                self.saut = self.saut_up

            if self.saut_down < 0:
                self.saut_up = 0
                self.saut_down = 5
                self.a_sauter = False

        self.rect.y = self.rect.y - (10 * (self.saut / 2))

    def set_speed_boost(self, speed_boost):
        """
        Met a jour la variable speed_boost
        :param speed_boost: (int) nouvelle valeur du speed_boost
        """
        self.speed_boost = speed_boost

    def set_jump_boost(self, jump_boost):
        """
        Met a jour la variable jump_boost
        :param jump_boost: (int) nouvelle valeur du jump_boost
        """
        self.jump_boost = jump_boost

    '''Collisions'''

    def general_collide(self, group):
        """
        Verification des collisions
        :param group: groupe de sprite
        :return: True si il y a collision
        """
        if pygame.sprite.spritecollide(self, group, False):
            return True
        else:
            return False

    def bottom_collide(self, entity):
        """
        Verification des collisions en bas du joueur
        :param entity: entite
        :return: True si il y a collision
        """
        if entity.rect.top - 10 <= self.rect.bottom <= entity.rect.top + 10 and self.rect.colliderect(entity.rect):
            return True
        else:
            return False

    def top_collide(self, entity):
        """
        Verification des collisions en haut du joueur
        :param entity: entite
        :return: True si il y a collision
        """
        if entity.rect.bottom - 10 <= self.rect.top <= entity.rect.bottom + 10 and self.rect.colliderect(entity.rect):
            return True
        else:
            return False

    def right_collide(self, entity):
        """
        Verification des collisions a droite du joueur
        :param entity: entite
        :return: True si il y a collision
        """
        if entity.rect.left - 10 <= self.rect.right <= entity.rect.left + 10 and self.rect.bottom // 10 * 10 != entity.rect.top // 10 * 10 and self.rect.colliderect(entity.rect):
            return True
        else:
            return False

    def left_collide(self, entity):
        """
        Verification des collisions a gauche du joueur
        :param entity: entite
        :return: True si il y a collision
        """
        if entity.rect.right - 10 <= self.rect.left <= entity.rect.right + 10 and self.rect.bottom // 10 * 10 != entity.rect.top // 10 * 10 and self.rect.colliderect(entity.rect):
            return True
        else:
            return False

    '''Attack'''

    def attaque(self):
        """
        Fait attaquer le joueur
        """
        if self.game.histoire.get_level() >= 2 and not self.a_tirer:
            if self.direction == 1:
                x = self.rect.x + param.player["image_player_shoot_size"][0]
            else:
                x = self.rect.x
            self.projectiles.add(Projectile(x, self.rect.y + 30, self.direction, param.player["weapon"][0], param.player["weapon"][1], param.player["weapon"][2]))
            self.a_tirer = True
            self.player_shoot()
            self.game.sound_canal.play(self.game.shoot_sound)

    '''Other'''

    def starting_point(self):
        """
        Remet le joueur au point de spawn
        """
        self.rect.x = self.image.get_rect().w + 350
        self.rect.y = param.game["taille_fenetre"][1] - 500

    def invinciblility(self):
        """
        Rend le joueur invincible
        """
        if self.invincible_time > 0:
            self.invincible_time -= 1
            self.invincible = True
        else:
            self.invincible = False

    def death(self):
        """
        Le joueur perd une vie
        """
        if not self.invincible:
            self.health -= 1
            self.invincible_time = 100
            self.game.histoire.game_score -= 30
            self.player_death()
            self.game.sound_canal.play(self.game.death_sound)


