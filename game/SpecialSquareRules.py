class SpecialSquareRules:
    def __init__(self, board):
        self.board = board
        self.last_roll = 0
        

        self.special_squares = {     
            26: "House of Happiness",    # بيت السعادة
            27: "House of Water",        # بيت الماء
            28: "House of Three Truths",  # بيت الحقائق الثلاث
            29: "House of Re-Atoum",     # بيت إعادة أتوم
            30: "House of Horus"         # بيت حورس
        }

    def update_last_roll(self, roll):
        self.last_roll = roll

    def handle_special_square(self, cur_pos, target, source_cell, target_cell, current_player):
        position = target + 1  
        
        if position not in self.special_squares:
            return False

        square_name = self.special_squares[position]
        print(f"\n⚠️ Special Square Detected: {square_name} (Square {position})")
        
        
        if position == 27:  # بيت الماء
            return self.handle_water_house(target, source_cell, current_player)
        elif position == 26:  # بيت السعادة
            return self.handle_happiness_house(cur_pos, target, source_cell, target_cell, current_player)
        elif position in [28,29,30]:  
            return self.last_three_houses(target, source_cell, target_cell, current_player)
        return False
    
    def handle_happiness_house(self, cur_pos, target, source_cell, target_cell, current_player):
        print("😊 House of Happiness: Must pass through directly")
        if target_cell.is_empty():
            target_cell.set_value(source_cell.get_value())
            source_cell.set_value('.')
        else:
            temp = source_cell.get_value()
            source_cell.set_value(target_cell.get_value())
            target_cell.set_value(temp)
        return True
    def handle_water_house(self, target, source_cell, current_player):
        """بيت الماء (27) - العودة فوراً إلى بيت البعث"""
        print("💧 House of Water: Returning to Rebirth House!")
        source_cell.set_value('.')  # إزالة القطعة من موقعها الأصلي

        # البحث عن أول مربع غير مشغول قبل المربع 15
        for square in range(14, -1, -1):  # من 14 إلى 0
            if self.board.grid[square].is_empty():
                print(
                    f"   ↪ Moving to square {square + 1} (before rebirth house)")
                self.board.grid[square].set_value(current_player)
                return True

        # إذا لم يوجد مربع فارغ، نذهب للمربع 15 نفسه
        print(f"   ↪ Moving directly to rebirth house (15)")
        self.board.grid[14].set_value(current_player)
        return True
    
    def last_three_houses(self, target, source_cell, target_cell, current_player):
        pos = target+1
        print("👁️ One of last three Houses : you should exit next turn ")

        target_cell.must_move_next_turn=True
        self.board.counter = 3 if not self.board.counter else self.board.counter
        
        if target_cell.is_empty():
            target_cell.set_value(source_cell.get_value())
            source_cell.set_value('.')
        else:
            temp = source_cell.get_value()
            source_cell.set_value(target_cell.get_value())
            target_cell.set_value(temp)

        return True

    def try_exit_from_special_square(self, cur_pos, current_player, dice_roll):
        target_num = cur_pos+dice_roll

        index_25= self.board.grid[25]
        print(f"index_25 {index_25.get_value()}  current_player = {current_player}  cur_pos = {cur_pos}  target_num {target_num}")
        if index_25.get_value()==current_player and cur_pos==26:
            if target_num>=31:
                print("exit from house of happenes")
                index_25.set_value('.')
                return True

        for  cell in self.board.grid[-3:]:
            if cell.get_value() == current_player and cell.must_move_next_turn:
                if target_num>=31:
                    print(f"✅ current_player {current_player} rolled 3 and exits from square 28 to off-board (31)")
                    cell.set_value('.')
                    cell.must_move_next_turn = False
                    return True
        return False

    def check_penalty_for_not_exiting(self, current_player, moved_from_square):
        for cell in self.board.grid[-3:]:
            if self.board.counter==0 and current_player == cell.value and cell.must_move_next_turn:
                self.apply_penalty(current_player,cell.pos+1)
                cell.must_move_next_turn=False
                return True
        return False

    def apply_penalty(self, player, square_number):
        square_index = square_number - 1 

        self.board.grid[square_index].set_value('.')
        for square in range(14, -1, -1): 
            if self.board.grid[square].is_empty():
                print(f"   ↪ Penalty: Moving back to square {square + 1}")
                self.board.grid[square].set_value(player)
                break
        else:
            print(f"   ↪ Penalty: Moving back to rebirth house (15)")
            self.board.grid[14].set_value(player)

    def can_pass_happiness_house(self, cur_pos, dist):

        target_pos = cur_pos + dist
        happiness_square = 25  # الفهرس 25 للمربع 26

        if cur_pos < happiness_square and target_pos > happiness_square:
            print(f"❌ Cannot jump over House of Happiness (square 26)")
            return False
        return True
