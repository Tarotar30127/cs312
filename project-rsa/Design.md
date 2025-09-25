Do you understand the math behind the ModExp algorithm?
    Yes, 
    Can you explain that algorithm to someone else?
    Can you implement the algorithm by hand?
What is the pseudocode for the Fermat primality test?

    Yes, you input a positive integer number and  

    How does the Fermat primality test use the ModExp algorithm?
What is the pseudocode for generating large prime numbers?
    How does this algorithm use the Fermat primality test?
How will you track and plot the empirical measurements?
    matplotlibs and put data into graphs
    How will you measure the constant of proportionality?
    timeit tracemalloc


prime_number_generation.py Design
    def mod_exp(x: int, y: int, N: int) -> int:
        base case:If y==0: return1
	    Z = mod_exp(x,y//2, N)
	    If y is even : # b%2000
		    Return z^2 (mod N) #(z**2)%N
	    Else return z^2*a(modN)


def fermat(N: int, k: int) -> bool:
    """
    Returns True if N is prime
    """
    for i in k:
        if !((i^n) mod n ==1):
            return False
    return true


def miller_rabin(N: int, k: int) -> bool:
    """
    Returns True if N is prime
    """
    return False


def generate_large_prime(n_bits: int) -> int:
    """Generate a random prime number with the specified bit length"""
    while True do 
    choose a random nbit number p
    primetest2(p) = 'yes'
    return p  # https://xkcd.com/221/