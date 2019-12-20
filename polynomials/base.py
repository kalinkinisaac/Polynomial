from abc import ABC, abstractmethod


class BasePolynomial(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError

    @abstractmethod
    def __str__(self):
        raise NotImplementedError

    @abstractmethod
    def __add__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __sub__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __neg__(self):
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __call__(self, x):
        raise NotImplementedError

    @abstractmethod
    def degree(self):
        raise NotImplementedError

    @abstractmethod
    def der(self, d=1):
        raise NotImplementedError

    @abstractmethod
    def __mul__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __rmul__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __mod__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __rmod__(self, other):
        raise NotImplementedError

    @abstractmethod
    def gcd(self, other):
        raise NotImplementedError

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError

    @abstractmethod
    def __next__(self):
        raise NotImplementedError
