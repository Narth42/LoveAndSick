# coding=utf-8
class Settings:
    def __init__(self):
        """
        Parametre du jeu
        """
        # Les valeurs avec un # derrier peuvent etre changer sans risque /!\ toutes les valeurs numerique doivent etre positives
        # /!\ Des changements deconseilles pourront entrainer un disfonctionnement du jeu ou meme un crash de celui-ci

        self.generale = {
            "titre": "Lovesick",
            "version": "Beta - 1.5"
        }

        self.game = {
            "fps": 60, # 60
            "taille_fenetre": (1300, 750),
            "music_level": 0.1, # 0.1
            "sound_level": 0.2, # 0.2
            "save": "save.csv"
        }

        self.button = {
            "size": (400, 130),

            "start": 1,
            "restart": 2,
            "resume": 3,
            "save": 4,
            "exit": 5,

            "texte1": "Jouer", # "Jouer" (str)
            "texte2": "Recommencer", # "Recommencer" (str)
            "texte3": "Reprendre", # "Reprendre" (str)
            "texte4": "Sauvegarder", # "Sauvegarder" (str)
            "texte5": "Quitter" # "Quitter" (str)
        }

        self.font = {
            "general_font_size": 35, # 35
            "menu_font_size1": 40, # 40
            "menu_font_size2": 150, # 150
            "dialogue_font_size": 30, # 30

            "general_font": "font/general_font.ttf",
            "menu_font1": "font/menu_font1.ttf",
            "menu_font2": "font/menu_font2.ttf",
            "dialogue_font": "font/dialogue_font.ttf"
        }

        self.dialogue = {
            # Exemple
            # speaker = 0 : Guide
            # speaker = 1 : Saiko
            # speaker = 2 : Masahiro
            # speaker = 3 : Kaguya
            # speaker = 4 : Bakubaku
            # [(texte1, speaker=1), (texte2, speaker=3)]
            "dialogue0": [
                ("Narrateur: Au coeur de la foret, vivait Saiko une jeune  "
                 "fille orpheline qui avait trouve refuge chez Masahiro un "
                 "jeune garcon qui l'avait eleve comme sa propre soeur.    "
                 "Mais ce lien qui les unissait ne lui plaisait pas elle   "
                 "voulais etre plus que ca. Elle qui passait son temps a   "
                 "l'admirer de loin  souhaitait plus que tout que celui-ci "
                 "l'a remarque par tout les moyens possibles.              "
                 "Malheureusement, le destin lui avait complique la tache.", 0),

                ("Kaguya: J'aurais pu finir noyer mais tu t'es jette a     "
                 "l'eau pour me sauver. Mon cher Masahiro, j'aimerais te   "
                 "remercie en t'invitant a mon chateau pour apprendre a te "
                 "connaitre.", 3),

                ("Masahiro: ...", 2),

                ("Kaguya: Je prends ton silence pour un oui.", 3),

                ("Narrateur: Plus loin dans la foret", 0),

                ("Saiko: Masahiro c'est toi ? Qui es-tu et qui te donne le "
                 "droit de toucher aux affaires de Masahiro ?", 1),

                ("Bakubaku: Je suis sous les ordre de la princesse Kaguya.", 4),

                ("Saiko: Pourquoi la princesse s'interesse t'elle a lui ?", 1),

                ("Bakubaku: Monsieur masahiro a sauver notre pricesse et   "
                 "pour le recompenser elle a inviter monsieur masahiro a   "
                 "vivre au chateau.", 4),

                ("Saiko *pense*: Vivre ? Elle souhaite l'epouser ? Elle me "
                 "l'a arracher a moi ? Moi qui n'est rien alors qu'elle a  "
                 "deja tout ce qu'elle souhaite ? Que cette fille est      "
                 "odieuse et avide ! J'aimerai voir son souffle s'arreter  "
                 "lorsque je prendra son cou entre mes mains... Je dois    "
                 "l'arreter a commencer par ces gentilles petits           "
                 "serviteurs.", 1),

                ("Guide: Bienvenu sur LoveSick, je suis ton guide et je    "
                 "t'aiderais tout au long de ton aventure. Pour commencer  "
                 "je vais te montrer quelques touches utiles. Retient les  "
                 "bien, je ne les repeterais pas !", 0),

                ("Une fois l'aventure debute, appuis sur la touche <d> pour"
                 "te deplacer vers la droite et la touche <q> pour te      "
                 "deplacer vers la gauche. Tu pourra aussi effectuer un    "
                 "saut en appuyant sur la touche <espace>.", 0),

                ("Tu pourra aussi appuyer sur la touche <echap> pour ouvrir"
                 "le menu de pause. Tu pourra ainsi sauvegarder ton        "
                 "avancement ou bien quitter le jeu.                       "
                 ""
                 "Ce sera tout pour le moment. Je te souhaite bonne chance "
                 "et j'espere qu'on se reverra bientot", 0)
            ],
            "dialogue1": [
                ("Saiko *pense*: Ma quete pour sauver masahiro vient tout  "
                 "juste de commencer, il faut que j'y parvienne coute que  "
                 "coute. Je pense qu cela va pouvoir m'aider", 1),

                ("Guide: Bien jouer, tu viens de ramasser l'objet arme.    "
                 "Tu peux maintenant effectuer des tirs en appuyant sur la "
                 "touche <e>.", 0)
            ],
            "dialogue2": [
                ("Kaguya: eh toi ! qui est vous ? et pourquoi tuez vous    "
                 "tout mes Bakubaku ?", 3),

                ("Saiko : Je suis Saiko et ce sont mes ennemi, il me gene  "
                 "pour ma quête !", 1),

                ("Kaguya : Mais quelle est votre quete pour devoir tous les"
                 "sacrifier ? ", 3),

                ("Saiko *pense*: Je doit sauver Masahiro.", 1)
            ],
            "dialogue3": [
                ("kaguya : Saiko, tu ne ma pas dit qu'elle etait ta quete, "
                 "je suis la pour t'aider", 3),

                ("Saiko : Masahiro, c'est lui ma quete, vous le retener    "
                 "prisonier, vous me l'avez enleve !", 1),

                ("kaguya : Il n'est pas prisonier, il a une vie juste plus "
                 "confortable tu devrais etre heureuse pour lui.", 3)
            ],
            "dialogue4": [
                ("Saiko *pense*: J'y suis bientot, Masahiro je te          "
                 "libererais !", 1)
            ],
            "dialogue5": [
                ("Kaguya: Tu as tue tous mes gardes pour ton ami. Pour quel"
                 "raison, n'aurais-je pas le droit d'apprendre a le        "
                 "connaitre ?", 3),

                ("Saiko: Il n'y a pas de nous ! Masahiro ne t'appartiens   "
                 "pas et ton existence n'a aucune importance a mes yeux.", 1),

                ("Kaguya: Il ne t'appartient pas non plus.", 3),

                ("Saiko: Quand je t'aurais elimine plus rien ne me genera  "
                 "pour que ce soit le cas.", 1)
            ],
            "dialogue6": [
                ("Saiko: Masahiro ! Tu vas bien ?", 1),

                ("Masahiro *acquiesce*: Tu n'aurais pas vu la princesse de "
                 "ce château, je comptais rentrer mais j'aimerais l'a      "
                 "remercie pour son hospitalite avant.", 2),

                ("Saiko : Elle n'est plus de ce monde, pour toi,           "
                 "pour nous...", 1),

                ("Masahiro : Qu'es-ce qui c'est passer ?", 2),

                ("Saiko : Je ne sais pas, je l'ai trouver allonger et      "
                 "sans vie", 1),

                ("Masahiro: Elle m'avait prevenue que des ennemies du      "
                 "royaume s'en prendront a elle je suppose qu'ils ont du   "
                 "attaquer le chateau en mon absence.", 2),

                ("Saiko : Ca doit etre ca, maintenant rentrons a la maison "
                 "tout les deux.", 1),

                ("Masahiro: Ca tombe bien je commence à avoir faim.", 2),

                ("Guide: Felicitation, tu as fini le jeu !", 0)
            ],

            "id_zone": 1,
            "id_saiko": 2,
            "id_masahiro": 3,
            "id_kaguya": 4,

            "saiko_size": (300, 500),
            "masahiro_size": (300, 500),
            "kaguya_size": (300, 500),
            "bakubaku_size": (300, 390)
        }

        self.histoire = {
            "base_score": 0, # 0
            "game_score": 0, # 0
            "level": 1, # 1  /!\ 1 >= level <= 5

            "level1": 15000, # 15000
            "level2": 17000, # 17000
            "level3": 20000, # 20000
            "level4": 23000, # 23000
            "level5": 25000, # 25000

            "texte_fin": ["Bien jouer !!!",
                          "Vous avez fini avec brio Lovesick",
                          "N'hesitez pas recomencer l'aventure pour ameliorer votre",
                          "score et votre temps.",
                          "",
                          "",
                          "Scenariste : GERARD Noe",
                          "Graphiste : ALI ABDALLAH Assia, ROUSSEL Lola Jocelyne",
                          "Sound Designer : ROUSSEL Lola Jocelyne",
                          "Developpeur : HIRTH Nathan",
                          "Tester : GERARD Noe",
                          "",
                          "",
                          "Merci d'avoir jouer !"],

            "texte_speed": 1 # 1
        }

        self.player = {
            "health": 5, # 5
            "speed": 5, # 5
            "jump": 6.5, # 6.5
            "size": (40, 90), # (40, 90)
            "image_player_shoot_size": (60, 90), # (60, 90)

            # (attack_speed : int, damage : int, attack_distance : int)
            "weapon": (5, 1, 3), # (5, 1, 3)
            "shoot_speed": 25 # 25
        }

        self.plateforme = {
            "base_plateforme_size": (130, 350),
            "fly_plateforme_size": (80, 20),

            "start_plateforme": (1, 0),
            "base_plateforme": (1, 1),
            "base_fly_plateforme": (2, 0),
            "fly_plateforme": (2, 1),
            "break_plateforme": (2, 2),
            "ice_plateforme": (2, 3),
            "move_splateforme": (2, 4)
        }

        self.enemy = {
            # (health, attack_distance, speed, size)
            "boss": (300, 5, 3, (100, 136)), # (300, 5, 3, (100, 136))
            "bakubaku": (2, 5, 2, (45, 63)), # (2, 5, 2, (45, 63))
        }

        self.event = {
            "time": 15000, # 15000

            "1": "Projectile Fall", # "Projectile Fall" (str)
            "2": "Blindness", # "Blindness" (str)
            "3": "Auto Walk" # "Auto Walk" (str)
        }

        self.sound = {
            "background_sound": "sound/sound.ogg",
            "shoot_sound": "sound/shoot.ogg",
            "jump_sound": "sound/jump.ogg",
            "click_sound": "sound/click.ogg",
            "death_sound": "sound/death.ogg"
        }

        self.images = {
            # Background Images
            "background": "images/background.png",
            "dark_background": "images/dark_background.png",
            "blindness": "images/blindness.png",
            "blindness2": "images/blindness2.png",

            # Projectile Images
            "projectile": "images/bullet.png",
            "event": "images/fall_knife.png",

            # Text Images
            "text_support": "images/text_support.png",
            "dialogue_support": "images/dialogue_support.png",
            "button": "images/button.png",

            # Player Images
            "player": "images/player.png",

            "player_saut1": "images/player/player_saut1.png",
            "player_saut2": "images/player/player_saut2.png",
            "player_shoot1": "images/player/player_arme1.png",
            "player_shoot2": "images/player/player_arme2.png",
            "player_death1": "images/player/player_death1.png",
            "player_death2": "images/player/player_death2.png",

            "player1_1": "images/player/player1_1.png",
            "player1_2": "images/player/player1_2.png",
            "player1_3": "images/player/player1_3.png",
            "player1_4": "images/player/player1_4.png",
            "player1_5": "images/player/player1_5.png",
            "player1_6": "images/player/player1_6.png",
            "player1_7": "images/player/player1_7.png",
            "player1_8": "images/player/player1_8.png",
            "player1_9": "images/player/player1_9.png",

            "player2_1": "images/player/player2_1.png",
            "player2_2": "images/player/player2_2.png",
            "player2_3": "images/player/player2_3.png",
            "player2_4": "images/player/player2_4.png",
            "player2_5": "images/player/player2_5.png",
            "player2_6": "images/player/player2_6.png",
            "player2_7": "images/player/player2_7.png",
            "player2_8": "images/player/player2_8.png",
            "player2_9": "images/player/player2_9.png",

            # BakuBaku Images
            "bakubaku": "images/bakubaku.png",

            "bakubaku1_1": "images/bakubaku/bakubaku1_1.png",
            "bakubaku1_2": "images/bakubaku/bakubaku1_2.png",
            "bakubaku1_3": "images/bakubaku/bakubaku1_3.png",
            "bakubaku1_4": "images/bakubaku/bakubaku1_4.png",
            "bakubaku1_5": "images/bakubaku/bakubaku1_5.png",
            "bakubaku1_6": "images/bakubaku/bakubaku1_6.png",
            "bakubaku1_7": "images/bakubaku/bakubaku1_7.png",
            "bakubaku1_8": "images/bakubaku/bakubaku1_8.png",
            "bakubaku1_9": "images/bakubaku/bakubaku1_9.png",

            "bakubaku2_1": "images/bakubaku/bakubaku2_1.png",
            "bakubaku2_2": "images/bakubaku/bakubaku2_2.png",
            "bakubaku2_3": "images/bakubaku/bakubaku2_3.png",
            "bakubaku2_4": "images/bakubaku/bakubaku2_4.png",
            "bakubaku2_5": "images/bakubaku/bakubaku2_5.png",
            "bakubaku2_6": "images/bakubaku/bakubaku2_6.png",
            "bakubaku2_7": "images/bakubaku/bakubaku2_7.png",
            "bakubaku2_8": "images/bakubaku/bakubaku2_8.png",
            "bakubaku2_9": "images/bakubaku/bakubaku2_9.png",

            # Explosion Images
            "explosion1": "images/explosion/explosion1.png",
            "explosion2": "images/explosion/explosion2.png",
            "explosion3": "images/explosion/explosion3.png",
            "explosion4": "images/explosion/explosion4.png",
            "explosion5": "images/explosion/explosion5.png",

            # Boss Images
            "boss": "images/boss.png",

            # Masahiro
            "masahiro": "images/masahiro.png",

            # Plateforme Images
            "plateforme1": "images/plateforme/plateforme1.png",
            "plateforme2": "images/plateforme/plateforme2.png",
            "plateforme3": "images/plateforme/plateforme3.png",
            "plateforme4": "images/plateforme/plateforme4.png",
            "plateforme5": "images/plateforme/plateforme5.png",

            "flyplateforme1": "images/plateforme/flyplateforme1.png",
            "flyplateforme2": "images/plateforme/flyplateforme2.png",
            "flyplateforme3": "images/plateforme/flyplateforme3.png",
            "flyplateforme4": "images/plateforme/flyplateforme4.png",
            "flyplateforme5": "images/plateforme/flyplateforme5.png",

            "breakplateforme1": "images/plateforme/breakplateforme1.png",
            "breakplateforme2": "images/plateforme/breakplateforme2.png",
            "breakplateforme3": "images/plateforme/breakplateforme3.png",
            "breakplateforme4": "images/plateforme/breakplateforme4.png",
            "breakplateforme5": "images/plateforme/breakplateforme5.png",

            "iceplateforme": "images/plateforme/iceplateforme.png",

            # Deco Images
            "deco1": "images/deco/1.png",
            "deco2": "images/deco/2.png",
            "deco3": "images/deco/3.png",
            "deco4": "images/deco/4.png",
            "deco5": "images/deco/5.png",
            "deco6": "images/deco/6.png",
            "deco7": "images/deco/7.png",

            # Boost Images
            "vie": "images/boost/vie.png",
            "speed": "images/boost/speed.png",
            "jump": "images/boost/jump.png"
        }
