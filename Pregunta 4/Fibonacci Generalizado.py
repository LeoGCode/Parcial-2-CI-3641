# 18-10638
# X = 6, Y = 3, Z = 8
# alpha = ((6 + 3) % 5) + 3 = 7
# beta = ((3 + 8) % 5) + 3 = 4

import matplotlib.pyplot as plt
import time
import sys
sys.setrecursionlimit(1000000)

# Constants values
ALPHA = ((6 + 3) % 5) + 3
BETA = ((3 + 8) % 5) + 3
ALPHA_BETA = ALPHA * BETA


def fibonacci74(n) -> int:
    """
    Esta función calcula el n-ésimo número de la sucesión de Fibonacci generalizada con
    los parámetros ALPHA = 7 y BETA = 4.
    :param n: n-esimo termino de la sucesión de Fibonacci generalizada a ser calculado
    :return: n-ésimo número de la sucesión de Fibonacci generalizada con los parámetros ALPHA = 7 y BETA = 4
    """
    if 0 <= n < ALPHA_BETA:
        return n
    elif n >= ALPHA_BETA:
        r = sum(fibonacci74(n - BETA * i) for i in range(1, ALPHA + 1))
        return r


def fibonacci74_tail(n: int) -> int:
    """
    Esta función calcula el n-ésimo número de la sucesión de Fibonacci generalizada con
    una recursión de cola:
    :param n: n-esimo termino de la sucesión de Fibonacci generalizada a ser calculado
    :return: n-ésimo número de la sucesión de Fibonacci generalizada con una recursión de cola
    """
    i = n % BETA
    tail = [i + j * BETA for j in range(ALPHA)]
    return _fibonacci74_tail(n, tail)


def _fibonacci74_tail(n: int, x: list) -> int:
    """
    Funcion auxiliar para la función fibonacci74_tail
    :param n: n-esimo termino de la sucesión de Fibonacci generalizada a ser calculado
    :param x: cola de valores ya calculados
    :return: n-ésimo número de la sucesión de Fibonacci generalizada con una recursión de cola
    """
    if 0 <= n < ALPHA_BETA:
        return n

    suma = sum(x)
    if 0 <= n - BETA < ALPHA_BETA:
        return suma

    x = x[1:]
    x.append(suma)
    return _fibonacci74_tail(n - BETA, x)


def fibonacci74_iterative(n: int) -> int:
    """
    Esta función calcula el n-ésimo número de la sucesión de Fibonacci generalizada de forma iterativa
    :param n: n-esimo termino de la sucesión de Fibonacci generalizada a ser calculado
    :return: n-ésimo número de la sucesión de Fibonacci generalizada de forma iterativa
    """
    i = n % BETA
    tail = [i + j * BETA for j in range(ALPHA)]
    while n > ALPHA * BETA:
        if 0 <= n < ALPHA * BETA:
            return n

        suma = sum(tail)
        if 0 <= n - BETA < ALPHA_BETA:
            return suma

        tail = tail[1:]
        tail.append(suma)
        n -= BETA

    return sum(tail)

if __name__ == '__main__':
    times = [i for i in range(0, 140, 10)]
    times_fibonacci74 = [[],[],[]]
    for i in times:
        start = time.time()
        fibonacci74(i)
        end = time.time()
        times_fibonacci74[0].append(end - start)
        start = time.time()
        fibonacci74_tail(i)
        end = time.time()
        times_fibonacci74[1].append(end - start)
        start = time.time()
        fibonacci74_iterative(i)
        end = time.time()
        times_fibonacci74[2].append(end - start)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    plt.suptitle('Tiempos de ejecución de la sucesión de Fibonacci generalizada (alpha = 7 y beta = 4)')

    ax1.plot(times, times_fibonacci74[0], label='Recursion directa')
    ax1.plot(times, times_fibonacci74[1], label='Recursión de cola')
    ax1.plot(times, times_fibonacci74[2], label='Iterativo')
    ax1.legend()
    ax1.set_title('Con recursión directa')
    ax1.set_xlabel('n-esimo termino')
    ax1.set_ylabel('Tiempo de ejecución (segundos)')

    times = [i for i in range(2000, 80000, 1000)]
    times_fibonacci74 = [[],[]]
    for i in times:
        start = time.time()
        fibonacci74_tail(i)
        end = time.time()
        times_fibonacci74[0].append(end - start)
        start = time.time()
        fibonacci74_iterative(i)
        end = time.time()
        times_fibonacci74[1].append(end - start)
    ax2.plot(times, times_fibonacci74[0], label='Recursión de cola')
    ax2.plot(times, times_fibonacci74[1], label='Iterativo')
    ax2.legend()

    ax2.set_title('Sin recursion directa')
    ax2.set_xlabel('n-esimo termino')

    plt.show()
