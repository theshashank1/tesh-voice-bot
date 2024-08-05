from jwt import encode, decode

secret_key = "251998SH"


def encode_jwt(payload, secret_key) -> str :
    return encode(payload, secret_key, algorithm='HS256')


def decode_jwt(jwt_token, secret_key) -> dict :
    return decode(jwt_token, secret_key, algorithms=['HS256'])


if __name__ == "__main__" :
    payload = {'Name' : 'SHASHANK', 'Age' : '21'}
    encoded_jwt = encode_jwt(payload, secret_key)
    print("JWT Token:", encoded_jwt)

    decoded_jwt = decode_jwt(encoded_jwt, secret_key)
    print("Payload:", decoded_jwt)
