import sys
from functools import partial

import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from sympy import latex, cos, sin, Subs
from sympy.abc import x, y as Y

from gui.formula_input import FormulaInput
from gui.math_text_label import MathTextLabel
from gui.plot import MyFuncPlot
from gui.utils import clear_box
from solver.equation import *


class UI(QMainWindow):
    val_range = [0, 1]
    epsilon_pow = -2

    def __init__(self, usualFormulas, inpropedFormulas):
        super(UI, self).__init__()
        self.inpropedFormulas = inpropedFormulas
        uic.loadUi("GUI.ui", self)

        self.usualFormulas = usualFormulas


        self.prop_plot_graph = MyFuncPlot()
        self.main_v_box = self.findChild(QVBoxLayout, 'solve_v_layout')
        self.main_v_box.addWidget(self.prop_plot_graph)

        self.create_setting_box()
        method_setting_layout = QHBoxLayout()
        self.create_method_setting(method_setting_layout)

        self.main_v_box.addLayout(method_setting_layout)

        method_setting_layout2 = QHBoxLayout()
        self.inprop_plot_graph = MyFuncPlot()
        self.inprop_box = self.findChild(QVBoxLayout, 'solve_inprop_layout')
        self.inprop_box.addWidget(self.inprop_plot_graph)
        self.inprop_box.addLayout(method_setting_layout2)
        self.create_method_setting(method_setting_layout2)

        self.findChild(QPushButton, 'select_eq_btn').clicked.connect(self.select_equation)
        self.findChild(QPushButton, 'select_inprop_btn').clicked.connect(self.select_inprop)

        self.findChild(QWidget, 'proper_widget').setVisible(False)
        self.findChild(QWidget, 'solve_widget').setVisible(False)

        self.findChild(QWidget, 'inproper_widget').setVisible(False)
        self.findChild(QWidget, 'solve_inprop_widget').setVisible(False)

        self.findChild(QPushButton, 'goPropBtn').clicked.connect(self.go_proper)
        self.findChild(QPushButton, 'goInpropBtn').clicked.connect(self.go_inproper)

        self.findChild(QPushButton, 'solve_inprop_btn').clicked.connect(self.solve_inproper)

        self.show()

    def go_proper(self):
        self.eq_box = self.findChild(QComboBox, 'select_eq_comboBox')
        self.show_equations()
        self.findChild(QWidget, 'chooseTaskWidget').setVisible(False)
        self.findChild(QWidget, 'proper_widget').setVisible(True)

    def go_inproper(self):
        self.eq_box = self.findChild(QComboBox, 'select_inprop_comboBox')
        self.show_inproper()

        self.findChild(QWidget, 'chooseTaskWidget').setVisible(False)
        self.findChild(QWidget, 'inproper_widget').setVisible(True)

    def create_method_setting(self, layout):
        clear_box(layout)
        e_label = QLabel('ε= 10^')
        e_label.setAlignment(Qt.AlignRight)
        layout.addWidget(e_label)
        eps_spin = QSpinBox()
        eps_spin.setValue(self.epsilon_pow)
        eps_spin.setRange(-10, 2)
        eps_spin.valueChanged.connect(partial(self.set_e, eps_spin))
        layout.addWidget(eps_spin)

        x1_label = QLabel('x∈[')
        x1_label.setAlignment(Qt.AlignRight)
        layout.addWidget(x1_label)
        self.a_spin = QDoubleSpinBox()
        self.a_spin.setRange(-1000, self.val_range[1])
        self.a_spin.setValue(self.val_range[0])
        self.a_spin.valueChanged.connect(partial(self.set_a, self.a_spin))
        layout.addWidget(self.a_spin)

        x_comma_label = QLabel(',')
        x_comma_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(x_comma_label)

        self.b_spin = QDoubleSpinBox()
        self.b_spin.setRange(self.val_range[0], 1000)
        self.b_spin.setValue(self.val_range[1])
        self.b_spin.valueChanged.connect(partial(self.set_b, self.b_spin))
        layout.addWidget(self.b_spin)

        x2_label = QLabel(']')
        x2_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(x2_label)

        self.window().update()

    def set_start_val(self, spin, i=0):
        self.start_val[i] = spin.value()

    def set_e(self, spin):
        self.epsilon_pow = spin.value()

    def set_a(self, spin):
        self.val_range[0] = spin.value()
        self.b_spin.setRange(self.val_range[0], 1000)

    def set_b(self, spin):
        self.val_range[1] = spin.value()
        self.a_spin.setRange(-1000, self.val_range[1])

    def create_setting_box(self):
        sel_method_h_box = QHBoxLayout()
        btn_list = [
            QRadioButton('Левые прямоугольники'),
            QRadioButton('Средние прямоугольники'),
            QRadioButton('Правые прямоугольники'),
            QRadioButton('Трапеции'),
            QRadioButton('Симпсон')
        ]

        for i, btn in enumerate(btn_list):
            btn.clicked.connect(partial(self.set_method, i))
            sel_method_h_box.addWidget(btn)

        self.main_v_box.addLayout(sel_method_h_box)

    def set_method(self, id):
        solve_btn = self.findChild(QPushButton, 'solve_btn')
        solve_btn.setEnabled(True)
        solve_btn.disconnect()
        method_list = [
            lambda: self.use_method(left_rectangle),
            lambda: self.use_method(center_rectangle),
            lambda: self.use_method(right_rectangle),
            lambda: self.use_method(trapezoid),
            lambda: self.use_method(simpson),

        ]

        solve_btn.clicked.connect(method_list[id])

    def save_to_file(self, text):
        userResponse = QMessageBox.question(self,
                                            "Тип вывода",
                                            'Хотите сохранить в файл?',
                                            QMessageBox.Save | QMessageBox.Cancel,
                                            QMessageBox.Cancel
                                            )
        if userResponse == QMessageBox.Save:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                      "Text Files (*.txt)", options=options)
            if fileName:
                try:
                    f = open(fileName + ".txt", 'a')
                    f.write(text + '\n')
                    f.close()
                except Exception as e:
                    print(e)

    def display_result(self, res, iter_count=0, label_name = 'res_label', error_msg=""):
        if len(error_msg) == 0:
            text = f"Ответ = {round(res, -1 * self.epsilon_pow + 1)}," \
                   f" при n = {round(iter_count, -1 * self.epsilon_pow + 1)},"
            self.findChild(QLabel, label_name).setText(text)
            self.save_to_file(text)
        else:
            self.findChild(QLabel, label_name).setText("Ошибка: " + error_msg)

    def use_method(self, method):
        try:
            res, iter_count = rungeIteration(
                self.current_eq,
                method,
                self.val_range[0],
                self.val_range[1],
                10 ** self.epsilon_pow
            )
            self.display_result(res, iter_count)
        except Exception as e:
            self.display_result(0, error_msg=str(e))

    def solve_inproper(self):
        try:
            res = integral(
                self.current_eq.formula,
                self.val_range[0],
                self.val_range[1],
                self.current_eq.crit
            )
            if res is None:
                self.display_result(res, error_msg='Интеграл расходится', label_name='inprop_res_label')
            else:
                self.display_result(res, label_name='inprop_res_label')
        except Exception as e:
            self.display_result(0, error_msg=str(e))


    def addFormula(self, equation):
        self.usualFormulas.append(equation)
        l = self.findChild(QVBoxLayout, 'formulas_widget')
        row = QHBoxLayout()
        row.addWidget(QLabel(f'{len(self.usualFormulas) + 1}) '))
        row.addLayout(FormulaInput(self.addFormula))
        l.addLayout(row)
        self.eq_box.addItem(str(len(self.usualFormulas)))

    def show_equations(self):
        l = self.findChild(QVBoxLayout, 'formulas_widget')
        for i in range(len(self.usualFormulas)):
            row = QHBoxLayout()
            row.addWidget(QLabel(f'{i + 1}) '))
            row.addWidget(MathTextLabel('$' + latex(self.usualFormulas[i]) + '=0$', self),
                          alignment=Qt.AlignHCenter)
            l.addLayout(row)
            self.eq_box.addItem(str(i + 1))

        row = QHBoxLayout()
        row.addWidget(QLabel(f'{len(self.usualFormulas) + 1}) '))
        row.addLayout(FormulaInput(self.addFormula))
        l.addLayout(row)

    def show_inproper(self):
        l = self.findChild(QVBoxLayout, 'inproper_widget_2')
        for i, f in enumerate(self.inpropedFormulas):
            row = QHBoxLayout()
            row.addWidget(QLabel(f'{i + 1}) '))
            row.addWidget(MathTextLabel('$' + latex(f.formula) + '=0$', self),
                          alignment=Qt.AlignHCenter)
            l.addLayout(row)
            self.eq_box.addItem(str(i + 1))

    def select_equation(self):
        id = self.eq_box.currentText()
        self.current_eq = self.usualFormulas[int(id) - 1]
        print(self.current_eq)
        self.findChild(QWidget, 'proper_widget').setVisible(False)
        self.findChild(QWidget, 'solve_widget').setVisible(True)
        self.prop_plot_graph.paint_graph([self.current_eq])
        self.window().update()
        # self.findChild(QWidget, 'eq_widget').setVisible(False)

    def select_inprop(self):
        id = self.eq_box.currentText()
        self.current_eq = self.inpropedFormulas[int(id) - 1]
        print(self.current_eq.formula)
        self.findChild(QWidget, 'inproper_widget').setVisible(False)
        self.findChild(QWidget, 'solve_inprop_widget').setVisible(True)
        self.inprop_plot_graph.paint_graph([self.current_eq.formula])
        self.window().update()
        # self.findChild(QWidget, 'eq_widget').setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UI(formulas, inproped)
    app.exec_()
