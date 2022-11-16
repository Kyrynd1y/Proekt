import sys

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QGridLayout


class Cell(QPushButton):
    pass


class Example(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        layout.setHorizontalSpacing(1)
        layout.setVerticalSpacing(1)
        self.setLayout(layout)
        n = 10
        for r in range(n):
            for c in range(n):
                btn = Cell(self)
                self.layout().addWidget(btn, r, c)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
