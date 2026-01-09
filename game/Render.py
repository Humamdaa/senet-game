class Render:

    @staticmethod
    def draw_board(grid):
        for i in range(1, 11):
            print(i, end=" ")
        data = list(grid)
        result = data[:10] + list(reversed(data[10:20])) + data[20:]
        for i, cell in enumerate(result):
            if i % 10 == 0:
                print()
            print(cell.get_value(), end=" ")
