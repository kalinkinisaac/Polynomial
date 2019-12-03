from .base import BasePolynomial
from collections.abc import Iterable


class Polynomial(BasePolynomial):
    def __init__(self, *args):
        super().__init__()

        self.__vector = []

        if len(args) == 1:
            self.__vector = args[0]

        elif len(args) > 1:
            self.__vector = args

        if not isinstance(self.__vector, Iterable):
            raise TypeError('Polynomial vector should be iterable')

        self.__vector = list(self.__vector)

        # Removing trailing zeros
        while self.__vector and self.__vector[-1] == 0:
            self.__vector.pop()

    def __repr__(self):
        return f'Polynomial {repr(self.__vector)}'

    def __str__(self):
        rev = list(reversed(list(enumerate(self.__vector))))
        return ' '.join([Polynomial.monomial_to_str(*rev[0], leading_sign=False)] + list(
            map(lambda ix: Polynomial.monomial_to_str(*ix),
                rev[1:])))

    def __add__(self, other):
        if isinstance(other, Polynomial):
            a = self.__vector
            b = other.__vector
            if len(a) > len(b):
                a, b = b, a
            return Polynomial([x + y for x, y in zip(a, b)] + b[len(a):])
        else:
            return Polynomial([self.__vector[0] + other] + self.__vector[1:])

    def __sub__(self, other):
        return self + (-other)

    def __neg__(self):
        return Polynomial([-x for x in self.__vector])

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return self.__vector == other.__vector
        else:
            return len(self.__vector) == 1 and self.__vector[0] == other

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def monomial_to_str(i, a, leading_sign=True):
        result = ''
        if a == 0:
            return result
        if a < 1:
            result += '- '
        if leading_sign:
            if a >= 0:
                result += '+ '

        if abs(a) != 1 or i == 0:
            result += str(a)
        if i == 1:
            result += 'x'
        elif i > 1:
            result += f'x^{i}'

        return result

    def degree(self):
        raise NotImplementedError
