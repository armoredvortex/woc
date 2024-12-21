from app.paillier import *
import json
from sslib import shamir
import hashlib

def generate_keys():
    public_key, private_key = generate_paillier_keys(512)
    return public_key, private_key

def generate_shares(private_key_b64, quantity, threshold):
    shares = shamir.to_base64(shamir.split_secret(private_key_b64.encode(), threshold, quantity))

    return json.dumps(shares)
    
def recover_secret(shares):
    shares = shamir.from_base64(shares)
    return shamir.recover_secret(shares)

def hash_data(data, salt=None):
    if salt:
        data += salt
    return hashlib.sha256(data.encode()).hexdigest()

def encrypt_vote_vector(public_key, vote_vector):
    return [encrypt(public_key,vote) for vote in vote_vector]
    # return [public_key.encrypt(vote) for vote in vote_vector]

def decrypt_vote_vector(private_key, public_key,encrypted_vote_vector):
    return [decrypt(private_key,public_key,vote) for vote in encrypted_vote_vector]

def homomorphic_add(public_key, ciphertext1, ciphertext2):
    """Perform homomorphic addition on two ciphertexts."""
    n, g = public_key
    n_square = n * n

    # Combine the ciphertexts using multiplication modulo n^2
    combined_ciphertext = (ciphertext1 * ciphertext2) % n_square

    return combined_ciphertext
