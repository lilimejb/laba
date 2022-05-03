import sys
import json
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
from PyQt5.QtGui import QPixmap

with open('elements.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


def find_element(name):
    for elem in data:
        if elem['name'] == name:
            return elem


def make_beautiful(element):
    return f"""Элемент {element['name']} ({element['symbol']}):
    Порядковый номер: {element['number']}
    Массовое число изотопа: {element['mass number']}
    Период полураспада: {element['T']}
    Излучение: {element['radiation']}"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        for elem in data:
            self.elem_chooser.addItem(elem['name'])

        self.elem_chooser.currentTextChanged.connect(self.show_info)
        self.make_graph.clicked.connect(self.graphastoika)
        self.save.clicked.connect(self.save_graph)
        print(self.graph.pixmap())

    def save_graph(self):
        import shutil
        import os
        if self.graph.pixmap():
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            if 'plots' not in os.listdir(desktop):
                os.mkdir(f'{desktop}/plots')
            plot_counter = len(os.listdir(f'{desktop}/plots'))
            name = f"plot{plot_counter}({find_element(self.elem_chooser.currentText())['name']}).jpg"
            shutil.copy('plot.jpg', f'{desktop}/plots/{name}')
            self.error_label.setText('')
        else:
            self.error_label.setText('Чтобы сохранить график нужно его построить')

    def graphastoika(self):
        import matplotlib.pyplot as plt
        import os

        try:
            n0 = int(self.number.text())
        except Exception:
            self.error_label.setText('Введено неверное число. Число частиц = 128')
            n0 = 128
        element = find_element(self.elem_chooser.currentText())
        T = eval(" ".join(element["T"].split()[:-1]))
        razmer = element["T"].split()[-1]
        t = [T * i for i in range(10)]
        n = [n0 * 2 ** (-i / T) for i in t]
        plt.clf()
        plt.plot(n, t)
        plt.ylabel('n')
        plt.xlabel(f't, {razmer}')
        if 'plot.jpg' in os.listdir():
            os.remove('plot.jpg')
        plt.savefig('plot.jpg')
        self.graph.setPixmap(QPixmap('plot.jpg'))

    def show_info(self):
        element = find_element(self.sender().currentText())
        self.element_info.setText(make_beautiful(element))


def error_catcher(exctype, value, tb):
    print('My Error Information')
    print('Type:', exctype)
    print('Value:', value)
    print('Traceback:', tb)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = error_catcher
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
