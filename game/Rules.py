from game.SpecialSquareRules import SpecialSquareRules
class Rules:

    # @staticmethod
    def move1(board, cur_pos, dist):
        target = cur_pos + dist
        board.special_rules.update_last_roll(dist)

        source_cell = board.get_cell(cur_pos)
        target_cell = board.get_cell(target)

        if target_cell.is_empty():
            print('empty')
            target_cell.set_value(source_cell.get_value())
            source_cell.set_value('.')

        elif target_cell.is_special():
            print('special')
            pass

        elif target_cell.is_player_piece():
            print('player')
            source_val = source_cell.get_value()
            target_val = target_cell.get_value()
            source_cell.set_value(target_val)
            target_cell.set_value(source_val)
    def move(board, cur_pos, dist):
        target = cur_pos + dist
        
        # تحديث الرمية الأخيرة في قواعد المربعات الخاصة
        board.special_rules.update_last_roll(dist)
        
        source_cell = board.grid[cur_pos]
        target_cell = board.grid[target]

        # قبل الحركة: التحقق من العقوبة إذا تجنب الخروج
        moved_from_square = cur_pos + 1  # رقم المربع (ليس الفهرس)
        penalty_applied = board.special_rules.check_penalty_for_not_exiting(
            board.current_player, moved_from_square
        )
        
        # إذا طبقت عقوبة، لا ننفذ الحركة الأصلية
        if penalty_applied:
            board.switchPlayer()
            return
        


        # أولاً: التحقق من القواعد الخاصة
        is_special_handled = board.special_rules.handle_special_square(
            cur_pos, target, source_cell, target_cell, board.current_player
        )
        
        # إذا لم يكن المربع خاصاً، ننفذ الحركة العادية
        if not is_special_handled:
            print(f"Moving to normal square {target + 1}")
            
            if target_cell.is_empty():
                print('empty')
                target_cell.set_value(source_cell.get_value())
                source_cell.set_value('.')
                
            elif target_cell.is_special():
                # إذا كان المربع خاصاً ولكن لم يتعامل معه handle_special_square
                # (هذا لا يجب أن يحدث، لكنه احتياطي)
                print('special (fallback)')
                target_cell.set_value(source_cell.get_value())
                source_cell.set_value('.')
                
            elif target_cell.is_player_piece():
                print('player swap')
                source_val = source_cell.get_value()
                target_val = target_cell.get_value()
                source_cell.set_value(target_val)
                target_cell.set_value(source_val)
        
        # ثانياً: التحقق من المربعات الخاصة بعد الحركة
        board.special_rules.check_special_squares_after_move(board.current_player)
        
        # ثالثاً: تبديل اللاعب
        # board.switchPlayer()
    '''''
    
    '''
    @staticmethod
    def checkMove(self, cur_pos, dist):
        print(f"cur = {cur_pos}  dist = {dist}")
        
        # التحقق الأساسي من الحدود
        if cur_pos < 0 or cur_pos >= 30:
            return False
            
        if self.grid[cur_pos].get_value() != self.current_player:
            return False
        
        # حساب الهدف
        target = cur_pos + dist
        
        # إذا كان الهدف خارج اللوحة
        if target >= 30:
            # السماح فقط بالهبوط الدقيق على المربع 30
            if target > 30:
                print("❌ Need exact roll to exit (must land on square 30)")
                return False
            return True
        
        # تحقق من حدود الهدف
        if target < 0 or target >= 30:
            return False
            
        # تحقق من أن الهدف ليس فيه قطعة لنفس اللاعب
        if self.grid[target].get_value() == self.current_player:
            return False
        
        # التحقق من قاعدة بيت السعادة
        if not self.special_rules.can_pass_happiness_house(cur_pos, dist):
            return False

        print('can move !')
        return True
