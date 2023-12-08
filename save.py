import csv

from settings import Settings

param = Settings()


class Save:
    def __init__(self, game):
        """
        Souvegarde du jeu
        :param game: Class du jeu
        """
        self.game = game
        self.save = {}
        self.read_save()

    def read_save(self):
        """
        Lit le contenu de la souvegarde du jeu
        """
        fichier = open(param.game['save'], 'r')
        if not list(csv.DictReader(fichier, delimiter=',')):
            self.reset_save()
        fichier.close()

        fichier = open(param.game['save'], 'r')
        self.save = list(csv.DictReader(fichier, delimiter=','))
        self.save = self.convert(self.save[0])
        fichier.close()

    def convert(self, dico):
        """
        Transforme les valeur du disctionnaire en int
        :param dico: (dict) disctionnaire a transformer
        :return: (dict) dictionnaire avec les valeurs en int
        """
        vie = int(dico["vie"])
        level = int(dico["level"])
        score = int(dico["score"])
        total_score = int(dico["total_score"])
        game_score = int(dico["game_score"])
        histoire = int(dico["histoire"])
        game_time = int(dico["game_time"])
        return {'vie': vie, 'level': level, 'score': score, 'total_score': total_score, 'game_score': game_score,'histoire': bool(histoire), 'game_time': game_time}

    def get_save(self):
        """
        Recuperer les donnees de la souvegarde du jeu
        :return: (list) liste de disctionnaire
        """
        return self.save

    def do_save(self):
        """
        Fait une souvegarde du jeu
        """
        with open(param.game['save'], 'w') as fichier:
            obj = csv.DictWriter(fichier, fieldnames=["vie", "level", "score", "total_score", "game_score", "histoire", "game_time"])
            obj.writeheader()
            obj.writerow({'vie': self.game.player.health, 'level': self.game.histoire.get_level(), 'score': self.game.histoire.score, "total_score": self.game.histoire.total_score, "game_score": self.game.histoire.game_score, "histoire": int(self.game.histoire.start_histoire), "game_time": self.game.secondes})

    def reset_save(self):
        """
        Reset les donnees de la souvegarde du jeu
        """
        with open(param.game['save'], 'w') as fichier:
            obj = csv.DictWriter(fichier, fieldnames=["vie", "level", "score", "total_score", "game_score", "histoire", "game_time"])
            obj.writeheader()
            obj.writerow({'vie': param.player["health"], 'level': param.histoire["level"], 'score': param.histoire["base_score"], "total_score": param.histoire["base_score"], "game_score": param.histoire["game_score"], "histoire": 0, "game_time": 0})
        self.read_save()
