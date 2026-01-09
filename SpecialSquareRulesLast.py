# SpecialSquareRules.py
class SpecialSquareRules:
    def __init__(self, board):
        self.board = board
        self.last_roll = 0
        self.piece_on_28 = None
        self.piece_on_29 = None
        self.piece_on_30 = None
        
        self.special_squares = {
            15: "House of Rebirth",      # بيت البعث
            26: "House of Happiness",    # بيت السعادة
            27: "House of Water",        # بيت الماء
            28: "House of Three Truths", # بيت الحقائق الثلاث
            29: "House of Re-Atoum",     # بيت إعادة أتوم
            30: "House of Horus"         # بيت حورس
        }
    
    def update_last_roll(self, roll):
        """تحديث الرمية الأخيرة"""
        self.last_roll = roll
    
    def handle_special_square(self, cur_pos, target, source_cell, target_cell, current_player):
        """
        التعامل مع المربعات الخاصة فقط
        يرجع True إذا كان المربع خاصاً وتم التعامل معه
        يرجع False إذا كان المربع عادياً
        """
        position = target + 1  # تحويل الفهرس إلى رقم المربع
        
        # إذا لم يكن المربع خاصاً، لا نتعامل معه
        if position not in self.special_squares:
            return False
        
        square_name = self.special_squares[position]
        print(f"\n⚠️ Special Square Detected: {square_name} (Square {position})")
        
        # التعامل مع كل مربع خاص حسب قواعده
        if position == 15:  # بيت البعث
            return self.handle_rebirth_house(target, target_cell, source_cell, current_player)
        
        elif position == 26:  # بيت السعادة
            return self.handle_happiness_house(cur_pos, target, source_cell, target_cell, current_player)
        
        elif position == 27:  # بيت الماء
            return self.handle_water_house(target, source_cell, current_player)
        
        elif position == 28:  # بيت الحقائق الثلاث
            return self.handle_three_truths(target, source_cell, target_cell, current_player)
        
        elif position == 29:  # بيت إعادة أتوم
            return self.handle_re_atoum(target, source_cell, target_cell, current_player)
        
        elif position == 30:  # بيت حورس
            return self.handle_horus_house(target, source_cell, target_cell, current_player)
        
        return False
    
    def handle_rebirth_house(self, target, target_cell, source_cell, current_player):
        """بيت البعث (15)"""
        print("🏠 House of Rebirth: Checking for empty squares before...")
        
        # البحث عن أول مربع غير مشغول قبل المربع 15
        for square in range(14, -1, -1):  # من 14 إلى 0
            if self.board.grid[square].is_empty():
                print(f"   ↪ Moving to empty square {square + 1} instead")
                self.board.grid[square].set_value(source_cell.get_value())
                source_cell.set_value('.')
                return True
        
        # إذا لم يوجد مربع فارغ، نذهب للمربع 15 نفسه
        print(f"   ↪ Moving directly to rebirth house (15)")
        target_cell.set_value(source_cell.get_value())
        source_cell.set_value('.')
        return True
    
    def handle_happiness_house(self, cur_pos, target, source_cell, target_cell, current_player):
        """بيت السعادة (26) - لا يمكن القفز فوقه"""
        print("😊 House of Happiness: Must pass through directly")
        
        # حركة عادية (لا توجد قواعد خاصة للهبوط عليه)
        target_cell.set_value(source_cell.get_value())
        source_cell.set_value('.')
        return True
    
    def handle_water_house(self, target, source_cell, current_player):
        """بيت الماء (27) - العودة فوراً إلى بيت البعث"""
        print("💧 House of Water: Returning to Rebirth House!")
        source_cell.set_value('.')  # إزالة القطعة من موقعها الأصلي
        
        # البحث عن أول مربع غير مشغول قبل المربع 15
        for square in range(14, -1, -1):  # من 14 إلى 0
            if self.board.grid[square].is_empty():
                print(f"   ↪ Moving to square {square + 1} (before rebirth house)")
                self.board.grid[square].set_value(current_player)
                return True
        
        # إذا لم يوجد مربع فارغ، نذهب للمربع 15 نفسه
        print(f"   ↪ Moving directly to rebirth house (15)")
        self.board.grid[14].set_value(current_player)
        return True
    
    def handle_three_truths(self, target, source_cell, target_cell, current_player):
        """بيت الحقائق الثلاث (28)"""
        print("🔺 House of Three Truths: Need 3 on next turn to exit")
        
        # تسجيل أن هناك قطعة على المربع 28
        self.piece_on_28 = current_player
        
        # حركة عادية
        if target_cell.is_empty():
            target_cell.set_value(source_cell.get_value())
            source_cell.set_value('.')
        else:
            # إذا كان فيه قطعة أخرى، تبادل
            temp = source_cell.get_value()
            source_cell.set_value(target_cell.get_value())
            target_cell.set_value(temp)
        
        return True
    
    def handle_re_atoum(self, target, source_cell, target_cell, current_player):
        """بيت إعادة أتوم (29)"""
        print("🔄 House of Re-Atoum: Need 2 on next turn to exit")
        
        # تسجيل أن هناك قطعة على المربع 29
        self.piece_on_29 = current_player
        
        # حركة عادية
        if target_cell.is_empty():
            target_cell.set_value(source_cell.get_value())
            source_cell.set_value('.')
        else:
            # إذا كان فيه قطعة أخرى، تبادل
            temp = source_cell.get_value()
            source_cell.set_value(target_cell.get_value())
            target_cell.set_value(temp)
        
        return True
    
    def handle_horus_house(self, target, source_cell, target_cell, current_player):
        """بيت حورس (30) - يمكن الخروج بأي رمية"""
        print("👁️ House of Horus: Can exit with any roll")
        
        # تسجيل أن هناك قطعة على المربع 30
        self.piece_on_30 = current_player
        
        # حركة عادية
        if target_cell.is_empty():
            target_cell.set_value(source_cell.get_value())
            source_cell.set_value('.')
        else:
            # إذا كان فيه قطعة أخرى، تبادل
            temp = source_cell.get_value()
            source_cell.set_value(target_cell.get_value())
            target_cell.set_value(temp)
        
        return True
    
    def check_special_squares_after_move(self, current_player):
        """
        التحقق من القطع على المربعات الخاصة بعد كل حركة
        يتم استدعاؤها بعد كل حركة
        """
        self.check_piece_on_28(current_player)
        self.check_piece_on_29(current_player)
        self.check_piece_on_30(current_player)
    
    def check_piece_on_28(self, current_player):
        """التحقق من القطعة على المربع 28 (بيت الحقائق الثلاث)"""
        if self.piece_on_28 and self.last_roll == 3:
            # إذا كانت هناك قطعة على 28 واللاعب رمى 3
            print(f"\n🎲 Player {self.piece_on_28} rolled 3! Piece exits from square 28!")
            # إزالة القطعة من المربع 28 (المؤشر 27)
            self.board.grid[27].set_value('.')
            self.piece_on_28 = None
    
    def check_piece_on_29(self, current_player):
        """التحقق من القطعة على المربع 29 (بيت إعادة أتوم)"""
        if self.piece_on_29 and self.last_roll == 2:
            # إذا كانت هناك قطعة على 29 واللاعب رمى 2
            print(f"\n🎲 Player {self.piece_on_29} rolled 2! Piece exits from square 29!")
            # إزالة القطعة من المربع 29 (المؤشر 28)
            self.board.grid[28].set_value('.')
            self.piece_on_29 = None
    
    def check_piece_on_30(self, current_player):
        """التحقق من القطعة على المربع 30 (بيت حورس)"""
        if self.piece_on_30 and self.last_roll > 0:
            # إذا كانت هناك قطعة على 30 واللاعب رمى أي رقم
            print(f"\n🎲 Player {self.piece_on_30} can exit from square 30!")
            # إزالة القطعة من المربع 30 (المؤشر 29)
            self.board.grid[29].set_value('.')
            self.piece_on_30 = None
    
    def can_pass_happiness_house(self, cur_pos, dist):
        """
        التحقق من قاعدة بيت السعادة (لا يمكن القفز فوق المربع 26)
        يمكن استدعاؤها من checkMove في Board
        """
        target_pos = cur_pos + dist
        happiness_square = 25  # الفهرس 25 للمربع 26
        
        # إذا كنا قبل المربع 26 والهدف بعده
        if cur_pos < happiness_square and target_pos > happiness_square + 1:
            print(f"❌ Cannot jump over House of Happiness (square 26)")
            return False
        return True