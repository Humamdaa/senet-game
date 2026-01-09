from Board import Board
<<<<<<< Updated upstream
=======
# from Board2 import Board

>>>>>>> Stashed changes
from Player import Player

import json


def load_levels(path="levels.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["levels"]


levels = load_levels()

level1 = levels[0]


board = Board(level1)

board.draw_board()

player1 = Player('A')
player2 = Player('B')

while True:
    if board.get_current_player() == 'A':

        dist = player2.roll_distance()

        print('\n', '='*50, f"\n A can move {dist} cells")
        cur_pos = int(input('select the piece to move : '))

        board.move(cur_pos - 1, dist)

        board.draw_board()
<<<<<<< Updated upstream
        print()
        print()
        board.draw_board()

    print(board.get_current_player())
=======
        # print()
        # print()
        # board.draw_board()
    else:
        break
    print()
    # print(board.get_current_player())
>>>>>>> Stashed changes
    # player1.roll_distance()
