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

    def _calc_K0(self):
        K, S0 = float(self._K), float(self._S0)
        self._K0 = 1 + math.floor(
            math.log(
                K / (S0 * math.pow(1 + self._a, self._N)),
                (1 + self._b) / (1 + self._a)
            )
        )

    def _calc_CN(self):
        self._CN = self._calc_F(self._S0) * \
            Decimal(math.pow(1 / (1 + self._r), self._N))

    def _calc_F(self, X):
        F = Decimal(0)
        N, a, b, p = self._N, self._a, self._b, self._p
        q, a_1, b_1 = 1 - p, 1 + a, 1 + b
        if self._K0 <= N:
            for k in range(self._K0, N + 1):
                x_ = X * Decimal(math.pow(a_1, N - k) * math.pow(b_1, k))
                F += self._fun(x_) * Decimal(sc.perm(N, k, exact=True)
                                             * math.pow(p, k) * math.pow(q, N - k))
        return F

    def _fun(self, X):
        return X - self._K

    def calc_Bn(self):
        self._Bn *= Decimal(1 + r)

    def calc_Sn(self, rho):
        self._Sn *= Decimal(1 + rho)
