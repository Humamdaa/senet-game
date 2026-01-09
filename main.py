from game.Board import Board
from modes.HumanVsHuman import HumanVsHuman
from game.Render import Render

import json


def load_levels(path="levels.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["levels"]


levels = load_levels()

level1 = levels[0]


board = Board(level1)


print()
print('1- Human vs Human')
print('2- Human vs Human')
choose = int(input('select type of game: '))


if choose == 1:
    game = HumanVsHuman(board)
    game.start()
