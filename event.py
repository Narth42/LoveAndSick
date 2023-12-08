import pygame
import random

from settings import Settings

param = Settings()


class Event:
    def __init__(self, game):
        """
        Evenement du jeu
        :param game: Class du jeu
        """
        self.game = game
        self.histoire = game.histoire
        self.player = game.player

        self.time = 0
        self.max_time = param.event['time']
        self.start_event = False
        self.entity = pygame.sprite.Group()
        self.event_cooldown = 100 * self.histoire.get_level()
        self.type = 0
        self.reset_type()
        self.blindness = False

    def add_time(self):
        """
        Remple petit a petit la barre d'evenement
        """
        self.time += random.randint(1, 7)

    def reset_time(self):
        """
        Reinitialise la barre d'evenement
        """
        self.time = 0

    def set_cooldown(self, cooldown):
        """
        Defini le cooldown de l'evenement
        """
        self.event_cooldown = cooldown

    def reset_type(self):
        """
        Reset le type de l'evenement
        """
        if self.histoire.get_level() <= 1:
            self.type = 1
        elif self.histoire.get_level() <= 3:
            self.type = random.randint(1, 2)
        else:
            self.type = random.randint(1, 3)

    def update(self):
        """
        Met a jour la barre d'evenement
        """
        # Cooldown
        if not self.start_event:
            self.add_time()
        else:
            self.event_cooldown -= 1

        # Fin de l'evenement
        if self.event_cooldown <= 0:
            self.event_cooldown = 100 * self.histoire.get_level()
            self.reset_time()
            self.reset_type()
            self.start_event = False
            self.player.health += 1
            self.game.histoire.game_score += 10
            self.blindness = False

    def draw_bar(self, surface):
        """
        Affiche les barres des evenements et le nom des evenements
        :param surface: Surface sur laquel afficher les elements
        """
        # Affichange des barres d'evenements
        pygame.draw.rect(surface, (102, 97, 96), [205, 49, surface.get_width() - 560, 8])
        pygame.draw.rect(surface, (246, 151, 14), [205, 49, (surface.get_width() - 560) * self.time / self.max_time, 8])

        # Affichange du nom de l'evenement
        if self.start_event:
            if self.type == 2:
                couleur = (255, 255, 255)
            else:
                couleur = (0, 0, 0)
            texte = "Event : " + param.event[str(self.type)] + "    Timer : " + str(self.event_cooldown)
            event_text = self.game.general_font.render(texte, False, couleur)
            surface.blit(event_text, ((param.game["taille_fenetre"][0] - self.game.general_font.size(texte)[0]) // 2, param.game["taille_fenetre"][1] - self.game.general_font.size(texte)[1]))

    def projectiles_fall(self):
        """
        Evenement de tombees de projectiles
        """
        if self.event_cooldown % 8 == 0:
            if self.histoire.get_level() <= 2:
                nb = random.randint(2, 4)
            elif self.histoire.get_level() <= 4:
                nb = random.randint(3, 6)
            else:
                nb = random.randint(5, 8)

            for i in range(1, nb):
                self.entity.add(EventEntity(self, self.histoire.get_level()))


class EventEntity(pygame.sprite.Sprite):

    def __init__(self, event, level, x=1, y=1):
        """
        Generation des entitees d'un evenement
        :param event: (class) L'evenement
        :param level: (int) niveau du actuel du jeu
        :param x: (int)
        :param y: (int)
        """
        super(EventEntity, self).__init__()
        self.level = level
        self.image = pygame.image.load(param.images["event"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 28))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, param.game['taille_fenetre'][0] * 2 // x)
        self.event = event

        # Vitesse alleatoire entitees en fonction du niveau
        if self.level <= 3:
            self.velocity = random.randint(1, 2)
        else:
            self.velocity = random.randint(1, 3)

        self.rect.y = -random.randint(60, 700) * y

    def remove(self):
        """
        Supprime les entitees
        """
        self.event.entity.remove(self)

    def fall(self):
        """
        Deplacement des entitees
        """
        self.rect.y += self.velocity

        if self.rect.y >= param.game['taille_fenetre'][1] - 150:
            self.remove()

    def move(self, player):
        """
        Mouvement des entitees
        :param player: Class joueur
        """
        self.rect.x -= player.speed + player.speed_boost

        if self.rect.x < - self.rect.width:
            self.remove()
