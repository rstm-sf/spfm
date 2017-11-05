import math
import scipy.special as sc
from decimal import Decimal


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
        self._BN = self._B0 * Decimal(math.pow(1 + r, N))
        self._BN_inv = 1 / float(self._BN)
        self._n, self._Sn_prev = 1, self._S0

    def _calc_K0(self):
        K, S0 = float(self._K), float(self._S0)
        self._K0 = 1 + math.floor(
            math.log(
                K / (S0 * math.pow(1 + self._a, self._N)),
                (1 + self._b) / (1 + self._a)
            )
        )

    def _calc_CN(self):
        self._CN = self._calc_FN(self._S0) * \
            Decimal(math.pow(1 / (1 + self._r), self._N))

    def _calc_FN(self, X):
        F, Fk, N = Decimal(0), self._calk_Fk, self._N
        if self._K0 <= N:
            for k in range(self._K0, N + 1):
                F += Fk(X, N, k)
        return F

    def _calc_F(self, X, n):
        F, Fk = Decimal(0), self._calk_Fk
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
        return max(Decimal(0), X - self._K)

    def increment_n(self):
        self._n += 1

    def calc_Sn(self, rho):
        self._Sn_prev *= Decimal(1 + rho)

    def calc_gamma_n(self):
        N, n, Sn_prev, F = self._N, self._n, self._Sn_prev, self._calc_F
        k, a, b, r = N - n, self._a, self._b, self._r
        self._gamma_n = math.pow(1 / (1 + self._r), k) * float(
            F(Sn_prev * Decimal(1 + b), k) - F(Sn_prev * Decimal(1 + a), k)
        ) / (float(Sn_prev) * (b - a))

    def calc_beta_n(self):
        N, n, Sn_prev, F = self._N, self._n, self._Sn_prev, self._calc_F
        k, a, b, r = N - n, self._a, self._b, self._r
        self._beta_n = self._BN_inv * (
            float(F(Sn_prev, k + 1)) - (1 + r) / (b - a) *
            float(F(Sn_prev * Decimal(1 + b), k) - F(Sn_prev * Decimal(1 + a), k))
        )
