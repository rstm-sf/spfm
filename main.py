import main_window as mw
import sys
from model_CRR import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Form(QMainWindow, mw.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show_dialog()
        a = self.a
        if a._n < a._N or (a._beta_n + a._gamma_n) != 0.0:
            self.pushButton.clicked.connect(self.button_up)
            self.pushButton_2.clicked.connect(self.button_down)

    def button_up(self):
        a = self.a
        a.increment_n()
        a.calc_Sn(a._b)
        self.update_beta_gamma()

    def button_down(self):
        a = self.a
        a.increment_n()
        a.calc_Sn(a._a)
        self.update_beta_gamma()

    def update_beta_gamma(self):
        a = self.a
        a.calc_gamma_n()
        a.calc_beta_n()
        self.lineEdit_11.setText(str(a._n))
        self.lineEdit_10.setText(str(round(a._beta_n, 4)))
        self.lineEdit_9.setText(str(round(a._gamma_n, 4)))

    def show_dialog(self):
        input_text = "Окно ввода"

        def enter_text(x: str):
            return "Введите значение " + x + ":"

        def print_error_input(x: str):
            return print("Неверно введено " + x + "!")

        num, ok = QInputDialog.getDouble(self, input_text, enter_text("r"))
        if ok and -1.0 < num < 1.0:
            r = num
        else:
            print_error_input("r")
        num, ok = QInputDialog.getDouble(self, input_text, enter_text("a"))
        if ok and -1.0 <= num < r:
            a = num
        else:
            print_error_input("a")
        num, ok = QInputDialog.getDouble(self, input_text, enter_text("b"))
        if ok and r < num <= 1.0:
            b = num
        else:
            print_error_input("b")
        num, ok = QInputDialog.getDouble(self, input_text, enter_text("B0"))
        if ok and num >= 0.0:
            B0 = num
        else:
            print_error_input("B0")
        num, ok = QInputDialog.getDouble(self, input_text, enter_text("S0"))
        if ok and num >= 0.0:
            S0 = num
        else:
            print_error_input("S0")
        num, ok = QInputDialog.getDouble(self, input_text, enter_text("K"))
        if ok and num >= 0.0:
            K = num
        else:
            print_error_input("K")
        num, ok = QInputDialog.getInt(self, input_text, enter_text("N"))
        if ok and num > 0:
            N = num
        else:
            print_error_input("N")

        # default test: Model_CRR(0, -2 / 5, 1 / 5, 1, 150, 150, 1)
        # (beta, gamma) = (-30, 1 / 3)
        # Ширяев А. Н. Основы стохастической финансовой математики
        self.a = Model_CRR(r, a, b, B0, S0, K, N)
        a = self.a
        a.calc_gamma_n()
        a.calc_beta_n()
        self.lineEdit.setText(str(a._a))
        self.lineEdit_2.setText(str(a._b))
        self.lineEdit_3.setText(str(a._r))
        self.lineEdit_4.setText(str(a._B0))
        self.lineEdit_5.setText(str(a._S0))
        self.lineEdit_6.setText(str(a._K))
        self.lineEdit_7.setText(str(a._N))
        self.lineEdit_8.setText(str(a._CN))
        self.update_beta_gamma()

    def check_end(self):
        a = self.a
        if a._n == a._N or (a._beta_n + a._gamma_n) == 0.0:
            self.pushButton.clicked.disconnect()
            self.pushButton_2.clicked.disconnect()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
