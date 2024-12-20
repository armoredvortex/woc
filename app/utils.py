from phe import paillier
import json
from sslib import shamir
import hashlib

def generate_keys():
    public_key, private_key = paillier.generate_paillier_keypair()

    return public_key, private_key

def reconstruct_public_key(public_key_json):
    public_key_data = json.loads(public_key_json)
    public_key = paillier.PaillierPublicKey(n=int(public_key_data['n']))
    return public_key

def reconstruct_private_key(public_key_json, private_key_json):
    private_key_data = json.loads(private_key_json)
    public_key = reconstruct_public_key(public_key_json)
    private_key = paillier.PaillierPrivateKey(public_key, p=int(private_key_data['p']), q=int(private_key_data['q']))
    return private_key

def generate_shares(private_key_b64):
    quantity = 3
    threshold = 2
    # shares = shamir.to_base64(shamir.split_secret(private_key_b64.encode(), threshold, quantity))
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
    return [public_key.encrypt(vote) for vote in vote_vector]

def decrypt_vote_vector(private_key, encrypted_vote_vector):
    return [private_key.decrypt(vote) for vote in encrypted_vote_vector]