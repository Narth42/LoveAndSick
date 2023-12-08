import pygame

from settings import Settings
from player import Player
from generation import Generation
from histoire import Histoire
from event import Event
from deco import DecoGroup
from save import Save
from texte import Texte
from enemy import Enemy_group
from boost import Boost_group

pygame.init()
param = Settings()


class Game:
    def __init__(self):
        """
        Class principale du jeu
        """

        # Regarde si les parametres sont bons
        self.check_settings()

        # Titre du jeu
        pygame.display.set_caption(param.generale['titre'] + ' : ' + param.generale['version'])

        # Images
        self.screen = pygame.display.set_mode(param.game['taille_fenetre'])
        self.background = pygame.image.load(param.images['background']).convert_alpha()
        self.dark_background = pygame.image.load(param.images['dark_background']).convert_alpha()
        self.screen_blindness = pygame.image.load(param.images['blindness']).convert_alpha()
        self.histoire_blindness = pygame.image.load(param.images['blindness2']).convert_alpha()

        # Polices d'ecriture
        self.general_font = pygame.font.Font(param.font['general_font'], param.font['general_font_size'])
        self.menu_font1 = pygame.font.Font(param.font['menu_font1'], param.font['menu_font_size1'])
        self.menu_font2 = pygame.font.Font(param.font['menu_font2'], param.font['menu_font_size2'])
        self.dialogue_font = pygame.font.Font(param.font['dialogue_font'], param.font['dialogue_font_size'])

        # Sons
        self.sound = pygame.mixer.Sound(param.sound["background_sound"])
        self.sound.set_volume(param.game["music_level"])
        self.shoot_sound = pygame.mixer.Sound(param.sound["shoot_sound"])
        self.shoot_sound.set_volume(param.game["sound_level"])
        self.jump_sound = pygame.mixer.Sound(param.sound["jump_sound"])
        self.jump_sound.set_volume(param.game["sound_level"])
        self.click_sound = pygame.mixer.Sound(param.sound["click_sound"])
        self.click_sound.set_volume(param.game["sound_level"])
        self.death_sound = pygame.mixer.Sound(param.sound["death_sound"])
        self.death_sound.set_volume(param.game["sound_level"])

        self.sound_canal = pygame.mixer.Channel(0)

        # Class et groupe
        self.save = Save(self)
        self.texte = Texte(self)
        self.histoire = Histoire(self)
        self.deco = DecoGroup(self)
        self.player = Player(self)
        self.plateformes = Generation(self)
        self.event = Event(self)
        self.enemy_group = Enemy_group(self)
        self.boost_group = Boost_group(self)

        self.player_projectiles = self.player.projectiles

        # Gravite
        self.gravity = 8
        self.player_resistance = 0

        # Collision
        self.right_collision = False
        self.left_collision = False
        self.top_collision = False
        self.bottom_collision = False

        # Autre
        self.running = True
        self.pause = False
        self.start_game = False

        self.clock = pygame.time.Clock()
        self.pressed_keys = {}

        self.histoire_blindness_effect = False

        self.time = 0
        self.secondes = self.save.save['game_time']

        self.game_chargement = True
        self.time_chargement = 0
        self.text_chargement = 0

    def boucle(self):
        """
        Boucle principale du jeu
        """

        # Creation des boutons du menu de demarrage du jeu
        self.texte.start_menu()

        while self.running:
            # Affichage de l'ecrant
            if not self.histoire.end:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.blit(self.dark_background, (0, 0))

            # Affichange du titre et de la version du jeu
            if not self.start_game:
                titre = self.menu_font2.render(param.generale['titre'], False, (204, 51, 190))
                self.screen.blit(titre, ((param.game['taille_fenetre'][0] - self.menu_font2.size(param.generale['titre'])[0]) // 2, (param.game['taille_fenetre'][1] - self.menu_font2.size(param.generale['titre'])[1]) // 5))

                version = self.menu_font1.render('Version : ' + param.generale['version'], False, (0, 0, 0))
                self.screen.blit(version, (10, param.game['taille_fenetre'][1] - self.menu_font1.size('Version : ' + param.generale['version'])[1] - 10))

            if self.game_chargement:
                # Chargement du jeu
                chargement = self.menu_font1.render('Chargement' + '.' * self.text_chargement, False, (0, 0, 0))
                self.screen.blit(chargement, (param.game['taille_fenetre'][0] - self.menu_font1.size('Chargement')[0] - 50, param.game['taille_fenetre'][1] - self.menu_font1.size('Chargement')[1] - 10))
                self.chargement()

            # Evenement du jeu
            self.commande()

            '''Jeu'''

            # Demarrage du jeu
            if self.start_game and not self.histoire.end:
                if not self.pause and not self.texte.start_dialogue:

                    self.game_time()
                    self.autogeneration()
                    self.plateforme()
                    self.joueur()
                    self.enemy()
                    self.boost()
                    self.projectile()
                    self.events()
                    self.histoires()
                    self.sound.play()
                    self.end()

                self.affichage()

            self.affichage_texte()
            self.end_close()

            # Mise a jour de l'ecran
            pygame.display.flip()

            # FPS du jeux
            self.clock.tick(param.game['fps'])

    def chargement(self):
        """
        Temps de chargement du jeu
        """
        self.time_chargement += 1
        if self.time_chargement % 30 == 0:
            if self.text_chargement == 4:
                self.text_chargement = 0
            else:
                self.text_chargement += 1

        if self.time_chargement >= 5 * 30:
            self.game_chargement = False

    def commande(self):
        """
        Evenement pour chaque touche presser
        """
        for event in pygame.event.get():
            # Quand le joueur quite le jeu
            if event.type == pygame.QUIT:
                self.save.do_save()
                self.running = False
            if not self.game_chargement:
                # Quand le joueur appuit sur <echap>
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if not self.pause and self.start_game:
                        # Met le jeu en pause
                        self.texte.pause_menu()
                        self.pause = True
                        self.sound.stop()
                    else:
                        # Enleve le mode pause
                        self.texte.del_button()
                        self.pause = False
                # Quand le joueur clique sur l'ecrant
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.start_game or self.pause:
                        self.texte.button_collide(event.pos)
                        self.sound_canal.play(self.click_sound)
                    elif self.histoire.start_histoire or self.histoire.intro or self.histoire.dialogue_end:
                        self.texte.dialogues_start(event.pos)
                        self.sound_canal.play(self.click_sound)

                # Enregistrement des touches pressees et relachees
                elif event.type == pygame.KEYDOWN:
                    self.pressed_keys[event.key] = True
                elif event.type == pygame.KEYUP:
                    self.pressed_keys[event.key] = False

    def autogeneration(self):
        """
        Generation automatique des plateformes
        """
        # Auto generation des plateformes
        if not self.histoire.start_histoire:
            if len(self.plateformes) <= 11:
                self.plateformes.auto_generation()
                self.histoire.game_score += 1

    def plateforme(self):
        """
        Evenement des plateformes
        """
        for plateforme in self.plateformes:
            # Activation des effets des differente plateforme
            plateforme.casse(self.player.rect)
            plateforme.glace(self.player.rect)
            plateforme.move(self.player, self.bottom_collision)

    def clear_plateforme(self):
        """
        Supprime toutes les plateformes
        """
        for plateforme in self.plateformes:
            plateforme.remove()

    def clear_deco(self):
        """
        Supprime tout les elements de decorations
        """
        for deco in self.deco:
            deco.remove()

    def clear_enemy(self):
        """
        Supprime tous les ennemis
        """
        for enemy in self.enemy_group:
            enemy.remove()

    def clear_event_entity(self):
        """
        Supprime tous les projectiles qui tombent
        """
        for entity in self.event.entity:
            entity.remove()

    def clear_boost(self):
        """
        Supprime tout les boosts
        """
        for boost in self.boost_group:
            boost.remove()

    def clear_all(self):
        """
        Supprime les entitees du jeu
        """
        self.clear_plateforme()
        self.clear_enemy()
        self.clear_event_entity()
        self.clear_deco()
        self.clear_boost()

    def gravite(self, entity):
        """
        Gravite du jeu
        :param entity: (Sprite) une entitee du jeu
        """
        # Si l'entitee est le joueur
        if entity == self.player:
            # Si il y a collision la gravite est compensee
            if self.bottom_collision:
                self.player_resistance = -self.gravity
            else:
                self.player_resistance = 0

            # Application de la gravite
            self.player.rect.y += self.gravity + self.player_resistance

        else:
            # Annule la gravite pour l'entitee si collision
            if entity.group_collision(self.plateformes):
                entity.resistance = -self.gravity
            else:
                self.player_resistance = 0

    def enemy(self):
        """
        Evenement des ennemis
        """
        for enemy in self.enemy_group:
            # Mise a jour des mouvements des ennemis
            enemy.update(self.screen)
            self.gravite(enemy)
            enemy.rect.y += self.gravity + enemy.resistance

            # Verification des collisions entre les ennemis et les tires du joueur
            if enemy.group_collision(self.player.projectiles):
                for projectiles in self.player.projectiles:
                    # Suppression du projectile
                    if projectiles.rect.colliderect(enemy.rect):
                        projectiles.remove()
                # Enleve un point de vie a l'entite touchee
                enemy.health -= 1

            # Verification des collisions entre les ennemis et le joueur
            if enemy.rect.colliderect(self.player.rect):
                if enemy.name != "boss":
                    # Suppression de l'entitee si toucher et si non boss
                    enemy.remove()
                    self.player.death()

    def joueur(self):
        """
        Evenement du joueur
        """
        self.collisions()

        # Deplacement du joueur
        # Quand touche <d> pressee
        if self.pressed_keys.get(pygame.K_d) and not self.right_collision and self.player.rect.x < param.game["taille_fenetre"][0] - self.player.rect.w:
            # Si joueur a 1/3 de la fenetre
            if self.player.rect.x < param.game['taille_fenetre'][0] / 3 or self.histoire.start_histoire:
                # Mouvement du joueur vers la droite
                self.player.move(1)
            else:
                # Mouvement des elements du jeu vers la gauche
                self.left_entity_movement()

            # Demarrage de l'animation du joueur
            self.player.start_animation()
            self.player.change_direction()

            # Ajout du score
            if self.histoire.score < self.histoire.max_score and not self.pressed_keys.get(pygame.K_q):
                self.histoire.add_score()

        # Quand touche <q> pressee
        if self.pressed_keys.get(pygame.K_q) and self.player.rect.x > 0 and not self.left_collision:
            # Mouvement du joueur vers la gauche
            self.player.move(-1)
            self.player.start_animation()
            self.player.change_direction()

        # Quand touche <espace> pressee
        if self.pressed_keys.get(pygame.K_SPACE) and self.bottom_collision:
            # Demarre le saut du joueur
            self.player.a_sauter = True
            self.sound_canal.play(self.jump_sound)

        # Saut du joueur
        if self.player.a_sauter:
            self.player.jump()

        # Annulation du saut si collision en haut
        if self.top_collision:
            self.player.a_sauter = False

        # Quand touche <e> pressee
        if self.pressed_keys.get(pygame.K_e):
            # Attaque du joueur
            self.player.attaque()

        # Invincibilite du joueur
        self.player.invinciblility()

        # Gravite du joueur
        self.gravite(self.player)

        # Mise a jour du joueur
        self.player.update()
        self.player.update_animation()

        # Mort du joueur
        self.death()
        self.loose()

    def left_entity_movement(self):
        """
        Mouvement des entitees du jeu vers la gauche
        """
        for plateforme in self.plateformes:
            plateforme.update(self.player)
        for entity in self.event.entity:
            entity.move(self.player)
        for element in self.deco:
            element.update(self.player)
        for ennemis in self.enemy_group:
            ennemis.update(self.screen)
            ennemis.auto_left_move()
        for boost in self.boost_group:
            boost.update(self.player)

    def collisions(self):
        """
        Collisions du jeu
        """
        # Verification des collisions entre le joueur et les plateformes
        for plateforme in self.plateformes:
            if self.player.bottom_collide(plateforme):
                self.bottom_collision = True
            elif not self.player.general_collide(self.plateformes):
                self.bottom_collision = False
            if self.player.top_collide(plateforme):
                self.top_collision = True
            elif not self.player.general_collide(self.plateformes):
                self.top_collision = False
            if self.player.right_collide(plateforme):
                self.right_collision = True
            elif not self.player.general_collide(self.plateformes):
                self.right_collision = False
            if self.player.left_collide(plateforme):
                self.left_collision = True
            elif not self.player.general_collide(self.plateformes):
                self.left_collision = False

    def death(self):
        """
        Mort du joueur
        """
        # Quand joueur tombe
        if self.player.rect.y > param.game["taille_fenetre"][1]:
            # Suppression des entity prensente sur le jeu
            self.clear_all()

            # Generation des nouvelles plateformes
            self.plateformes.death_generation()

            # Remise du joueur au point de depart avec une vie en moin
            self.player.starting_point()
            self.player.death()

    def loose(self):
        """
        Quand le joueur n'a plus de vie
        """
        if self.player.health == 0:
            # Suppression des entity prensente sur le jeu
            self.clear_all()

            self.histoire.game_score -= 100

            # Reatribution des paramettres du commencement du niveau actuel ou au debut du boss
            self.player.health = param.player["health"]
            self.event.start_event = False
            self.event.blindness = False
            self.event.event_cooldown = 100 * self.histoire.get_level()
            if self.histoire.start_histoire:
                level = self.histoire.get_level()
                self.histoire.score = param.histoire['level' + str(self.histoire.get_level())] - 200
                self.histoire.total_score = -200
            else:
                level = self.histoire.get_level()
                self.histoire.score = 0
                self.histoire.total_score = 0
            for i in range(0, level):
                if i != 0:
                    self.histoire.total_score += param.histoire['level' + str(i)]
            self.histoire.start_histoire = False

            # Remise du joueur au point de depart et generation des premiere plateforme
            self.player.starting_point()
            self.plateformes.death_generation()

    def projectile(self):
        """
        Projectiles du jeu
        """
        for projectile in self.player_projectiles:
            projectile.move()
            projectile.general_collide(self.plateformes)

    def boost(self):
        """
        Boosts du jeu
        """
        self.boost_group.boost_effect(self.player)
        for boost in self.boost_group:
            boost.collision(self.player)

    def events(self):
        """
        Event du jeu
        """

        # Demarrage d'un evenement
        if self.event.time >= self.event.max_time:
            self.event.start_event = True
            self.event.reset_time()

            # Lancement du bon type d'evenement
            if self.event.type == 1:
                self.event.set_cooldown(100 * self.histoire.get_level())
            elif self.event.type == 2:
                self.event.set_cooldown(1000 * self.histoire.get_level())
            elif self.event.type == 3:
                self.event.set_cooldown(500 * self.histoire.get_level())

        if self.event.start_event:
            # Lancement des effets de l'evenement
            if self.event.type == 1:
                self.event.projectiles_fall()
            elif self.event.type == 2:
                self.event.blindness = True
            elif self.event.type == 3:
                if not self.right_collision and self.player.rect.x < param.game["taille_fenetre"][0] - self.player.rect.w:
                    # Si joueur a 1/3 de la fenetre
                    if self.player.rect.x < param.game['taille_fenetre'][0] / 3 or self.histoire.start_histoire:
                        # Mouvement du joueur vers la droite
                        self.player.move(1)
                    else:
                        # Mouvement des elements du jeu vers la gauche
                        self.left_entity_movement()

                    # Demarrage de l'animation du joueur
                    self.player.start_animation()

        # Evenement de projectile qui tombe
        for entity in self.event.entity:
            entity.fall()
            # Verification des collisions
            if self.player.rect.colliderect(entity):
                entity.remove()
                self.player.death()
            if pygame.sprite.spritecollide(entity, self.plateformes, False):
                entity.remove()

        # Met a jour l'evenement
        if not self.histoire.start_histoire:
            self.event.update()

    def histoires(self):
        """
        Histoire du jeu
        """

        # Demarrage de l'histoire
        if self.histoire.score >= self.histoire.max_score:
            self.player.invincible_time = 50
            self.player.invinciblility()
            self.histoire.reset_score()
            self.event.reset_time()
            self.histoire.start_histoire = True
            self.event.start_event = False
            self.event.blindness = False

            # Suppression des entitees presente sur le jeu
            self.clear_all()

            # Generation des plateformes de l'histoire
            self.plateformes.story_generation()

            # Debut de l'evenement
            self.texte.start_dialogue = True
            self.texte.add_dialogue_surface()

        # Lancement de l'histoire
        if self.histoire.start_histoire:
            self.histoire.start()
        elif self.histoire.intro:
            self.histoire.introduction()
        elif self.histoire.dialogue_end:
            self.histoire.dialogue_fin()

    def dialogue_text(self):
        """
        Affichange du texte des dialogues
        """
        texte = self.texte.dialogue
        for dialogue in self.texte.dialogues:
            # Si le dialoque est inferieur a la fenetre de dialogue
            if self.dialogue_font.size(texte)[0] < dialogue.rect.w:
                # Affichage du dialogue
                dialogue_text = self.dialogue_font.render(texte, False, (255, 255, 255))
                self.screen.blit(dialogue_text, (dialogue.rect.x + (dialogue.rect.w - self.dialogue_font.size(texte)[0]) // 2, dialogue.rect.y + (dialogue.rect.h - self.dialogue_font.size(texte)[1]) // 2))
            else:
                liste_texte = []
                # Decoupage du dialogue en chaine de 56 carracteres
                for i in range(len(texte) // 56):
                    liste_texte.append(texte[:57])
                    texte = texte[57:]
                liste_texte.append(texte)

                for i in range(len(liste_texte)):
                    # Affichage de la liste de dialogue
                    dialogue_text = self.dialogue_font.render(liste_texte[i], False, (255, 255, 255))
                    self.screen.blit(dialogue_text, (dialogue.rect.x + 160, dialogue.rect.y + (dialogue.rect.h - self.dialogue_font.size(liste_texte[i])[1] - 27 * len(liste_texte)) // 2 + 27 * (i + 1)))

    def affichage(self):
        """
        Affichage des elements du jeu
        """
        # Couleur du texte
        color = (0, 0, 0)

        # Affichange des elements du jeu
        self.plateformes.draw(self.screen)
        self.deco.draw(self.screen)
        self.event.entity.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.boost_group.draw(self.screen)
        self.player_projectiles.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)

        # Affichange des dialogues
        if self.texte.personnage_dialogue == 1:
            image = pygame.image.load(param.images['player']).convert_alpha()
            image = pygame.transform.scale(image, param.dialogue['saiko_size'])
            self.screen.blit(image, (150, (param.game['taille_fenetre'][1] - image.get_rect().x) // 3))
        elif self.texte.personnage_dialogue == 2:
            image = pygame.image.load(param.images['masahiro']).convert_alpha()
            image = pygame.transform.scale(image, param.dialogue['masahiro_size'])
            self.screen.blit(image, (param.game['taille_fenetre'][0] - 400, (param.game['taille_fenetre'][1] - image.get_rect().x) // 3))
        elif self.texte.personnage_dialogue == 3:
            image = pygame.image.load(param.images['boss']).convert_alpha()
            image = pygame.transform.scale(image, param.dialogue['kaguya_size'])
            self.screen.blit(image, (param.game['taille_fenetre'][0] - 400, (param.game['taille_fenetre'][1] - image.get_rect().x) // 3))
        elif self.texte.personnage_dialogue == 4:
            image = pygame.image.load(param.images['bakubaku']).convert_alpha()
            image = pygame.transform.scale(image, param.dialogue['bakubaku_size'])
            self.screen.blit(image, (param.game['taille_fenetre'][0] - 400, (param.game['taille_fenetre'][1] - image.get_rect().x) // 3))
        self.texte.dialogues.draw(self.screen)

        if self.texte.start_dialogue:
            self.dialogue_text()

        # Changement de la couleur du texte + affichange de la vision reduite
        if self.event.blindness:
            self.screen.blit(self.screen_blindness, (self.player.rect.x - 1270, self.player.rect.y - 720))
            color = (255, 255, 255)
        elif self.histoire_blindness_effect:
            self.screen.blit(self.histoire_blindness, (self.player.rect.x - 1270, self.player.rect.y - 720))
            color = (255, 255, 255)

        # Affichange de la barre d'evenement et d'histoire
        self.event.draw_bar(self.screen)
        self.histoire.draw_bar(self.screen)

        # Affichage du texte du score
        score_text = self.general_font.render("Score : " + str(self.histoire.total_score), False, color)
        self.screen.blit(score_text, (param.game["taille_fenetre"][0] - 190, 30))

        # Affichage du texte des niveaux
        level_text = self.general_font.render("Level : " + str(self.histoire.get_level()), False, color)
        self.screen.blit(level_text, (param.game["taille_fenetre"][0] - 310, 30))

        # Affichage du texte des vies
        heath_text = self.general_font.render("Health : " + str(self.player.health), False, color)
        self.screen.blit(heath_text, (20, 30))

    def affichage_texte(self):
        """
        Affiche les differents groupes de la class texte
        """

        # Affichage des boutons
        self.texte.buttons.draw(self.screen)
        self.texte.texte_fin.draw(self.screen)

        # Affichage des textes des boutons
        for button in self.texte.buttons:
            texte_button = self.menu_font1.render(param.button["texte" + str(button.item)], False, (0, 0, 0))
            self.screen.blit(texte_button, (button.rect.x + (button.rect.w - self.menu_font1.size(param.button["texte" + str(button.item)])[0]) // 2, button.rect.y + (button.rect.h - self.menu_font1.size(param.button["texte" + str(button.item)])[1]) // 2))

        for texte in self.texte.texte_fin:
            texte.update(self.screen)

    def restart(self):
        """
        Remet a zero le jeu
        """

        # Remet a zero les differentes variable du jeu
        self.player.health = param.player["health"]
        self.histoire.level = param.histoire["level"]
        self.histoire.score = param.histoire["base_score"]
        self.histoire.total_score = param.histoire["base_score"]
        self.histoire.game_score = param.histoire["game_score"]
        self.histoire.start_histoire = False
        self.secondes = 0

    def end(self):
        """
        Condition de fin du jeu
        """
        # Fin du jeu quand l'histoire est fini
        if self.histoire.end:
            # Generation du texte de fin
            self.texte.add_texte_fin()
            self.clear_all()
            self.sound.stop()

    def end_close(self):
        """
        Fermeture du jeu
        """
        if not self.texte.texte_fin and self.histoire.end:
            # Reset les parametre du jeu
            self.histoire.end = False
            self.save.reset_save()
            self.running = False

    def game_time(self):
        """
        Temps de jeu
        """
        if self.time % 30 == 0:
            self.secondes += 1
            self.time = 0
        self.time += 1

    def check_settings(self):
        """
        Verifie si les paramettres du jeu sont valides
        """
        # Int / Float
        if param.game["fps"] < 0 or not isinstance(param.game["fps"], int):
            param.game["fps"] = 60
            print("Error value: settings/game/fps")

        if param.game["music_level"] < 0 or not isinstance(param.game["music_level"], (int, float)):
            param.game["music_level"] = 0.1
            print("Error value: settings/game/music_level")

        if param.game["sound_level"] < 0 or not isinstance(param.game["sound_level"], (int, float)):
            param.game["sound_level"] = 0.2
            print("Error value: settings/game/sound_level")

        if param.player["health"] < 0 or not isinstance(param.player["health"], int):
            param.player["health"] = 5
            print("Error value: settings/player/health")

        if param.player["speed"] < 0 or not isinstance(param.player["speed"], (int, float)):
            param.player["speed"] = 5
            print("Error value: settings/player/speed")

        if param.player["jump"] < 0 or not isinstance(param.player["jump"], (int, float)):
            param.player["jump"] = 6.5
            print("Error value: settings/player/jump")

        if param.player["size"][0] < 0 or param.player["size"][1] < 0 or not isinstance(param.player["size"], tuple) or not isinstance(param.player["size"][0], int) or not isinstance(param.player["size"][1], int):
            param.player["size"] = (40, 90)
            print("Error value: settings/player/size")

        if param.player["weapon"][0] < 0 or param.player["weapon"][1] < 0 or param.player["weapon"][2] < 0 or not isinstance(param.player["weapon"], tuple) or not isinstance(param.player["weapon"][0], (int, float)) or not isinstance(param.player["weapon"][1], int) or not isinstance(param.player["weapon"][2], int):
            param.player["weapon"] = (5, 1, 3)
            print("Error value: settings/player/weapon")

        if param.player["image_player_shoot_size"][0] < 0 or param.player["image_player_shoot_size"][1] < 0 or not isinstance(param.player["image_player_shoot_size"], tuple) or not isinstance(param.player["image_player_shoot_size"][0], int) or not isinstance(param.player["image_player_shoot_size"][1], int):
            param.player["image_player_shoot_size"] = (60, 90)
            print("Error value: settings/player/image_player_shoot_size")

        if param.player["shoot_speed"] < 0 or not isinstance(param.player["shoot_speed"], (int, float)):
            param.player["shoot_speed"] = 25
            print("Error value: settings/player/shoot_speed")

        if param.enemy["boss"][0] < 0 or param.enemy["boss"][1] < 0 or param.enemy["boss"][2] < 0 or param.enemy["boss"][3][0] < 0 or param.enemy["boss"][3][1] < 0 or not isinstance(param.enemy["boss"], tuple) or not isinstance(param.enemy["boss"][0], int) or not isinstance(param.enemy["boss"][1], int) or not isinstance(param.enemy["boss"][2], (int, float)) or not isinstance(param.enemy["boss"][3], tuple) or not isinstance(param.enemy["boss"][3][0], int) or not isinstance(param.enemy["boss"][3][1], int):
            param.enemy["boss"] = (300, 5, 3, (100, 136))
            print("Error value: settings/enemy/boss")

        if param.enemy["bakubaku"][0] < 0 or param.enemy["bakubaku"][1] < 0 or param.enemy["bakubaku"][2] < 0 or param.enemy["bakubaku"][3][0] < 0 or param.enemy["bakubaku"][3][1] < 0 or not isinstance(param.enemy["bakubaku"], tuple) or not isinstance(param.enemy["bakubaku"][0], int) or not isinstance(param.enemy["bakubaku"][1], int) or not isinstance(param.enemy["bakubaku"][2], (int, float)) or not isinstance(param.enemy["bakubaku"][3], tuple) or not isinstance(param.enemy["bakubaku"][3][0], int) or not isinstance(param.enemy["bakubaku"][3][1], int):
            param.enemy["bakubaku"] = (2, 5, 2, (45, 63))
            print("Error value: settings/enemy/bakubaku")

        if param.event["time"] < 0 or not isinstance(param.event["time"], int):
            param.event["time"] = 20000
            print("Error value: settings/event/time")

        if param.histoire["base_score"] < 0 or not isinstance(param.histoire["base_score"], int):
            param.histoire["base_score"] = 0
            print("Error value: settings/histoire/base_score")

        if param.histoire["game_score"] < 0 or not isinstance(param.histoire["game_score"], int):
            param.histoire["game_score"] = 0
            print("Error value: settings/histoire/game_score")

        if param.histoire["level"] < 1 or param.histoire["level"] > 5 or not isinstance(param.histoire["level"], int):
            param.histoire["level"] = 1
            print("Error value: settings/histoire/level")

        if param.histoire["level1"] < 0 or not isinstance(param.histoire["level1"], int):
            param.histoire["level1"] = 15000
            print("Error value: settings/histoire/level1")

        if param.histoire["level2"] < 0 or not isinstance(param.histoire["level2"], int):
            param.histoire["level2"] = 17000
            print("Error value: settings/histoire/level2")

        if param.histoire["level3"] < 0 or not isinstance(param.histoire["level3"], int):
            param.histoire["level3"] = 20000
            print("Error value: settings/histoire/level3")

        if param.histoire["level4"] < 0 or not isinstance(param.histoire["level4"], int):
            param.histoire["level4"] = 23000
            print("Error value: settings/histoire/level4")

        if param.histoire["level5"] < 0 or not isinstance(param.histoire["level5"], int):
            param.histoire["level5"] = 25000
            print("Error value: settings/histoire/level5")

        if param.histoire["texte_speed"] < 0 or not isinstance(param.histoire["texte_speed"], (int, float)):
            param.histoire["texte_speed"] = 1
            print("Error value: settings/histoire/texte_speed")

        if param.font["general_font_size"] < 0 or not isinstance(param.font["general_font_size"], int):
            param.font["general_font_size"] = 35
            print("Error value: settings/font/general_font_size")

        if param.font["menu_font_size1"] < 0 or not isinstance(param.font["menu_font_size1"], int):
            param.font["menu_font_size1"] = 40
            print("Error value: settings/font/menu_font_size1")

        if param.font["menu_font_size2"] < 0 or not isinstance(param.font["menu_font_size2"], int):
            param.font["menu_font_size2"] = 150
            print("Error value: settings/font/menu_font_size2")

        if param.font["dialogue_font_size"] < 0 or not isinstance(param.font["dialogue_font_size"], int):
            param.font["dialogue_font_size"] = 30
            print("Error value: settings/font/dialogue_font_size")

        if not isinstance(param.button["texte1"], str):
            param.button["texte1"] = "Jouer"
            print("Error value: settings/button/texte1")

        if not isinstance(param.button["texte2"], str):
            param.button["texte2"] = "Recommencer"
            print("Error value: settings/button/texte2")

        if not isinstance(param.button["texte3"], str):
            param.button["texte3"] = "Reprendre"
            print("Error value: settings/button/texte3")

        if not isinstance(param.button["texte4"], str):
            param.button["texte4"] = "Sauvegarder"
            print("Error value: settings/button/texte4")

        if not isinstance(param.button["texte5"], str):
            param.button["texte5"] = "Quitter"
            print("Error value: settings/button/texte5")

        if not isinstance(param.event["1"], str):
            param.event["1"] = "Projectile Fall"
            print("Error value: settings/event/1")

        if not isinstance(param.event["2"], str):
            param.event["2"] = "Blindness"
            print("Error value: settings/event/2")

        if not isinstance(param.event["3"], str):
            param.event["3"] = "Auto Walk"
            print("Error value: settings/event/3")


# Lancement du jeu
if __name__ == '__main__':
    pygame.init()
    Game().boucle()
    pygame.quit()
