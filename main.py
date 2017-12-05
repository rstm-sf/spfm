import math
import sys


import scipy.special as sc


import main_window as mw


from decimal import Decimal, getcontext
getcontext().prec = 2


from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Model_CRR(object):
    def __init__(self, r, a, b, B0, S0, K, N):
        self._r = r
        self._a = a
        self._b = b
        self._B0 = Decimal(B0)
        self._S0 = Decimal(S0)
        self._K = Decimal(K)
        self._N = N
        self._p = (r - a) / (b - a)
        self._calc_K0()
        self._calc_CN()
        self._BN = self._B0 * Decimal(math.pow(1.0 + r, N))
        self._BN_inv = 1.0 / float(self._BN)
        self._n, self._Sn_prev = 1, self._S0

    def _calc_K0(self):
        K, S0 = float(self._K), float(self._S0)
        self._K0 = 1 + math.floor(
            math.log(
                K / (S0 * math.pow(1.0 + self._a, self._N)),
                (1.0 + self._b) / (1.0 + self._a)
            )
        )

    def _calc_CN(self):
        self._CN = self._calc_FN(self._S0) * \
            Decimal(math.pow(1.0 / (1.0 + self._r), self._N))

    def _calc_FN(self, X):
        F, Fk, N = Decimal(0.0), self._calk_Fk, self._N
        if self._K0 <= N:
            for k in range(self._K0, N + 1):
                F += Fk(X, N, k)
        return F

    def _calc_F(self, X, n):
        F, Fk = Decimal(0.0), self._calk_Fk
        for k in range(n + 1):
            F += Fk(X, n, k)
        return F

    def _calk_Fk(self, X, n, k):
        a, b, p = self._a, self._b, self._p
        q, a_1, b_1 = 1 - p, 1 + a, 1 + b
        x_ = X * Decimal(math.pow(a_1, n - k) * math.pow(b_1, k))
        binom = Decimal(sc.perm(n, k) * math.pow(p, k) * math.pow(q, n - k))
        return self._fun(x_) * binom

    def _fun(self, X):
        return max(Decimal(0.0), X - self._K)

    def increment_n(self):
        self._n += 1

    def calc_Sn(self, rho):
        self._Sn_prev *= Decimal(1.0 + rho)

    def calc_gamma_n(self):
        N, n, Sn_prev, F = self._N, self._n, self._Sn_prev, self._calc_F
        k, a, b, r = N - n, self._a, self._b, self._r
        self._gamma_n = math.pow(1.0 / (1.0 + self._r), k) * float(
            F(Sn_prev * Decimal(1.0 + b), k) - F(Sn_prev * Decimal(1.0 + a), k)
        ) / (float(Sn_prev) * (b - a))

    def calc_beta_n(self):
        N, n, Sn_prev, F = self._N, self._n, self._Sn_prev, self._calc_F
        k, a, b, r = N - n, self._a, self._b, self._r
        self._beta_n = self._BN_inv * (
            float(F(Sn_prev, k + 1)) - (1.0 + r) / (b - a) *
            float(F(Sn_prev * Decimal(1.0 + b), k) -
                  F(Sn_prev * Decimal(1.0 + a), k))
        )


