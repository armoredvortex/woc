import random
from math import gcd
from sympy import mod_inverse

def generate_large_prime(bitsize):
    while True:
        prime_candidate = random.getrandbits(bitsize)
        if prime_candidate % 2 == 0:
            prime_candidate += 1
        if is_prime(prime_candidate):
            return prime_candidate

def is_prime(n, k=5):
    """Miller-Rabin algorithm."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

def lcm(a, b):
    return a * b // gcd(a, b)

def l_function(x, n):
    return (x - 1) // n

def generate_paillier_keys(bitsize=512):
    # p and q
    p = generate_large_prime(bitsize)
    q = generate_large_prime(bitsize)

    while p == q:
        q = generate_large_prime(bitsize)

    # n and lambda
    n = p * q
    lambda_value = lcm(p - 1, q - 1)

    # choose random integer g
    n_square = n * n
    g = random.randint(1, n_square - 1)

    # ensure g is valid
    if gcd(l_function(pow(g, lambda_value, n_square), n), n) != 1:
        raise ValueError("Iinvalid g value")

    # mu
    l_value = l_function(pow(g, lambda_value, n_square), n)
    mu = mod_inverse(l_value, n)

    # keys
    public_key = (n, g)
    private_key = (lambda_value, mu)

    return public_key, private_key


def encrypt(public_key, plaintext):
    n, g = public_key
    n_square = n * n

    # r
    r = random.randint(1, n - 1)

    # c = g^m * r^n mod n^2
    c = (pow(g, plaintext, n_square) * pow(r, n, n_square)) % n_square

    return c

def decrypt(private_key, public_key, ciphertext):
    n, g = public_key
    lambda_value, mu = private_key
    n_square = n * n

    # m = L(c^lambda mod n^2) * mu mod n
    l_value = l_function(pow(ciphertext, lambda_value, n_square), n)
    plaintext = (l_value * mu) % n

    return plaintext
