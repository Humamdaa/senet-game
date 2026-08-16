# modes/human_vs_ai.py
from game.GameState import GameState
from ai.ai_engine import AIEngine
from game.Render import Render
from Utils.RandomStep import Random
from game.Rules import Rules

class HumanVsAI:
    def __init__(self, board):
        self.board = board
        self.ai = AIEngine()
        self.ai.max_depth = 3
        self.rand = Random()

    def start(self):
        Render.draw_board(self.board.grid)
        while True:
            # دور الإنسان
            dist = self.rand.roll_distance()
            print(f"\n{self.board.get_current_player()} rolled: {dist}")
            user_input = input(f"Select piece to move (distance = {dist}) or press N to simulate: ").strip()
            if user_input.upper() == "N":
                Rules.show_simulations(self.board, dist)
            else:
                Rules.move(self.board, int(user_input)-1, dist)
            self.board.switchPlayer()

            # دور AI
            self._ai_turn(self.rand.roll_distance())

    def _ai_turn(self, dice_value):
        print("\n🤖 AI's turn")
        print(f"\n🤖 AI rolled: {dice_value}")  # ⬅️ هنا نطبع رقم الزهر
        state = GameState(self.board, "B")
        move = self.ai.decide_move(state, dice_value)
        if move:
            state.apply_move(move)
            Render.draw_board(self.board.grid)
            self.board.switchPlayer()
