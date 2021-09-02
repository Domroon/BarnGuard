from cryptography.fernet import Fernet
import cryptography
import json
import ast

#key = Fernet.generate_key()
KEY = b'canqPbW5nzW4t5QneAEVqVELvXdEX2CTmPsd8kaacWc='

f = Fernet(KEY)

token = f.encrypt(b"deep secret!!")

print(f'KEY {KEY}')

print(f'encrypted {token}')

token_dec = f.decrypt(token)

print(f'descripted {token_dec}')

saved_token = b'gAAAAABhMICwotcaCPTN8t_IbdcbGzS_PSEZU-9icyq4VQjU7rKmfASPTLZBvGOEao9tOuvHaA6YD8-RAX1QRPeUZyx6O9GRQA=='

token_dec = f.decrypt(saved_token)
print(f'descripted BEFORE {token_dec}')

# changed token the second "=" at the end is deleted
malicious_token = b'gAAAAABhMICwotcaCPTN8t_IbdcbGzS_PSEZU-9icyq4VQjU7rKmfASPTLZBvGOEao9tOuvHaA6YD8-RAX1QRPeUZyx6O9GRQA='

try:
    mal_token_dec = f.decrypt(malicious_token)
    print(f'descripted MALICIOUS {token_dec}')
except cryptography.fernet.InvalidToken:
     print(f'[INVALID] Token: {malicious_token}')

# REAL TOKEN TEST

JWT_ISSUER = "domroon.de"
IAT_TEST = "2021-09-02"
EXP_TEST = "2021-09-02"
SUB_TEST = "2021-09-02"

payload = {
        "iss": JWT_ISSUER,
        "iat": IAT_TEST, #int(timestamp),
        "exp": EXP_TEST, #int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": SUB_TEST, #str(user_id),
}

print(" ")
print(f'payload {payload}')
print(f'type: {type(payload)}')

bytes_payload = json.dumps(payload).encode('utf-8')
print(f'bytes_payload {bytes_payload}')

enc_payload = f.encrypt(bytes_payload)
print(f'enc_payload (this is the token) {enc_payload}')

dec_payload = f.decrypt(enc_payload)
print(f'dec_payload {dec_payload}')

str_payload = dec_payload.decode('utf-8')
dict_payload = ast.literal_eval(str_payload)
print(f'dict_payload {dict_payload}')
print(f'type: {type(dict_payload)}')

print(f'show item at key exp: {dict_payload["exp"]}')