from base64 import encode
from cryptography.fernet import Fernet
import cryptography
import json
import ast
import time

JWT_ISSUER = 'domroon.de'
JWT_SECRET = b'canqPbW5nzW4t5QneAEVqVELvXdEX2CTmPsd8kaacWc='
JWT_LIFETIME_SECONDS = 30

#key = Fernet.generate_key()
KEY = b'canqPbW5nzW4t5QneAEVqVELvXdEX2CTmPsd8kaacWc='
KEY_OBJ = Fernet(KEY)

def tests():
    f = Fernet(KEY)

    # token = f.encrypt(b"deep secret!!")

    # print(f'KEY {KEY}')

    # print(f'encrypted {token}')

    # token_dec = f.decrypt(token)

    # print(f'descripted {token_dec}')

    # saved_token = b'gAAAAABhMICwotcaCPTN8t_IbdcbGzS_PSEZU-9icyq4VQjU7rKmfASPTLZBvGOEao9tOuvHaA6YD8-RAX1QRPeUZyx6O9GRQA=='

    # token_dec = f.decrypt(saved_token)
    # print(f'descripted BEFORE {token_dec}')

    # # changed token the second "=" at the end is deleted
    # malicious_token = b'gAAAAABhMICwotcaCPTN8t_IbdcbGzS_PSEZU-9icyq4VQjU7rKmfASPTLZBvGOEao9tOuvHaA6YD8-RAX1QRPeUZyx6O9GRQA='

    # try:
    #     mal_token_dec = f.decrypt(malicious_token)
    #     print(f'descripted MALICIOUS {token_dec}')
    # except cryptography.fernet.InvalidToken:
    #     print(f'[INVALID] Token: {malicious_token}')



    # payload = {
    #         "iss": JWT_ISSUER,
    #         "iat": IAT_TEST, #int(timestamp),
    #         "exp": EXP_TEST, #int(timestamp + JWT_LIFETIME_SECONDS),
    #         "sub": SUB_TEST, #str(user_id),
    # }

    # print(" ")
    # print(f'payload {payload}')
    # print(f'type: {type(payload)}')

    # bytes_payload = json.dumps(payload).encode('utf-8')
    # print(f'bytes_payload {bytes_payload}')

    # enc_payload = f.encrypt(bytes_payload)
    # print(f'enc_payload (this is the token) {enc_payload}')

    dec_payload = f.decrypt(enc_payload)
    print(f'dec_payload {dec_payload}')

    str_payload = dec_payload.decode('utf-8')
    dict_payload = ast.literal_eval(str_payload)
    print(f'dict_payload {dict_payload}')
    print(f'type: {type(dict_payload)}')

    print(f'show item at key exp: {dict_payload["exp"]}')

    timestamp = time.time()
    timestamp_int = int(time.time())
    print(f'timestamp: {timestamp} TYPE: {type(timestamp)}')
    print(f'timestamp: {timestamp_int} TYPE: {type(timestamp_int)}')


# add bcrypt for implement encrypted password for database
# implement to load user with username form database 
# implement check encrypted password
# change function to functions that can be used as decorator

def _current_timestamp() -> int:
    return int(time.time())


def generate_token(username):
    # get username from database and check the password (encrypted by bcrypt)
    # for testing:
    timestamp = _current_timestamp()
    payload = {
            "iss": JWT_ISSUER,
            "iat": int(timestamp),
            "exp": int(timestamp + JWT_LIFETIME_SECONDS),
            "sub": str(username),
    }

    bytes_payload = json.dumps(payload).encode('utf-8')

    return KEY_OBJ.encrypt(bytes_payload)


def decode_token(token):
    encoded_token = token.encode('utf-8')
    try:
        token_dec = KEY_OBJ.decrypt(encoded_token)
    except cryptography.fernet.InvalidToken:
        return 'Unauthorized'

    token_str = token_dec.decode('utf-8')
    token_dict = ast.literal_eval(token_str)

    if int(_current_timestamp()) >= token_dict["exp"]:
        return 'Token expired'
    else:
        return token_dict


# def main():
#     choice = input("1 - Generate Token       2 - Decode Token")

#     if choice == "1":
#         print(generate_token("domroon", "geheim", key_obj))
#     elif choice == "2":
#         token = input("Token: ")
#         print(decode_token(token, key_obj))
#     else:
#         print("Invalid choice")


# if __name__ == '__main__':
#     main()

