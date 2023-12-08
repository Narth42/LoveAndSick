import pygame

from settings import Settings

param = Settings()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed, power=0, attack_distance=0):
        """
        Creation des projectiles
        :param x: (int) position en x
        :param y: (int) position en y
        :param direction: (int) direction du projectile
        :param speed: (int) vitesse du projectile
        :param power: (int) puissance du projecti
        :param attack_distance: (int) distance que peut parcourir le projectile
        """
        super(Projectile, self).__init__()
        self.image = pygame.image.load(param.images['projectile']).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.speed = speed
        self.power = power
        self.attack_distance = attack_distance
        self.dispawn_time = 20 * attack_distance

    def remove(self):
        """
        Supprime le projectile
        """
        self.kill()

    def move(self):
        """
        Fait bouger le projectile
        """
        self.rect.x += self.direction * self.speed

        if self.rect.x > param.game["taille_fenetre"][0] or self.dispawn_time < 0:
            self.remove()
        else:
            self.dispawn_time -= 1

    def general_collide(self, group):
        """
        Verification des collisions
        :param group: groupe de sprite
        """
        if pygame.sprite.spritecollide(self, group, False):
            self.remove()
