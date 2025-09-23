import sys
from time import time
from typing import Any
from prime_number_generation import generate_large_prime
# When trying to find a relatively prime e for (p-1) * (q-1)
# use this list of 25 primes
# If none of these work, throw an exception (and let the instructors know!)
primes = [
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
]


def extended_euclid(a: int, b: int) -> (int, int, int):
    """
    The Extended Euclid algorithm returns x, y, d such that:
    d = GCD(a, b)
    ax + by = d
    Note: a must be greater than b.
    """
    # base case
    if b == 0:
        return a, 1, 0

    d, x1, y1 = extended_euclid(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return d, x, y


def generate_key_pairs(n_bits) -> tuple[int, int, int]:
    """
    Generate RSA public and private key pairs.
    Randomly creates a p and q (two large n-bit primes)
    Computes N = p*q
    Computes e and d such that e*d = 1 mod (p-1)(q-1)
    Return N, e, and d
    """
    p: int = generate_large_prime(n_bits)
    q: int = generate_large_prime(n_bits)
    while p == q:
        q = generate_large_prime(n_bits)
    N: int = p * q
    r: int = (p - 1) * (q - 1)
    e = 0
    d = 0
    for i in primes:
        gcd, x, y = extended_euclid(i, r)
        if gcd == 1:
            e = i
            d = x
            if d < 0:
                d += r
            break
    return N, e, d


def main(n_bits: int, filename_stem: str):
    start = time()
    N, e, d = generate_key_pairs(n_bits)
    print(f'{(time() - start)*1000} milliseconds elapsed')

    public_file = filename_stem + '.public.txt'
    with open(public_file, 'w') as file:
        file.writelines([
            str(N),
            '\n',
            str(e)
        ])
    print(public_file, 'written')

    private_file = filename_stem + '.private.txt'
    with open(private_file, 'w') as file:
        file.writelines([
            str(N),
            '\n',
            str(d)
        ])
    print(private_file, 'written')


if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2])
