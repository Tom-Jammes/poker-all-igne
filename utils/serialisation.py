import pickle
from base64 import b64encode, b64decode

def serialiser_obj(obj):
    return b64encode(pickle.dumps(obj)).decode()

def deserialiser_obj(chaine):
    return pickle.loads(b64decode(chaine.encode()))