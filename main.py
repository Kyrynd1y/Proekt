import sys

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QGridLayout


class MyButton(QPushButton):
    def __init__(self, x, y, number):
        super(MyButton, self).__init__(self, x, y, number)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False

    def __repr__(self):
        return f'MyButton {self.x} {self.y} {self.number}'


class MineSweeper(QWidget):
    ROW = 10
    COLUMN = 10

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
            for j in range(MineSweeper.COLUMN):
                btn = MyButton(self, x=i, y=j, number=count)
                self.layout().addWidget(btn, i, j)
                temp.append(btn)
                count += 1
            self.buttons.append(temp)

    def print_buttons(self):
        for row_btn in self.buttons:
            print(row_btn)

    def start(self):
        self.print_buttons()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MineSweeper()
    ex.start()
    ex.show()
    sys.exit(app.exec())

#
