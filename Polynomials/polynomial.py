from .base import BasePolynomial
from collections.abc import Iterable


class Polynomial(BasePolynomial):
    def __init__(self, *coefficients):
        super().__init__()

        self.__coefficients = []

        if len(coefficients) == 1:
            if isinstance(coefficients[0], Polynomial):
                self.__coefficients = list(coefficients[0].__coefficients)
            elif isinstance(coefficients[0], dict):
                d = coefficients[0]
                degree = max(map(int, d.keys()))
                self.__coefficients = [
                    d[i] if i in d else 0 for i in range(degree + 1)
                ]
            elif isinstance(coefficients[0], Iterable):
                self.__coefficients = coefficients[0]
            else:
                self.__coefficients = coefficients

        elif len(coefficients) > 1:
            self.__coefficients = coefficients


        self.__coefficients = list(self.__coefficients)

        # Removing trailing zeros
        while self.__coefficients and self.__coefficients[-1] == 0:
            self.__coefficients.pop()

        if not self.__coefficients:
            self.__coefficients = [0]

    def __repr__(self):
        return f'Polynomial {repr(self.__coefficients)}'

    def __str__(self):
        monomials = list(reversed(list(map(
            Polynomial.monomial_to_str,
            enumerate(self.__coefficients)
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
            a = self.__coefficients
            b = other.__coefficients
            if len(a) > len(b):
                a, b = b, a
            return Polynomial([x + y for x, y in zip(a, b)] + b[len(a):])
        else:
            return Polynomial([self.__coefficients[0] + other] + self.__coefficients[1:])

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    def __neg__(self):
        return Polynomial([-x for x in self.__coefficients])

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return self.__coefficients == other.__coefficients
        else:
            return len(self.__coefficients) == 1 and self.__coefficients[0] == other

    def __call__(self, x):
        result = 0
        for a in reversed(self.__coefficients):
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
        return len(self.__coefficients) - 1

    def der(self, d=1):
        coefficients = self.__coefficients
        while d > 0 and coefficients:
            der_coefficients = []
            for i, c in list(enumerate(coefficients))[1:]:
                der_coefficients.append(c * i)
            coefficients = der_coefficients
            d -= 1
        return Polynomial(coefficients)

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            a = self.__coefficients
            b = other.__coefficients
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
            return Polynomial([a * other for a in self.__coefficients])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mod__(self, other):
        raise NotImplementedError

    def __rmod__(self, other):
        raise NotImplementedError

    def gcd(self, other):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError
