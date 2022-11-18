import sys
from random import shuffle
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QGridLayout

colors = {
    1: 'blue',
    2: 'green',
    3: 'red',
    4: 'dark blue',
    5: 'dark red'
}


class Button(QPushButton):
    def __repr__(self):
        return f'My button {self.x} {self.y} {self.number} ({self.is_mine})'

    def __init__(self, x, y, number):
        super(Button, self).__init__()
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_mines = 0
        self.is_open = False


class MineSweeper(QWidget):
    ROW = 10
    COLUMNS = 10
    MINES = 10
    IS_GAME_OVER = False

    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        layout.setHorizontalSpacing(1)
        layout.setVerticalSpacing(1)
        self.setLayout(layout)

        self.buttons = []

        count = 1

        for i in range(MineSweeper.ROW):
            temp = []
            for j in range(MineSweeper.COLUMNS):
                btn = Button(x=i, y=j, number=count)
                self.layout().addWidget(btn, i, j)
                temp.append(btn)
                count += 1
            self.buttons.append(temp)

    @staticmethod
    def right_click(event):

        if MineSweeper.IS_GAME_OVER:
            return

        cur_btn = event.widget
        if cur_btn['state'] == 'normal' and 0 < MineSweeper.MINES <= 10:
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '🚩'
            MineSweeper.MINES -= 1
        elif cur_btn['text'] == '🚩':
            cur_btn['text'] = ''
            cur_btn['state'] = 'normal'
            MineSweeper.MINES += 1

    def click(self, clicked_button: Button):

        if MineSweeper.IS_GAME_OVER:
            return

        if clicked_button.is_mine:
            clicked_button.config(text='*', background='red', disabledforeground='black')
            clicked_button.is_open = True
            MineSweeper.IS_GAME_OVER = True
            for i in range(1, MineSweeper.ROW + 1):
                for j in range(1, MineSweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'
        else:
            color = colors.get(clicked_button.count_mines, 'black')
            if clicked_button.count_mines:
                clicked_button.config(text=clicked_button.count_mines, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)

    def breadth_first_search(self, btn: Button):
        queue = [btn]
        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_mines, 'black')
            if cur_btn.count_mines:
                cur_btn.config(text=cur_btn.count_mines, disabledforeground=color)
                cur_btn.is_open = True
            else:
                cur_btn.config(text='', disabledforeground=color)
                cur_btn.is_open = True

            if cur_btn.count_mines == 0:
                x = cur_btn.x
                y = cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if not abs(dx - dy) == 1:
                            continue

                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.ROW and \
                                1 <= next_btn.y <= MineSweeper.COLUMNS and next_btn not in queue:
                            queue.append(next_btn)

    def open_all_buttons(self):
        for i in range(MineSweeper.ROW + 2):
            for j in range(MineSweeper.COLUMNS + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', background='red', disabledforeground='black')
                elif btn.count_mines == 1:
                    btn.config(text=btn.count_mines, fg='blue')
                elif btn.count_mines == 2:
                    btn.config(text=btn.count_mines, fg='green')
                elif btn.count_mines == 3:
                    btn.config(text=btn.count_mines, fg='red')
                elif btn.count_mines == 4:
                    btn.config(text=btn.count_mines, fg='dark blue')
                elif btn.count_mines == 5:
                    btn.config(text=btn.count_mines, fg='dark red')
                else:
                    btn.config(text='', disabledforeground='black')

    def start_game(self):
        pass

    def print_buttons(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('M', end=' ')
                else:
                    print(btn.count_mines, end=' ')
            print()

    def insert_mines(self, number: int):
        index_mines = self.get_mines_places(number)
        print(index_mines)
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True

    def count_mines_in_buttons(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_mines = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                count_mines += 1
                btn.count_mines = count_mines

    @staticmethod
    def get_mines_places(exclude_number: int):
        indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROW + 1))
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:MineSweeper.MINES]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MineSweeper()
    ex.start_game()
    ex.show()
    sys.exit(app.exec())

# 🚩
