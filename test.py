import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle("PyQt MessageBox Tutorial - pythonprogramminglanguage.com")

        pybutton = QPushButton('Trigger Message Box', self)
        pybutton.clicked.connect(self.displayMessageBox)
        pybutton.resize(200,64)
        pybutton.move(50, 50)

    def displayMessageBox(self):
        userResponse = QMessageBox.question(self,
                                            "Тип вывода",
                                            'Хотите сохранить в файл?',
                                            QMessageBox.Save | QMessageBox.Cancel,
                                            QMessageBox.Cancel
                                            )

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())