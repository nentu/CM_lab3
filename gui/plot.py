import numpy as np
from pyqtgraph import PlotWidget, mkPen
from sympy import solve, Subs, cos, sin
from sympy.abc import x, y as Y

from PyQt5 import QtCore


class MyFuncPlot(PlotWidget):
    view_range = [[-5, 5], [-5, 5]]
    density = 50
    graph_count = 0

    def __init__(self):
        super().__init__()
        self.setBackground("w")
        self.showGrid(x=True, y=True)
        self.setXRange(0, 10, padding=0)
        self.setYRange(0, 10, padding=0)

        self.sigRangeChanged.connect(self.rangeChanged)

        self.eq_list = list()
        self.curves = list()

    def rangeChanged(self, _, range):
        self.view_range = range
        # self._paint_graph(self.view_range[0], [0, 0], (255, 0, 0))
        self._paint_current_graph()

    def paint_graph(self, f_list):
        self.eq_list = f_list.copy()
        self.curves = [self.plot(name="Line"+str(i)) for i in range(len(self.eq_list))]
        # self._paint_graph(self.view_range[0], [0, 0], (255, 0, 0))
        self._paint_current_graph()

    def count_eq(self, eq, val):
        res = eq.subs(x, val)
        if res.is_real:
            return res
        return 0

    def _paint_current_graph(self):

        for i in range(len(self.eq_list)):
            eq = self.eq_list[i]
            if eq.count(Y):
                y = np.linspace(
                    self.view_range[1][0],
                    self.view_range[1][1],
                    self.density).astype(float)
                f_1 = lambda val: eq.subs(Y, val)
                x_val = np.array([f_1(i) for i in y]).astype(float)
            else:
                x_val = np.linspace(
                    self.view_range[0][0],
                    self.view_range[0][1],
                    self.density
                ).astype(float)
                f = lambda val: self.count_eq(eq, val)
                y = np.array([f(i) for i in x_val]).astype(float)
            self._paint_graph(x_val, y, i)




    def _paint_graph(self, x_val, y, curve_i, color=(0, 0, 255)):
        self.curves[curve_i].setData(x=x_val, y=y, pen=mkPen(color=color))



from PyQt5 import Qt
import pyqtgraph as pg


class Window(Qt.QWidget):

    def __init__(self):
        super().__init__()

        layout = Qt.QVBoxLayout(self)

        self.setGeometry(300, 100, 600, 600)
        self.setWindowTitle('Программа')

        self.view = MyFuncPlot()
        self.curves = []

        self.view.setVisible(False)

        self.btn = Qt.QPushButton("Random plot")
        self.btn.clicked.connect(self.random_plot)

        layout.addWidget(Qt.QLabel("Some text"))
        layout.addWidget(self.view)
        layout.addWidget(self.btn)

    def random_plot(self):
        self.view.paint_graph([1 - cos(Y) / 2, sin(x + 1.0) - 1.2])
        self.view.setVisible(True)

        self.window().update()


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = Window()
    w.show()
    app.exec()