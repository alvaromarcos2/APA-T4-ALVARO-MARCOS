"""
Generación de números aleatorios mediante el algoritmo LGC. Alvaro Marcos
"""

M_POSIX = 2**48
A_POSIX = 25214903917
C_POSIX = 11
X0_DEFAULT = 1212121


class Aleat:
    """
    Clase que genera números aleatorios usando el algoritmo LGC.

    La secuencia se genera aplicando la fórmula: x = (a*x + c) % m

    Atributos:
        m: módulo
        a: multiplicador
        c: incremento
        x: valor actual de la secuencia

    El método __call__ permite reiniciar la secuencia con una nueva semilla.

    >>> rand = Aleat(m=32, a=9, c=13, x0=11)
    >>> for _ in range(4):
    ...     print(next(rand))
    16
    29
    18
    15

    >>> rand(29)
    >>> for _ in range(4):
    ...     print(next(rand))
    18
    15
    20
    1
    """

    def __init__(self, *, m=M_POSIX, a=A_POSIX, c=C_POSIX, x0=X0_DEFAULT):
        self.m = m
        self.a = a
        self.c = c
        self.x = x0

    def __iter__(self):
        return self

    def __next__(self):
        self.x = (self.a * self.x + self.c) % self.m
        return self.x

    def __call__(self, x0, /):
        self.x = x0


def aleat(*, m=M_POSIX, a=A_POSIX, c=C_POSIX, x0=X0_DEFAULT):
    """
    Función generadora de números aleatorios usando el algoritmo LGC.

    Argumentos (todos opcionales y por clave):
        m: módulo (por defecto 2^48, estándar POSIX)
        a: multiplicador (por defecto 25214903917)
        c: incremento (por defecto 11)
        x0: semilla inicial (por defecto 1212121)

    Si se le envía un valor con send(), reinicia la secuencia
    usando ese valor como nueva semilla.

    >>> rand = aleat(m=64, a=5, c=46, x0=36)
    >>> for _ in range(4):
    ...     print(next(rand))
    34
    24
    38
    44

    >>> rand.send(24)
    38
    >>> for _ in range(4):
    ...     print(next(rand))
    44
    10
    32
    14
    """
    x = x0
    while True:
        x = (a * x + c) % m
        seed = yield x
        if seed is not None:
            x = seed


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)