import os
from dotenv import load_dotenv
from jwt import encode, decode



def encode_jwt(payload) -> str :

    load_dotenv()
    secret_key = os.getenv("SECRET_KEY")
    return encode(payload, secret_key, algorithm='HS256')


def decode_jwt(jwt_token) -> dict :
    load_dotenv()
    secret_key = os.getenv("SECRET_KEY")
    return decode(jwt_token, secret_key, algorithms=['HS256'])


__all__ = ['encode_jwt', 'decode_jwt']



if __name__ == "__main__" :
    payload = {'Name' : 'SHASHANK', 'Age' : '21'}
    encoded_jwt = encode_jwt(payload)
    print("JWT Token:", encoded_jwt)

    decoded_jwt = decode_jwt(encoded_jwt)
    print("Payload:", decoded_jwt)