class Form(QMainWindow, mw.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.stack_str = list()
        self.stack_dict = dict()
        self._is_connect_up_down = False
        self.test_input()
        self.pushButton_3.clicked.connect(self.get_choice_history)
        self.pushButton_4.clicked.connect(self.clear)
        self.pushButton_5.clicked.connect(self.show_dialog)

    def button_up(self):
        a = self.a
        self.push_state_to_stack()
        a.increment_n()
        a.calc_Sn(a._b)
        self.update_beta_gamma()
        self.check_end()

    def button_down(self):
        a = self.a
        self.push_state_to_stack()
        a.increment_n()
        a.calc_Sn(a._a)
        self.update_beta_gamma()
        self.check_end()

    def update_beta_gamma(self):
        self.a.calc_gamma_n()
        self.a.calc_beta_n()
        self.update_beta_gamma_line_edit()

    def update_beta_gamma_line_edit(self):
        a = self.a
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
        self.lineEdit_8.setText(str(int(a._CN)))
        self.update_beta_gamma()
        self.check_start()

    def show_dialog(self):
        r = self.input_dialog_get_r_a_b("r")
        a = self.input_dialog_get_r_a_b("a", -1.0, r)
        b = self.input_dialog_get_r_a_b("b", r, 1.0)
        B0 = self.input_dialog_get_B0()
        S0 = self.input_dialog_get_S0_K("S0")
        K = self.input_dialog_get_S0_K("K")
        N = self.input_dialog_get_N()
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
        self.lineEdit_8.setText(str(int(a._CN)))
        self.update_beta_gamma()
        self.check_start()

    def input_dialog_get_r_a_b(self, x: str, l=-1.0, h=1.0):
        num, ok = QInputDialog.getDouble(
            self, "Окно ввода", "Введите значение " + x + ":", min=l, max=h
        )
        if ok and l < num < h:
            return num
        else:
            raise Exception("Неверно введено " + x + "!")

    def input_dialog_get_S0_K(self, x: str):
        num, ok = QInputDialog.getDouble(
            self, "Окно ввода", "Введите значение " + x + ":", min=0.0
        )
        if ok:
            return num
        else:
            raise Exception("Неверно введено " + x + "!")

    def input_dialog_get_B0(self):
        num, ok = QInputDialog.getDouble(
            self, "Окно ввода", "Введите значение B0:", min=0.0
        )
        if ok and num > 0.0:
            return num
        else:
            raise Exception("Неверно введено B0!")

    def input_dialog_get_N(self):
        num, ok = QInputDialog.getInt(
            self, "Окно ввода", "Введите значение N:", min=0
        )
        if ok and num > 0:
            return num
        else:
            raise Exception("Неверно введено N!")

    def check_start(self):
        a = self.a
        if a._n < a._N and a._beta_n != 0.0 and a._gamma_n != 0.0 \
            and (Decimal(a._beta_n) * a._B0 +
                 Decimal(a._gamma_n) * a._S0) != Decimal(0.0):
            self.button_up_down_connect()

    def check_end(self):
        a = self.a
        if a._n == a._N or a._beta_n == 0.0 and a._gamma_n == 0.0 \
            or (Decimal(a._beta_n) * a._B0 +
                Decimal(a._gamma_n) * a._S0) == Decimal(0.0):
            self.button_up_down_disconnect()

    def button_up_down_connect(self):
        if not self._is_connect_up_down:
            self._is_connect_up_down = True
            self.pushButton.clicked.connect(self.button_up)
            self.pushButton_2.clicked.connect(self.button_down)

    def button_up_down_disconnect(self):
        if self._is_connect_up_down:
            self._is_connect_up_down = False
            self.pushButton.clicked.disconnect()
            self.pushButton_2.clicked.disconnect()

    def get_choice_history(self):
        item, ok = QInputDialog.getItem(
            self, "Диалог возврата", "Выберите шаг:",
            self.stack_str, editable=False
        )
        if ok and item:
            item = self.stack_dict.get(item)
            self.a._n = item[0]
            self.a._beta_n = item[1]
            self.a._gamma_n = item[2]
            self.a._Sn_prev = item[3]
            self.update_beta_gamma_line_edit()
            self.button_up_down_connect()
            for i in range(self.a._n, len(self.stack_str)):
                self.stack_dict.pop(str(i))
                self.stack_str.pop()

    def push_state_to_stack(self):
        a = self.a
        save_str = str(a._n)
        self.stack_str.append(save_str)
        self.stack_dict[save_str] = [a._n, a._beta_n, a._gamma_n, a._Sn_prev]

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
        self.button_up_down_disconnect()


def main():
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
