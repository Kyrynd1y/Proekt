import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo

colors = {
    1: 'blue',
    2: 'green',
    3: 'red',
    4: 'dark blue',
    5: 'dark red'
}


class Button(tk.Button):
    def __repr__(self):
        return f'My button {self.x} {self.y} {self.number} ({self.is_mine})'

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(Button, self).__init__(master, width=3, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_mines = 0
        self.is_open = False


class SAPER:
    main_window = tk.Tk()
    ROW = 10
    COLUMNS = 10
    MINES = 10
    IS_GAME_OVER = False
    IS_WIN = False
    IS_FIRST_CLICK = True

    def __init__(self):
        self.buttons = []

        for i in range(SAPER.ROW + 2):
            temp = []
            for j in range(SAPER.COLUMNS + 2):
                btn = Button(SAPER.main_window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind('<Button-3>', self.right_click)
                temp.append(btn)
            self.buttons.append(temp)

    @staticmethod
    def right_click(event):

        if SAPER.IS_GAME_OVER:
            return

        cur_btn = event.widget
        if cur_btn['state'] == 'normal' and 0 < SAPER.MINES <= 10:
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '🚩'
            SAPER.MINES -= 1
        elif cur_btn['text'] == '🚩':
            cur_btn['text'] = ''
            cur_btn['state'] = 'normal'
            SAPER.MINES += 1

    def click(self, clicked_button: Button):

        if SAPER.IS_GAME_OVER:
            return

        if SAPER.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_buttons()
            self.print_buttons()
            SAPER.IS_FIRST_CLICK = False

        if clicked_button.is_mine:
            clicked_button.config(text='*', background='red', disabledforeground='black')
            clicked_button.is_open = True
            SAPER.IS_GAME_OVER = True
            showinfo('GAME OVER', 'GAME OVER')
            for i in range(1, SAPER.ROW + 1):
                for j in range(1, SAPER.COLUMNS + 1):
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
        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)

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
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_mines == 0:
                x = cur_btn.x
                y = cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if not abs(dx - dy) == 1:
                            continue

                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= SAPER.ROW and \
                                1 <= next_btn.y <= SAPER.COLUMNS and next_btn not in queue:
                            queue.append(next_btn)

    def create_widgets(self):
        count = 1
        for i in range(1, SAPER.ROW + 1):
            for j in range(1, SAPER.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j)
                count += 1

    def open_all_buttons(self):
        for i in range(SAPER.ROW + 2):
            for j in range(SAPER.COLUMNS + 2):
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
        self.create_widgets()
        SAPER.main_window.mainloop()

    def print_buttons(self):
        for i in range(1, SAPER.ROW + 1):
            for j in range(1, SAPER.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('M', end=' ')
                else:
                    print(btn.count_mines, end=' ')
            print()

    def insert_mines(self, number: int):
        index_mines = self.get_mines_places(number)
        print(index_mines)
        for i in range(1, SAPER.ROW + 1):
            for j in range(1, SAPER.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True

    def count_mines_in_buttons(self):
        for i in range(1, SAPER.ROW + 1):
            for j in range(1, SAPER.COLUMNS + 1):
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
        indexes = list(range(1, SAPER.COLUMNS * SAPER.ROW + 1))
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:SAPER.MINES]


game = SAPER()
game.start_game()
