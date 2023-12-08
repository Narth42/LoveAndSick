import pygame

from settings import Settings

param = Settings()


class Histoire:
    def __init__(self, game):
        """
        Histoire du jeu
        :param game: Class du jeu
        """
        self.game = game
        self.save = game.save.get_save()
        self.score = self.save['score']
        self.total_score = self.save['total_score']
        self.max_score = param.histoire['level' + str(self.save['level'])]
        self.game_score = self.save['game_score']
        self.level = self.save['level']
        self.start_histoire = False
        self.end = False
        self.intro = False
        self.dialogue_end = False

    def add_score(self):
        """
        Ajoute 1 au score du jeu
        """
        if not self.end and not self.start_histoire:
            self.score += 1
            self.total_score += 1

    def reset_score(self):
        """
        Reinitialise le score
        """
        self.score = 0

    def draw_bar(self, surface):
        """
        Met a jour la barre de l'histoire
        :param surface: Surface sur laquelle la barre sera affiche
        """
        pygame.draw.rect(surface, (102, 97, 96), [180, 35, surface.get_width() - 510, 12])
        pygame.draw.rect(surface, (187, 11, 11), [180, 35, (surface.get_width() - 510) * self.score / self.max_score, 12])

    def introduction(self):
        """
        Introduction du jeu
        """
        if not self.game.texte.dialogues:
            self.game.player.starting_point()
            self.intro = False

    def dialogue_fin(self):
        """
        Fin du jeu
        """
        if not self.game.texte.dialogues:
            self.dialogue_end = False
            self.end = True
            self.game_score += 400

    def start(self):
        """
        Evenement de l'histoire quand elle est active en fonction du niveau
        """
        if self.level == 1:
            if not self.game.texte.dialogues:
                self.end_histoire()
                self.game_score += 100

        elif self.level == 2:
            if not self.game.texte.dialogues:
                self.end_histoire()
                self.game_score += 150

        elif self.level == 3:
            if not self.game.enemy_group and not self.game.texte.dialogues:
                self.end_histoire()
                self.game_score += 200

        elif self.level == 4:
            if not self.game.texte.dialogues:
                self.end_histoire()
                self.game_score += 300

        elif self.level == 5:
            if not self.game.enemy_group and not self.game.texte.dialogues:
                self.game.texte.start_dialogue = True
                self.game.texte.add_dialogue_surface()
                self.dialogue_end = True
                self.start_histoire = False
                self.game.histoire_blindness_effect = False

    def end_histoire(self):
        """
        Fin de l'evenement de l'histoire
        """
        self.level += 1
        self.max_score = param.histoire['level'+str(self.level)]
        self.game.player.starting_point()
        self.start_histoire = False
        self.game.histoire_blindness_effect = False

    def get_level(self):
        """
        Renvoie le niveau actuel du jeu
        :return: (int) niveau actuel du jeu
        """
        assert self.level <= 5, "Le niveau du jeu est au dessus de 5 !"
        return self.level
