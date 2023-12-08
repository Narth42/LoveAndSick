import pygame

from settings import Settings

param = Settings()


class Texte:
    def __init__(self, game):
        """
        Class contenant le groupe des boutons du jeu et le groupe des dialogues du jeu
        :param game: Class du jeu
        """
        self.game = game
        self.buttons = pygame.sprite.Group()
        self.dialogues = pygame.sprite.Group()
        self.texte_fin = pygame.sprite.Group()
        self.dialogue_count = 0
        self.personnage_dialogue = 0
        self.dialogue = "Cliquer ici"
        self.start_dialogue = False

    """Button"""

    def group_buttons(self, buttons):
        """
        Ajoute des Sprite au groupe des boutons
        :param buttons: (list) liste des Sprite a ajouter au groupe
        """
        for i in buttons:
            self.buttons.add(i)

    def start_menu(self):
        """
        Generation des boutons du menu de demarrage
        """
        buttons = [Button(self.game, param.button["start"], (param.game['taille_fenetre'][0] // 2) - (param.button['size'][0] // 2), param.game['taille_fenetre'][1] // 2 - (param.button['size'][1] // 2) - 5),
                   Button(self.game, param.button["restart"], (param.game['taille_fenetre'][0] // 2) - (param.button['size'][0] // 2), param.game['taille_fenetre'][1] // 2 + (param.button['size'][1] // 2) + 5)]
        self.group_buttons(buttons)

    def pause_menu(self):
        """
        Generation des boutons du menu de pause
        """
        buttons = [Button(self.game, param.button["resume"], (param.game['taille_fenetre'][0] // 2) - (param.button['size'][0] // 2), param.game['taille_fenetre'][1] // 2 - (param.button['size'][1] // 2) * 3 - 5),
                   Button(self.game, param.button["save"], (param.game['taille_fenetre'][0] // 2) - (param.button['size'][0] // 2), param.game['taille_fenetre'][1] // 2 - (param.button['size'][1] // 2)),
                   Button(self.game, param.button["exit"], (param.game['taille_fenetre'][0] // 2) - (param.button['size'][0] // 2), param.game['taille_fenetre'][1] // 2 + (param.button['size'][1] // 2) + 5)]
        self.group_buttons(buttons)

    def del_button(self):
        """
        Supprime les Sprite contenu dans la groupe des boutons
        """
        self.buttons = pygame.sprite.Group()

    def button_collide(self, event_pos):
        """
        Verifie la collision entre la souris et un bouton
        :param event_pos: positon de la souris
        """
        for button in self.buttons:
            if button.rect.collidepoint(event_pos):
                # Declanche l'effet du bouton
                button.button_effect()

    """Dialogue"""

    def add_dialogue_surface(self):
        """
        Generation de la surface de dialogue
        """
        self.dialogues.add(Dialogue(self.game, param.images["dialogue_support"], 100, (param.game['taille_fenetre'][1] // 3) * 2, (param.game['taille_fenetre'][0] - 200, param.game['taille_fenetre'][1] // 3)))

    def dialogues_start(self, event_pos):
        """
        Demarrage des dialogue
        :param event_pos: positon de la souris
        """
        for dialogue in self.dialogues:
            if dialogue.rect.collidepoint(event_pos):
                self.dialogues_suivant()

    def dialogues_suivant(self):
        """
        Change le dialogue
        """
        if self.game.histoire.intro:
            if self.dialogue_count < len(param.dialogue["dialogue0"]):
                self.dialogue = param.dialogue["dialogue0"][self.dialogue_count][0]
                self.personnage_dialogue = param.dialogue["dialogue0"][self.dialogue_count][1]
                self.dialogue_count += 1
            else:
                self.dialogues = pygame.sprite.Group()
                self.dialogue_count = 0
                self.personnage_dialogue = 0
                self.dialogue = "Cliquer ici"
                self.start_dialogue = False

        elif self.game.histoire.dialogue_end:
            if self.dialogue_count < len(param.dialogue["dialogue6"]):
                self.dialogue = param.dialogue["dialogue6"][self.dialogue_count][0]
                self.personnage_dialogue = param.dialogue["dialogue6"][self.dialogue_count][1]
                self.dialogue_count += 1
            else:
                self.dialogues = pygame.sprite.Group()
                self.start_dialogue = False

        elif self.dialogue_count < len(param.dialogue["dialogue" + str(self.game.histoire.get_level())]):
            self.dialogue = param.dialogue["dialogue" + str(self.game.histoire.get_level())][self.dialogue_count][0]
            self.personnage_dialogue = param.dialogue["dialogue" + str(self.game.histoire.get_level())][self.dialogue_count][1]
            self.dialogue_count += 1
        else:
            if self.game.histoire.get_level() == 5:
                self.game.player.starting_point()
                self.game.enemy_group.boss_generation()
            self.dialogues = pygame.sprite.Group()
            self.dialogue_count = 0
            self.personnage_dialogue = 0
            self.dialogue = "Cliquer ici"
            self.start_dialogue = False

    """Texte Fin"""

    def group_texte_fin(self, textes):
        """
        Ajoute des Sprite au groupe des dialogues
        :param textes: (list) liste des Sprite a ajouter au groupe
        """
        for i in textes:
            self.texte_fin.add(i)

    def add_texte_fin(self):
        """
        Generation des texte de fin
        """
        minutes = self.game.secondes // 60
        heurs = minutes // 60
        minutes = minutes % 60
        secondes = minutes % 60

        texte1 = [Fin(self.game, param.generale["titre"], self.game.menu_font2, -self.game.menu_font2.size(param.generale["titre"])[1], (204, 51, 190))]
        texte2 = [Fin(self.game, 'Votre score final: ' + str(self.game.histoire.game_score), self.game.menu_font1, 70, (255, 255, 255))]
        texte3 = [Fin(self.game, 'Votre temps: ' + str(heurs) + ' h, ' + str(minutes) + ' min et ' + str(secondes) + ' s', self.game.menu_font1, 2 * 70, (255, 255, 255))]
        texte4 = [Fin(self.game, param.histoire["texte_fin"][i], self.game.menu_font1, (i + 4) * 70, (255, 255, 255)) for i in range(len(param.histoire["texte_fin"]))]
        self.group_texte_fin(texte1)
        self.group_texte_fin(texte2)
        self.group_texte_fin(texte3)
        self.group_texte_fin(texte4)


class Button(pygame.sprite.Sprite):
    def __init__(self, game, item, x, y):
        """
        Class des boutons du jeu
        :param game: Class du jeu
        :param item: (int) id du bouton
        :param x: (int) Position en x
        :param y: (int) Position en y
        """
        super(Button, self).__init__()
        self.game = game
        self.item = item
        self.image = pygame.image.load(param.images['button']).convert_alpha()
        self.image = pygame.transform.scale(self.image, param.button['size'])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def button_effect(self):
        """
        Effet des boutons du jeu
        """
        if self.item == param.button["start"]:
            # Commancement du jeu
            if self.game.histoire.total_score == 0:
                self.game.histoire.intro = True
                self.game.texte.start_dialogue = True
                self.game.texte.add_dialogue_surface()
            elif self.game.save.get_save()['histoire']:
                # Si le joueur ete au dans l'histoire alors le remettre juste avant l'histoire
                self.game.histoire.score = param.histoire['level' + str(self.game.save.get_save()['level'])] - 200
                self.game.histoire.total_score -= 200
            self.game.start_game = True
            self.game.texte.del_button()
            self.game.plateformes.start_generation()

        elif self.item == param.button["restart"]:
            # Recommancement du jeu
            self.game.save.reset_save()
            self.game.restart()
            self.game.start_game = True
            self.game.texte.del_button()
            self.game.plateformes.start_generation()
            if self.game.histoire.get_level() == 1:
                self.game.histoire.intro = True
                self.game.texte.start_dialogue = True
                self.game.texte.add_dialogue_surface()

        elif self.item == param.button["resume"]:
            # Reprise du jeu
            self.game.pause = False
            self.game.texte.del_button()

        elif self.item == param.button["save"]:
            # Souvegarde le jeu
            self.game.save.do_save()

        elif self.item == param.button["exit"]:
            # Quite le jeu
            self.game.save.do_save()
            self.game.running = False


class Dialogue(pygame.sprite.Sprite):
    def __init__(self, game, image, x, y, size):
        """
        Class des dialogues du jeu
        :param game: Class du jeu
        :param image: image du Sprite
        :param x: (int) position en x
        :param y: (int) position en y
        """
        super(Dialogue, self).__init__()
        self.game = game
        self.image = pygame.image.load(image).convert_alpha()
        self.image = self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Fin(pygame.sprite.Sprite):
    def __init__(self, game, texte, font, espace, color):
        """
        Class des dialogues du jeu
        :param game: Class du jeu
        :param texte: (str) Texte a afficher
        :param font: Police d'ecriture
        :param espace: (int) espace entre chaque texte
        """
        super(Fin, self).__init__()
        self.game = game
        self.texte = texte
        self.font = font
        self.color = color
        self.image = pygame.image.load(param.images['text_support']).convert_alpha()
        self.image = self.image = pygame.transform.scale(self.image, (font.size(texte)[0], font.size(texte)[1]))
        self.rect = self.image.get_rect()
        self.rect.x = (param.game['taille_fenetre'][0] - self.rect.w) // 2
        self.rect.y = param.game['taille_fenetre'][1] + espace

    def update(self, surface):
        """
        Met a jour les textes
        :param surface: Surface sur laquel afficher le texte
        """
        text = self.font.render(self.texte, True, self.color)
        surface.blit(text, (self.rect.x, self.rect.y))

        self.move()

    def move(self):
        """
        Fait bouger les texte
        """
        self.rect.y -= param.histoire["texte_speed"]

        if self.rect.y < 0 - self.rect.h:
            self.remove()

    def remove(self):
        """
        Supression du texte
        """
        self.kill()
