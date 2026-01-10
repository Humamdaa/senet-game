from utils.RandomStep import Random
from game.Board import Board
from game.Rules import Rules
from game.Render import Render


class HumanVsHuman:
    def __init__(self, board):
        self.board: Board = board
        self.rand = Random()

    def start(self):
        Render.draw_board(self.board.grid)

        while True:
            dist = self.rand.roll_distance()

            while True:
                print('\n', '='*50,
                      f"\n {self.board.get_current_player()} can move {dist} cells")

                cur_pos = input('select the piece to move : ')
                if cur_pos.strip() == '':
                    print("You must enter a number!")
                    continue
                else:
                    cur_pos = int(cur_pos)

                if Rules.checkMove(self.board, cur_pos - 1, dist):
                    Rules.move(self.board, cur_pos - 1, dist)
                    Render.draw_board(self.board.grid)
                    self.board.switchPlayer()
                    break
                print('try again my dear')
