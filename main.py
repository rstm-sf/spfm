import math
import sys


import main_window as mw
import start_window as sw


from decimal import Decimal


from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Base_model_CRR():
    def __init__(self, r, a, b, B0, S0, K, N):
        self._r = r
        self._a = a
        self._b = b
        self._B0 = Decimal(B0)
        self._S0 = Decimal(S0)
        self._K = Decimal(K)
        self._N = N

    def get_r_a_b_B0_S0_K_N(self):
        return self._r, self._a, self._b, self._B0, self._S0, self._K, self._N


class Model_CRR(Base_model_CRR):
    def __init__(self, r, a, b, B0, S0, K, N):
        super().__init__(r, a, b, B0, S0, K, N)
        self._p = (r - a) / (b - a)
        self._calc_K0()
        self._calc_CN()
        self._BN = self._B0 * Decimal(math.pow(1.0 + r, N))
        self._BN_inv = 1.0 / float(self._BN)
        self._n, self._Sn_prev = 1, self._S0

    @staticmethod
    def _Ckn(k, n):
        return math.factorial(n) / (math.factorial(n - k) * math.factorial(k))

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
        binom = Decimal(self._Ckn(k, n) * math.pow(p, k) * math.pow(q, n - k))
        return self._fun(x_) * binom

    def _fun(self, X):
        return max(Decimal(0.0), X - self._K)

    def increment_n(self):
        self._n += 1

    def calc_Sn_prev(self, rho):
        self._Sn_prev *= Decimal(1.0 + rho)

    def calc_gamma_n(self):
        if self._n > self._N:
            return
        N, n, Sn_prev, F = self._N, self._n, self._Sn_prev, self._calc_F
        k, a, b, r = N - n, self._a, self._b, self._r
        self._gamma_n = math.pow(1.0 / (1.0 + self._r), k) * float(
            F(Sn_prev * Decimal(1.0 + b), k) - F(Sn_prev * Decimal(1.0 + a), k)
        ) / (float(Sn_prev) * (b - a))

    def calc_beta_n(self):
        if self._n > self._N:
            return
        N, n, Sn_prev, F = self._N, self._n, self._Sn_prev, self._calc_F
        k, a, b, r = N - n, self._a, self._b, self._r
        self._beta_n = self._BN_inv * (
            float(F(Sn_prev, k + 1)) - (1.0 + r) / (b - a) *
            float(F(Sn_prev * Decimal(1.0 + b), k) -
                  F(Sn_prev * Decimal(1.0 + a), k))
        )


