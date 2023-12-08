import pygame

from settings import Settings

param = Settings()


class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, current_class, name, size):
        """
        Anime un element du jeu
        :param current_class: (Class) l'element a anime
        :param name: (str) nom de l'element a anime
        :param size: (tuple) taille de l'element a anime
        """
        super(AnimateSprite, self).__init__()
        self.current_class = current_class
        self.size = size
        self.name = name
        self.image = pygame.image.load(param.images[self.name]).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.current_image = 0
        self.time = 0
        self.images = animations.get(self.name + "1")
        self.animation = False

    def start_animation(self):
        """
        Demarrage de l'animation
        """
        self.animation = True

    def animate(self, loop=False):
        """
        Anime un enlement du jeu
        :param loop: (bool) Si l'animation se fait en boucle
        """
        if self.animation:
            self.time += 1

            if self.name == 'bakubaku' and self.current_class.direction == 0:
                timer = self.time % 10
            else:
                timer = self.time % 4

            # Change d'image tout les 4 tours de boucle
            if timer == 0:

                self.current_image += 1

                # Si l'animation est arrivee a la fin
                if self.current_image >= len(self.images):
                    self.current_image = 0
                    self.time = 0

                    if loop is False:
                        self.animation = False

                # Change l'image
                self.image = self.images[self.current_image].convert_alpha()
                self.image = pygame.transform.scale(self.image, self.size)

    def player_jump(self):
        """
        Animation du joueur quand il saute
        """
        self.animation = False
        if self.current_class.direction == 1:
            self.image = pygame.image.load(param.images["player_saut1"]).convert_alpha()
        else:
            self.image = pygame.image.load(param.images["player_saut2"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

    def player_shoot(self):
        """
        Animation du joueur quand il tire
        """
        self.animation = False
        if self.current_class.direction == 1:
            self.image = pygame.image.load(param.images["player_shoot1"]).convert_alpha()
        else:
            self.image = pygame.image.load(param.images["player_shoot2"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, param.player["image_player_shoot_size"])

    def player_death(self):
        """
        Animation du joueur quand il perd une vie
        """
        self.animation = False
        if self.current_class.direction == 1:
            self.image = pygame.image.load(param.images["player_death1"]).convert_alpha()
        else:
            self.image = pygame.image.load(param.images["player_death2"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

    def change_direction(self):
        """
        Change l'animation en fonction de la direction de l'element
        """
        if len(self.images) == 1:
            self.image = animations.get(self.name + str(self.current_class.direction))[0].convert_alpha()
            self.image = pygame.transform.scale(self.image, self.size)
        else:
            self.images = animations.get(self.name + str(self.current_class.direction))

    def set_size(self, new_size):
        """
        Change la taille de l'image
        :param new_size: (tuple) Nouvelle taille
        """
        self.size = new_size


# Generation des images
def load_animation_images(name, nb):
    images = []
    for num in range(1, nb):
        image_path = param.images[name + str(num)]
        images.append(pygame.image.load(image_path))
    return images

# Image a generer
animations = {
    'bakubaku1': load_animation_images('bakubaku1_', 9),
    'bakubaku-1': load_animation_images('bakubaku2_', 9),
    'bakubaku0': load_animation_images('explosion', 5),
    'player1': load_animation_images('player1_', 9),
    'player-1': load_animation_images('player2_', 9),
    'boss1': [pygame.image.load(param.images['boss'])]
}