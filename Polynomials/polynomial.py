from .base import BasePolynomial
from collections.abc import Iterable


class Polynomial(BasePolynomial):
    def __init__(self, *coefficients):
        super().__init__()
        self.iter_num = 0
        self._coefficients = []

        if len(coefficients) == 1:
            if isinstance(coefficients[0], Polynomial):
                self._coefficients = list(coefficients[0].__coefficients)
            elif isinstance(coefficients[0], dict):
                d = coefficients[0]
                degree = max(map(int, d.keys()))
                self._coefficients = [
                    d[i] if i in d else 0 for i in range(degree + 1)
                ]
            elif isinstance(coefficients[0], Iterable):
                self._coefficients = coefficients[0]
            else:
                self._coefficients = coefficients

        elif len(coefficients) > 1:
            self._coefficients = coefficients


        self._coefficients = list(self._coefficients)

        # Removing trailing zeros
        while self._coefficients and self._coefficients[-1] == 0:
            self._coefficients.pop()

        if not self._coefficients:
            self._coefficients = [0]

    def __repr__(self):
        return f'Polynomial {repr(self._coefficients)}'

    def __str__(self):
        monomials = list(reversed(list(map(
            Polynomial.monomial_to_str,
            enumerate(self._coefficients)
        ))))

        result = ''
        first_sign, first_value = monomials.pop(0)
        if first_sign == '-':
            result += f'{first_sign}{first_value}'
        else:
            result += f'{first_value}'

        for sign, value in monomials:
            if value != '0':
                result += f' {sign} {value}'

        return result

    def __add__(self, other):
        if isinstance(other, Polynomial):
            a = self._coefficients
            b = other._coefficients
            if len(a) > len(b):
                a, b = b, a
            return Polynomial([x + y for x, y in zip(a, b)] + b[len(a):])
        else:
            return Polynomial([self._coefficients[0] + other] + self._coefficients[1:])

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    def __neg__(self):
        return Polynomial([-x for x in self._coefficients])

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return self._coefficients == other._coefficients
        else:
            return len(self._coefficients) == 1 and self._coefficients[0] == other

    def __call__(self, x):
        result = 0
        for a in reversed(self._coefficients):
            result = result * x + a

        return result

    @staticmethod
    def monomial_to_str(pair):
        i, a = pair
        sign = '+' if a >= 0 else '-'
        if a == 0:
            m = '0'
        else:
            m = ''
            if abs(a) != 1 or i == 0:
                m = str(abs(a))
            if i == 1:
                m += 'x'
            elif i > 1:
                m += f'x^{i}'

        return (sign, m)

    def degree(self):
        return len(self._coefficients) - 1

    def der(self, d=1):
        coefficients = self._coefficients
        while d > 0 and coefficients:
            der_coefficients = []
            for i, c in list(enumerate(coefficients))[1:]:
                der_coefficients.append(c * i)
            coefficients = der_coefficients
            d -= 1
        return Polynomial(coefficients)

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            a = self._coefficients
            b = other._coefficients
            n, m = self.degree(), other.degree()
            c = [
                sum([a[j] * b[i - j] for j in range(
                        max(0, i - m),
                        min(n, i) + 1
                    )]
                ) for i in range(n + m + 1)
            ]
            return Polynomial(c)
        else:
            return Polynomial([a * other for a in self._coefficients])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mod__(self, other):
        raise NotImplementedError

    def __rmod__(self, other):
        raise NotImplementedError

    def gcd(self, other):
        raise NotImplementedError

    def __iter__(self):
        self.iter_num = 0
        return self

    def __next__(self):
        cur = self.iter_num
        self.iter_num += 1
        if cur > self.degree():
            raise StopIteration()
        return (cur, self._coefficients[cur])
