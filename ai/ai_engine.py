class AIEngine:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth

        # احتمالات النرد في Senet
        self.dice_probs = {
            1: 1 / 16,
            2: 4 / 16,
            3: 6 / 16,
            4: 4 / 16,
            5: 1 / 16
        }

    # ==========================================
    # ========== HEURISTIC FUNCTION ============
    # ==========================================
    def evaluate(self, state):
        score = 0

        board = state.board

        # ---------- التقدم على الرقعة ----------
        for cell in board.grid:
            if cell.get_value() == "B":      # AI
                score += cell.pos
            elif cell.get_value() == "A":    # Human
                score -= cell.pos

        # ---------- المربعات الخاصة ----------
        for cell in board.grid:
            if cell.get_value() == "B":
                if cell.pos == 26:
                    score += 6
                elif cell.pos == 27:
                    score -= 8
                elif cell.pos == 28:
                    score += 3
                elif cell.pos == 29:
                    score += 2
                elif cell.pos == 30:
                    score += 10

            elif cell.get_value() == "A":
                if cell.pos == 26:
                    score -= 6
                elif cell.pos == 27:
                    score += 8
                elif cell.pos == 28:
                    score -= 3
                elif cell.pos == 29:
                    score -= 2
                elif cell.pos == 30:
                    score -= 10

        return score

    # ==========================================
    # ========== DECIDE BEST MOVE ==============
    # ==========================================
    def decide_move(self, state, dice_value):
        best_move = None
        best_value = float("-inf")

        legal_moves = state.get_legal_moves(dice_value)

        if not legal_moves:
            return None

        for move in legal_moves:
            next_state = state.clone()
            next_state.apply_move(move)

            value = self.expectiminimax(
                next_state,
                self.max_depth - 1,
                "CHANCE"
            )

            if value > best_value:
                best_value = value
                best_move = move

        return best_move

    # ==========================================
    # ========== EXPECTIMINIMAX ================
    # ==========================================
    def expectiminimax(self, state, depth, node_type):

        if depth == 0 or state.is_terminal():
            return self.evaluate(state)

        # ---------- CHANCE NODE (Dice) ----------
        if node_type == "CHANCE":
            expected_value = 0

            for dice, prob in self.dice_probs.items():
                next_state = state.clone()
                next_state.dice_value = dice

                next_node = "MAX" if next_state.current_player == "B" else "MIN"

                value = self.expectiminimax(
                    next_state,
                    depth - 1,
                    next_node
                )

                expected_value += prob * value

            return expected_value

        # ---------- MAX NODE (AI) ----------
        if node_type == "MAX":
            best = float("-inf")
            moves = state.get_legal_moves(state.dice_value)

            if not moves:
                return self.evaluate(state)

            for move in moves:
                next_state = state.clone()
                next_state.apply_move(move)

                value = self.expectiminimax(
                    next_state,
                    depth - 1,
                    "CHANCE"
                )

                best = max(best, value)

            return best

        # ---------- MIN NODE (Human) ----------
        if node_type == "MIN":
            best = float("inf")
            moves = state.get_legal_moves(state.dice_value)

            if not moves:
                return self.evaluate(state)

            for move in moves:
                next_state = state.clone()
                next_state.apply_move(move)

                value = self.expectiminimax(
                    next_state,
                    depth - 1,
                    "CHANCE"
                )

                best = min(best, value)

            return best
