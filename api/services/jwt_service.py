import os
from dotenv import load_dotenv
from jwt import encode, decode



def encode_jwt(payload) -> str :

    load_dotenv()
    secret_key = os.getenv("SECRET_KEY")
    return encode(payload, secret_key, algorithm='HS256')


# def decode_jwt(jwt_token) -> dict :
#     load_dotenv()
#     secret_key = os.getenv("SECRET_KEY")
#     return decode(jwt_token, secret_key, algorithms=['HS256'])


def decode_jwt(jwt_token) -> dict :
    load_dotenv()
    secret_key = os.getenv("SECRET_KEY")

    # Convert jwt_token to bytes if it's a string
    if isinstance(jwt_token, str) :
        jwt_token = jwt_token.encode('utf-8')

    return decode(jwt_token, secret_key, algorithms=['HS256'])


__all__ = ['encode_jwt', 'decode_jwt']





if __name__ == "__main__" :
    payload = {'Name' : 'SHASHANK', 'Age' : '21'}
    encoded_jwt = encode_jwt(payload)
    print("JWT Token:", encoded_jwt)

    decoded_jwt = decode_jwt("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJOYW1lIjoiU0hBU0hBTksiLCJBZ2UiOiIyMSJ9.5A8NZ3UrVy5qG5waG8bpFYSQP12YlNaDg7inqSAFFiQ")
    print("Payload:", decoded_jwt)
