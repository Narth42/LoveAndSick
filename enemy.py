import pygame
import random
import animation

from settings import Settings
from event import EventEntity

param = Settings()


class Enemy_group(pygame.sprite.Group):
    def __init__(self, game):
        """
        Group des ennemis
        :param game: Class du jeu
        """
        pygame.sprite.Group.__init__(self)
        self.game = game

    def group(self, enemy):
        """
        Fonction qui ajoute des ennemis au groupe des ennemis
        :param enemy: (list) ennemis a ajoute dans le groupe
        """
        for i in enemy:
            self.add(i)

    def boss_generation(self):
        """
        Generation d'un boss
        """
        self.group([Boss(self.game, param.game["taille_fenetre"][0] // 2, param.game["taille_fenetre"][1] // 2 - 400)])

    def boss_bakubaku_generation(self, x, y):
        """
        Generation d'un bakubaku au cours du boos
        """
        self.group([Bakubaku(self.game, x, y)])

    def bakubaku_generation(self, x, y, rect):
        """
        Generation d'un bakubaku sur une plateforme
        :param x: (int) position x
        :param y: (int) position y
        :param rect: dimension d'une entitee
        """
        self.group([Bakubaku(self.game, x, y, rect)])


class Enemy(animation.AnimateSprite):

    def __init__(self, game, name, size, x, y):
        """
        Class des ennemis
        :param game: Class du jeu
        :param name: (str) Nom de l'entite
        :param size: (tuple) Taille de l'entite
        :param x: (int) position x
        :param y: (int) position y
        :param rect: dimension d'une entitee
        """
        super(Enemy, self).__init__(self, name, size)
        self.game = game
        self.name = name
        self.attack_distance = param.enemy[name][1]
        self.speed = param.enemy[name][2]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.moving = True
        self.spawn = True
        self.explotion = False
        self.event_time = 0
        self.attack_time = 0
        self.baku_time_spawn = random.randrange(200, 500, 100)
        self.boss_down = random.randint(400, 600)
        self.resistance = 0
        self.direction = 1
        self.health = param.enemy[name][0]
        self.max_health = self.health

        # Demarre l'animation
        self.start_animation()

    def update_animation(self):
        """
        Met a jour l'animation de l'entite
        """
        if self.explotion:
            if not self.animation:
                self.remove()
            else:
                self.animate()
        else:
            if self.name != "boss":
                self.change_direction()
            self.animate(loop=True)

    def update_health_bar(self, surface):
        """
        Affiche les barres de vie de l'entite
        :param surface: Surface sur laquel afficher les barres
        """

        if not self.explotion:
            pygame.draw.rect(surface, (60, 63, 60), [self.rect.x, self.rect.y - 15, self.rect.w, 7])
            pygame.draw.rect(surface, (111, 210, 46), [self.rect.x, self.rect.y - 15, self.rect.w * self.health // self.max_health, 7])

    def move(self):
        """
        Mouvement de l'entite
        """
        if self.moving:
            if self.game.histoire.start_histoire:
                # Fait avancer l'entite
                self.rect.x += self.speed * self.direction

                # Change de direction de l'entite
                if self.rect.x <= 0:
                    self.direction = 1
                elif self.rect.x >= param.game["taille_fenetre"][0] - self.rect.w:
                    self.direction = -1

            # Deplacement en y de l'entite boss
            if self.name == "boss":
                if self.rect.y >= 150:
                    self.rect.y -= self.speed
                elif self.rect.y <= 80:
                    self.rect.y += self.speed
                else:
                    self.rect.y += self.speed * random.randrange(-1, 2, 2)

    def auto_left_move(self):
        """
        Fait bouger l'ennemy vers la gauche en fonction de la vitesse du joueur
        """
        self.rect.x -= self.game.player.speed + self.game.player.speed_boost

    def update(self, surface):
        """
        Met a jour l'entite
        :param surface: Surface sur laquel afficher les barres
        """
        # Evenement en fonction de la vie de l'entite si boss
        if self.health <= 0 or self.rect.x <= -self.rect.w:
            self.game.histoire.game_score += 3
            self.remove()
        elif self.rect.x <= -self.rect.w:
            self.remove()
        elif self.health <= self.max_health // 4 and self.name == "boss":
            self.game.histoire_blindness_effect = False
            self.random_fall_event()
        elif self.health <= self.max_health // 2 and self.name == "boss":
            self.game.histoire_blindness_effect = True

        # Mise a jour de l'entite
        if self.game.histoire.start_histoire:
            self.update_animation()
        self.update_health_bar(surface)
        self.move()
        self.attack()

    def attack(self):
        """
        Attaque de l'entite
        """
        if self.name == "bakubaku" and self.attack_time >= 1000 and self.game.histoire.start_histoire:
            # Explosion du bakubaku
            self.explosion()

        elif self.name == "boss":
            if self.moving:
                if not self.spawn and len(self.game.enemy_group) == 1:
                    # Fait immobilise le boss
                    self.resistance = 0
                    self.attack_time = 0
                    self.moving = False

                elif self.attack_time >= 3000:
                    # Met fin au spawn des bakubaku
                    self.spawn = False

                elif self.spawn and self.attack_time % self.baku_time_spawn == 0 and self.attack_time >= 100:
                    # Generation d'un bakubaku
                    self.game.enemy_group.boss_bakubaku_generation(self.rect.x, self.rect.y)
                    self.baku_time_spawn = random.randrange(300, 500, 100)
                    self.attack_time += 1

                else:
                    self.attack_time += 1

            elif not self.moving and self.attack_time >= self.boss_down:
                # Fait rebouger le boss
                self.resistance = -self.game.gravity
                self.moving = True
                self.spawn = True
                self.attack_time = 0
                self.boss_down = random.randint(400, 600)

            else:
                self.attack_time += 1

        else:
            self.attack_time += 1

    def random_fall_event(self):
        """
        Event de tomber de projectile
        """
        if self.event_time % 200 == 0:
            for i in range(random.randint(1, 2)):
                self.game.event.entity.add(EventEntity(self.game.event, self.game.histoire.get_level(), x=2, y=0))
        self.event_time += 1

    def explosion(self):
        """
        Explosion de l'entite
        """
        self.direction = 0
        self.explotion = True
        self.change_direction()

    def remove(self):
        """
        Supression de l'entite
        """
        self.kill()

    def group_collision(self, group):
        """
        Collision de l'entite avec un group
        :param group: group avec lequel verifier la collision
        :return: True ou False en fonction de si il y a collision
        """
        if pygame.sprite.spritecollide(self, group, False):
            return True
        else:
            return False


class Bakubaku(Enemy):
    def __init__(self, game, x, y, rect=None):
        """
        Class des bakubaku
        :param game: Class du jeu
        :param x: (int) position x
        :param y: (int) position y
        """
        super(Bakubaku, self).__init__(game, "bakubaku", param.enemy["bakubaku"][3], x, y)
        if game.histoire.start_histoire:
            self.direction = random.randrange(-1, 2, 2)
        else:
            self.direction = -1
            self.rect.x = x + (rect.w - self.rect.w) // 2
            self.rect.y = y - self.rect.h

        self.resistance = 0
        self.health = param.enemy[self.name][0] + self.game.histoire.get_level() - 1
        self.max_health = self.health


class Boss(Enemy):
    def __init__(self, game, x, y):
        """
        Class des boss
        :param game: Class du jeu
        :param x: (int) position x
        :param y: (int) position y
        """
        super(Boss, self).__init__(game, "boss", param.enemy["boss"][3], x, y)
        self.resistance = -self.game.gravity
        self.direction = 1
