import json
import random

def generate_shares(secret, quantity, threshold):
    # generate coefficients
    secret = int.from_bytes(secret.encode(), 'big')
    coefficients = [secret] + [random.randint(1, 100) for _ in range(threshold - 1)]
    shares = []
    for i in range(1, quantity + 1):
        share = sum([coeff * i ** index for index, coeff in enumerate(coefficients)])
        shares.append((i, share))

    shares = {'required_shares': threshold, 'shares': shares}
    return json.dumps(shares)

def recover_secret(shares):
    shares = shares['shares']
    secret = 0
    print(shares)
    for i, share in shares:
        numerator = 1
        denominator = 1
        for j, other_share in shares:
            if i == j:
                continue
            numerator *= -j
            denominator *= i - j
        secret += share * numerator // denominator
    return secret.to_bytes((secret.bit_length() + 7) // 8, 'big').decode()
