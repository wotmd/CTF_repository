from base64 import b64decode
from socket import socket

ADDR = 'localhost', 7777
KEY_LEN = 128

def get_msg():
    while True:
        with socket() as s:
            s.connect(ADDR)
            msg = b64decode(s.recv(3000))
        if len(msg) == 2039:
            return msg

def xor_bytetrings(a, b):
    return bytes((x^y for x,y in zip(a,b)))

def find_msgs():
    msgs ={get_msg()}
    needed = set(range(128))

    while needed:
        print(len(msgs), needed)
        new_msg = get_msg()
        for msg in list(msgs):
            xor_key = xor_bytetrings(new_msg, msg)
            good_part, last_part = xor_key[:KEY_LEN], xor_key[KEY_LEN:]

            if good_part in last_part:
                i = last_part.index(good_part)
                print('\t', i)
                if i in needed:
                    yield (i+KEY_LEN, new_msg)
                    needed -= {i}
                    msgs -= {msg}
                    continue
        msgs.add(new_msg)

if __name__ == "__main__":
### STEP 1. find key_length and Save
    for i, text in find_msgs():
        with open('key_{0:0>3}_c'.format(i), 'wb') as f:
            f.write(text)

# yeild : http://kkamikoon.tistory.com/90  , https://dojang.io/mod/page/view.php?id=1119