class Start_Form(QMainWindow, sw.Ui_StartWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.test_input()
        self.pushButton_5.clicked.connect(self.show_dialog)
        self.pushButton_6.clicked.connect(self.button_change_a)
        self.pushButton_7.clicked.connect(self.button_change_b)
        self.pushButton_8.clicked.connect(self.button_change_r)
        self.pushButton_9.clicked.connect(self.button_change_B0)
        self.pushButton_10.clicked.connect(self.button_change_S0)
        self.pushButton_11.clicked.connect(self.button_change_K)
        self.pushButton_12.clicked.connect(self.button_change_N)
        self.pushButton_4.clicked.connect(self.calculate)

    def test_input(self):
        ''' (beta, gamma) = (-30, 1 / 3)
        Ширяев А. Н. Основы стохастической финансовой математики'''
        self.a = Base_model_CRR(0, -2 / 5, 1 / 5, 1, 150, 150, 1)
        self.settext_lineedit_a_b_r_B0_S0_K_N()

    def show_dialog(self):
        r, ok = self.input_dialog_get_r_a_b("r")
        if not ok:
            return
        a, ok = self.input_dialog_get_r_a_b("a", -1.0, r)
        if not ok:
            return
        b, ok = self.input_dialog_get_S0_K_b("b", r)
        if not ok:
            return
        B0, ok = self.input_dialog_get_B0()
        if not ok:
            return
        S0, ok = self.input_dialog_get_S0_K_b("S0")
        if not ok:
            return
        K, ok = self.input_dialog_get_S0_K_b("K")
        if not ok:
            return
        N, ok = self.input_dialog_get_N()
        if not ok:
            return
        self.a = Base_model_CRR(r, a, b, B0, S0, K, N)
        self.settext_lineedit_a_b_r_B0_S0_K_N()

    def input_dialog_get_r_a_b(self, x: str, l=-1.0, h=1.0):
        num, ok = QInputDialog.getDouble(
            self, "Окно ввода", "Введите значение " + x + ":", min=l, max=h
        )
        if l < num < h:
            return num, ok
        else:
            raise Exception("Неверно введено " + x + "!")

    def input_dialog_get_S0_K_b(self, x: str, l=0.0):
        return QInputDialog.getDouble(
            self, "Окно ввода", "Введите значение " + x + ":", min=l
        )

    def input_dialog_get_B0(self):
        num, ok = QInputDialog.getDouble(
            self, "Окно ввода", "Введите значение B0:", min=0.0
        )
        if num > 0.0:
            return num, ok
        else:
            raise Exception("Неверно введено B0!")

    def input_dialog_get_N(self):
        num, ok = QInputDialog.getInt(
            self, "Окно ввода", "Введите значение N:", min=1
        )
        if num > 0:
            return num, ok
        else:
            raise Exception("Неверно введено N!")

    def settext_lineedit_a_b_r_B0_S0_K_N(self):
        a = self.a
        self.lineEdit.setText(str(a._a))
        self.lineEdit_2.setText(str(a._b))
        self.lineEdit_3.setText(str(a._r))
        self.lineEdit_4.setText(str(a._B0))
        self.lineEdit_5.setText(str(a._S0))
        self.lineEdit_6.setText(str(a._K))
        self.lineEdit_7.setText(str(a._N))

    def button_change_r(self):
        r, ok = self.input_dialog_get_r_a_b("r")
        if not ok:
            return
        self.a._r = r
        self.lineEdit_3.setText(str(r))

    def button_change_a(self):
        a, ok = self.input_dialog_get_r_a_b("a")
        if not ok:
            return
        self.a._a = a
        self.lineEdit.setText(str(a))

    def button_change_b(self):
        b, ok = self.input_dialog_get_S0_K_b("b", -1.0)
        if not ok:
            return
        self.a._b = b
        self.lineEdit_2.setText(str(b))

    def button_change_B0(self):
        B0, ok = self.input_dialog_get_B0()
        if not ok:
            return
        self.a._B0 = Decimal(B0)
        self.lineEdit_4.setText(str(B0))

    def button_change_S0(self):
        S0, ok = self.input_dialog_get_S0_K_b("S0")
        if not ok:
            return
        self.a._S0 = Decimal(S0)
        self.lineEdit_5.setText(str(S0))

    def button_change_K(self):
        K, ok = self.input_dialog_get_S0_K_b("K")
        if not ok:
            return
        self.a._K = Decimal(K)
        self.lineEdit_6.setText(str(K))

    def button_change_N(self):
        N, ok = self.input_dialog_get_N()
        if not ok:
            return
        self.a._N = N
        self.lineEdit_7.setText(str(N))

    def calculate(self):
        if not self.a._a < self.a._r < self.a._b:
            print("Должно быть a < r < b!")
            return
        self.main_window = Main_Form(self.a)
        self.close()
        self.main_window.show()


class Main_Form(QMainWindow, mw.Ui_MainWindow):
    def __init__(self, base_model_CRR):
        super().__init__()
        self.setupUi(self)
        self.a = Model_CRR(*base_model_CRR.get_r_a_b_B0_S0_K_N())
        self.settext_lineedit_a_b_r_B0_S0_K_N_CN_K0()
        self.update_beta_gamma()
        self.stack_str = list()
        self.stack_dict = dict()
        self._is_connect_up_down = False
        self.check_start()
        self.pushButton_3.clicked.connect(self.get_choice_history)
        self.pushButton_4.clicked.connect(self.button_calc_capital)
        self.pushButton_5.clicked.connect(self.button_new_task)

    def button_up(self):
        a = self.a
        self.push_state_to_stack()
        a.increment_n()
        a.calc_Sn_prev(a._b)
        self.update_beta_gamma()
        self.check_end()

    def button_down(self):
        a = self.a
        self.push_state_to_stack()
        a.increment_n()
        a.calc_Sn_prev(a._a)
        self.update_beta_gamma()
        self.check_end()

    def update_beta_gamma(self):
        self.a.calc_gamma_n()
        self.a.calc_beta_n()
        self.update_n_beta_gamma_S_prev_line_edit()

    def update_n_beta_gamma_S_prev_line_edit(self):
        a = self.a
        self.lineEdit_8.setText(str(round(float(a._Sn_prev), 4)))
        self.lineEdit_11.setText(str(a._n - 1))
        self.lineEdit_10.setText(str(round(a._beta_n, 4)))
        self.lineEdit_9.setText(str(round(a._gamma_n, 4)))

    def settext_lineedit_a_b_r_B0_S0_K_N_CN_K0(self):
        a = self.a
        self.lineEdit.setText(str(a._a))
        self.lineEdit_2.setText(str(a._b))
        self.lineEdit_3.setText(str(a._r))
        self.lineEdit_4.setText(str(a._B0))
        self.lineEdit_5.setText(str(a._S0))
        self.lineEdit_6.setText(str(a._K))
        self.lineEdit_7.setText(str(a._N))
        self.lineEdit_8.setText(str(a._Sn_prev))
        self.lineEdit_15.setText(str(round(float(a._CN), 4)))
        self.lineEdit_16.setText(str(a._K0))

    def check_start(self):
        if self.a._n <= self.a._N and self.a._K0 <= self.a._N and (
            abs(self.a._beta_n) >= float(1e-31) or \
            abs(self.a._gamma_n) >= float(1e-31)
        ):
            self.button_up_down_connect()

    def check_end(self):
        if self.a._n > self.a._N or abs(self.a._beta_n) < float(1e-31) and \
                abs(self.a._gamma_n) < float(1e-31):
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
        if ok:
            a = self.a
            a._n, a._beta_n, a._gamma_n, a._Sn_prev = self.stack_dict.get(item)
            self.update_n_beta_gamma_S_prev_line_edit()
            self.button_up_down_connect()
            for i in range(a._n - 1, len(self.stack_str)):
                self.stack_dict.pop(str(i))
                self.stack_str.pop()

    def push_state_to_stack(self):
        a = self.a
        save_str = str(a._n - 1)
        self.stack_str.append(save_str)
        self.stack_dict[save_str] = [a._n, a._beta_n, a._gamma_n, a._Sn_prev]

    def button_calc_capital(self):
        a = self.a
        QMessageBox.question(
            self,
            "Исполнение",
            "Выплата равна: " + str(round(float(a._fun(a._Sn_prev)), 4)),
            QMessageBox.Ok
        )

    def button_new_task(self):
        self.start_window = Start_Form()
        self.close()
        self.start_window.show()


def main():
    app = QApplication(sys.argv)
    start_form = Start_Form()
    start_form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
