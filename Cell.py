class Cell:
    def __init__(self, pos, value):
        self.row = pos
        self.value = value

    def is_empty(self):
        return self.value == "."

    def get_value(self):
        return self.value

    def set_value(self, newVal):
        self.value = newVal
        
    def is_player_piece(self):
        return self.value in ["1", "2"]

    def is_special(self):
        return self.value in ["H", "W", "T", "R", "A", "E"]

    # def __repr__(self):
    #     return f"Cell({self.row}, {self.col}, '{self.value}')"

