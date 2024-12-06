from phe import paillier
import json

def generate_keys():
    public_key, private_key = paillier.generate_paillier_keypair()
    
    print(public_key, private_key)
    
    public_key_json = json.dumps({
        'n': public_key.n
    })
    
    private_key_json = json.dumps({
        'p': private_key.p,
        'q': private_key.q
    })
    
    return public_key_json, private_key_json

def reconstruct_keys(public_key_json, private_key_json):
    public_key_data = json.loads(public_key_json)
    private_key_data = json.loads(private_key_json)
    
    public_key = paillier.PaillierPublicKey(n=int(public_key_data['n']))
    private_key = paillier.PaillierPrivateKey(public_key, p=int(private_key_data['p']), q=int(private_key_data['q']))
    
    return public_key, private_key