from phe import paillier
import json
from sslib import shamir
import hashlib

def generate_keys():
    public_key, private_key = paillier.generate_paillier_keypair()
        
    public_key_json = json.dumps({
        'n': public_key.n
    })
    
    private_key_json = json.dumps({
        'p': private_key.p,
        'q': private_key.q
    })
    
    return public_key_json, private_key_json

# def reconstruct_keys(public_key_json, private_key_json):
#     public_key_data = json.loads(public_key_json)
#     private_key_data = json.loads(private_key_json)
    
#     public_key = paillier.PaillierPublicKey(n=int(public_key_data['n']))
#     private_key = paillier.PaillierPrivateKey(public_key, p=int(private_key_data['p']), q=int(private_key_data['q']))
    
#     return public_key, private_key

def reconstruct_public_key(public_key_json):
    public_key_data = json.loads(public_key_json)
    public_key = paillier.PaillierPublicKey(n=int(public_key_data['n']))
    return public_key

def reconstruct_private_key(public_key_json, private_key_json):
    private_key_data = json.loads(private_key_json)
    public_key = reconstruct_public_key(public_key_json)
    private_key = paillier.PaillierPrivateKey(public_key, p=int(private_key_data['p']), q=int(private_key_data['q']))
    return private_key

def generate_shares(private_key_json):
    quantity = 3
    threshold = 2
    shares = shamir.to_base64(shamir.split_secret(private_key_json.encode(), threshold, quantity))
    return str(shares)
    
def recover_secret(shares):
    return shamir.recover_secret(shamir.from_base64(shares)).decode()

def hash_data(data, salt=None):
    if salt:
        data += salt
    return hashlib.sha256(data.encode()).hexdigest()