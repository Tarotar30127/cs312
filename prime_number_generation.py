import sys
import random
from time import time

sys.setrecursionlimit(3000)

# You will need to implement this function and change the return value.
def mod_exp(x: int, y: int, N: int) -> int:
    if y == 0:
        return 1
    z: int = mod_exp(x, y // 2, N)
    if y % 2 == 0:
        return (z ** 2) % N
    return x * (z ** 2) % N


def fermat(N: int, k: int) -> bool:
    """
    Returns True if N is prime
    """
    for i in range(k):
        r = random.randint(1, N - 1)
        if mod_exp(r, N - 1, N) != 1:
            return False
    return True


def miller_rabin(N: int, k: int) -> bool:
    """
    Returns True if N is prime
    """
    return False


def generate_large_prime(n_bits: int) -> int:
    """Generate a random prime number with the specified bit length"""
    while True:
        i = random.getrandbits(n_bits)
        if fermat(i, 20):
            return i  # https://xkcd.com/221/


def main(n_bits: int):
    start = time()
    large_prime = generate_large_prime(n_bits)
    print(large_prime)
    print(f'Generation took {(time() - start) * 1000} Ms')


if __name__ == '__main__':
    main(int(sys.argv[1]))
