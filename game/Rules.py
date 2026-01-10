from game.SpecialSquareRules import SpecialSquareRules
class Rules:

    def move(board, cur_pos, dist):
        target = cur_pos + dist
        
        board.special_rules.update_last_roll(dist)
        
        source_cell = board.grid[cur_pos]
        target_cell = board.grid[target]
        '''
        # قبل الحركة: التحقق من العقوبة إذا تجنب الخروج
        moved_from_square = cur_pos + 1  # رقم المربع (ليس الفهرس)
        penalty_applied = board.special_rules.check_penalty_for_not_exiting(
            board.current_player, moved_from_square
        )
        
        # إذا طبقت عقوبة، لا ننفذ الحركة الأصلية
        if penalty_applied:
            board.switchPlayer()
            return
        '''


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
                
            elif target_cell.is_player_piece():
                print('player swap')
                source_val = source_cell.get_value()
                target_val = target_cell.get_value()
                source_cell.set_value(target_val)
                target_cell.set_value(source_val)
                
        board.counter-=1
        moved_from_square = cur_pos + 1
        penalty_applied = board.special_rules.check_penalty_for_not_exiting(
        board.current_player, moved_from_square)
        
        # ثانياً: التحقق من المربعات الخاصة بعد الحركة
        # board.special_rules.check_special_squares_after_move(board.current_player)
        
        # ثالثاً: تبديل اللاعب
        # board.switchPlayer()
    
    
    
    @staticmethod
    def checkMove(self, cur_pos, dist):
        # print(f"cur = {cur_pos}  dist = {dist}")
        
        if cur_pos < 0 or cur_pos >= 30:
            return False
            
        if self.grid[cur_pos].get_value() != self.current_player:
            return False
        
        target = cur_pos + dist
        '''
        here controll out peice 
        '''
        if self.grid[target].get_value() == self.current_player:
            return False
        
        if not self.special_rules.can_pass_happiness_house(cur_pos, dist):
            return False

        print('can move !')
        return True
