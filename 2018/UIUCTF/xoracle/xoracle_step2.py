import os

KEY_LEN = 128
FILE_LEN = 2039

def xor_bytetrings(a, b):
    return bytes((x^y for x,y in zip(a,b)))

def key2039_gen(key):
    key = key*(FILE_LEN // KEY_LEN)
    key += key[:FILE_LEN % KEY_LEN]
    return key
    
if __name__ == "__main__":
### STEP 2. Xor M1, M2 AND Genearte M[0]^M[i] (i=range(1,128)
    res = [0]
    with open('key_128_c', 'rb') as f: 
        original = f.read()
    
    for i in range(1,128):
        idx=i+KEY_LEN
        with open('key_{0:0>3}_c'.format(idx), 'rb') as f: 
            shifted = f.read()
        
        or_blocks = [original[KEY_LEN*x:KEY_LEN*(x+1)] for x in range(0,2)]
        sh_blocks = [shifted[(KEY_LEN+i)*x:(KEY_LEN+i)*(x+1)] for x in range(0,2)]

        H1 = xor_bytetrings(*or_blocks)
        H2 = xor_bytetrings(*sh_blocks)

        res.append(H1[i] ^ H2[0])

### STEP 3. Bruteforce M[0]
    for m0 in range(256):
        msg_first = [m0^x for x in res]
        key = xor_bytetrings(msg_first, original)
        key = key2039_gen(key);
        
        flag = xor_bytetrings(key, original)
        with open('flag_{0:0>3}'.format(m0), 'wb') as f:
            f.write(flag)

### STEP 4. file operation AND Find Real FLAG!
    for m0 in range(256):
        os.system('file flag_{0:0>3} | grep -v ": data"'.format(m0))



