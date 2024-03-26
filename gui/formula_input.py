from PyQt5.QtWidgets import *
from sympy import latex
from sympy.abc import x
from sympy.parsing.sympy_parser import parse_expr

from gui.math_text_label import MathTextLabel
from gui.utils import clear_box


# from task2.solver.utils import msg_parse_error


class FormulaInput(QHBoxLayout):

    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.inputField = QLineEdit()
        self.addWidget(self.inputField)
        self.btn = QPushButton('Добавить')
        self.btn.clicked.connect(self.addFormula)
        self.addWidget(self.btn)

    def addFormula(self):

        try:
            for i in self.inputField.text():
                if 'a' <= i.lower() <= 'z' and i != 'x':
                    raise Exception('Unknown symbols')
            formula = parse_expr(self.inputField.text(), evaluate=False, local_dict={'x': x})
            formula.as_base_exp
        except Exception as e:
            msg_parse_error = QMessageBox()
            msg_parse_error.setIcon(QMessageBox.Critical)
            msg_parse_error.setText("Ошибка парсинга")
            msg_parse_error.setInformativeText('Пожалуйста, проверьте корректность введённой строки')
            msg_parse_error.setWindowTitle("Error")
            msg_parse_error.exec_()
            print(e)
            return
        self.callback(formula)
        print(formula)
        clear_box(self)
        self.addWidget(MathTextLabel('$' + latex(formula) + '=0$'))

