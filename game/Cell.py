class Cell:
    def __init__(self, pos, value):
        self.pos = pos
        self.value = value
        self.special = None
        if self.value in ["H", "W", "T", "R", "P", "E"]:
            self.special = self.value
            # self.value='.'

    def is_empty(self):
        return self.value == "." or self.value in ["H", "W", "T", "R", "P", "E"]

    def get_value(self):
        return self.value

    def set_value(self, newVal):
        if newVal=='.' and self.is_special():
            self.value=self.special
            print('retttt')
            return 
        self.value = newVal
        
    def is_player_piece(self):
        return self.value in ["A", "B"]

    def is_special(self):
        return self.special is not None

