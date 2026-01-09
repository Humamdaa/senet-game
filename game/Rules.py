class Rules:

    @staticmethod
    def move(board, cur_pos, dist):
        target = cur_pos + dist

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

    @staticmethod
    def checkMove(board, cur_pos, dist):

        if cur_pos < 0 or cur_pos >= len(board.grid):
            return False

        source = board.get_cell(cur_pos)
        target = board.get_cell(cur_pos + dist)

        print(f"current : {source.get_value()}, {board.get_current_player()}")

        if source.get_value() != board.get_current_player():
            print('source is not same current player')
            return False
        if target.get_value() == board.get_current_player():
            print('source is same target')
            return False

        return True
