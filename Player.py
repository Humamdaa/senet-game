import random

class Player:
    def __init__(self, name):
        self.name = name

    def roll_distance(self):
        return random.randint(1, 5)
