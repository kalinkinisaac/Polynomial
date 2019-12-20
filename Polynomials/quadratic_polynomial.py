from .polynomial import Polynomial
import math


class QuadraticPolynomial(Polynomial):
    def __init__(self, *args):
        super().__init__(*args)

    def solve(self):
        c, b, a = self._coefficients
        d = b ** 2 - 4 * a * c

        if d < 0:
            return []
        elif d == 0:
            return [(-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)]
        else:
            return [
                (-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a),
                (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
            ]
