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
        self.stack_str = list()
        self.stack_dict = dict()
        self.test_input()
        self.pushButton_3.clicked.connect(self.getChoiceHistory)
        self.pushButton_4.clicked.connect(self.clear)
        self.pushButton_5.clicked.connect(self.show_dialog)

    def button_up(self):
        a = self.a
        self.push_state_to_stack()
        a.increment_n()
        a.calc_Sn(a._b)
        self.update_beta_gamma()

    def button_down(self):
        a = self.a
        self.push_state_to_stack()
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

    def test_input(self):
        ''' (beta, gamma) = (-30, 1 / 3)
        Ширяев А. Н. Основы стохастической финансовой математики'''
        self.a = Model_CRR(0, -2 / 5, 1 / 5, 1, 150, 150, 1)
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

    def show_dialog(self):
        input_text = "Окно ввода"

        def enter_text(x: str):
            return "Введите значение " + x + ":"

        def print_error_input(x: str):
            return print("Неверно введено " + x + "!")

        num, ok = QInputDialog.getDouble(
            self, input_text, enter_text("r"), min=-1.0, max=1.0
        )
        if ok and -1.0 < num < 1.0:
            r = num
        else:
            print_error_input("r")
        num, ok = QInputDialog.getDouble(
            self, input_text, enter_text("a"), min=-1.0, max=r
        )
        if ok and num < r:
            a = num
        else:
            print_error_input("a")
        num, ok = QInputDialog.getDouble(
            self, input_text, enter_text("b"), min=r, max=1.0
        )
        if ok and r < num < 1.0:
            b = num
        else:
            print_error_input("b")
        num, ok = QInputDialog.getDouble(
            self, input_text, enter_text("B0"), min=0.0
        )
        if ok:
            B0 = num
        else:
            print_error_input("B0")
        num, ok = QInputDialog.getDouble(
            self, input_text, enter_text("S0"), min=0.0
        )
        if ok:
            S0 = num
        else:
            print_error_input("S0")
        num, ok = QInputDialog.getDouble(
            self, input_text, enter_text("K"), min=0.0
        )
        if ok:
            K = num
        else:
            print_error_input("K")
        num, ok = QInputDialog.getInt(self, input_text, enter_text("N"), min=0)
        if ok and num > 0:
            N = num
        else:
            print_error_input("N")

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

        if a._n < a._N and a._beta_n == 0.0 and a._gamma_n == 0.0 \
            and (Decimal(a._beta_n) * a._B0 +
                 Decimal(a._gamma_n) * a._S0) != Decimal(0.0):
            self.pushButton.clicked.connect(self.button_up)
            self.pushButton_2.clicked.connect(self.button_down)

    def check_end(self):
        a = self.a
        if a._n == a._N or a._beta_n == 0.0 and a._gamma_n == 0.0 \
            or (Decimal(a._beta_n) * a._B0 +
                Decimal(a._gamma_n) * a._S0) == Decimal(0.0):
            self.pushButton.clicked.disconnect()
            self.pushButton_2.clicked.disconnect()

    def getChoiceHistory(self):
        item, ok = QInputDialog.getItem(
            self, "Диалог возврата", "Выберите шаг:",
            self.stack_str, editable=False
        )
        if ok and item:
            item = self.stack_dict.get(item)
            n, beta, gamma = item[0], item[1], item[2]
            for i in range(n, len(self.stack_str)):
                self.stack_dict.pop(str(i))
                self.stack_str.pop()
            self.a._n = n
            self.a._beta_n = beta
            self.a._gamma_n = gamma
            self.update_beta_gamma()

    def push_state_to_stack(self):
        a = self.a
        save_str = str(a._n)
        self.stack_str.append(save_str)
        self.stack_dict[save_str] = [a._n, a._beta_n, a._gamma_n]

    def clear(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()
        self.lineEdit_11.clear()
        self.lineEdit_10.clear()
        self.lineEdit_9.clear()
        self.stack_dict.clear()
        self.stack_str.clear()


def main():
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
