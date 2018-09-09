BLOCK_SIZE = 40

def block2bin(b, length=BLOCK_SIZE):
    return list(map(int, bin(b)[2:].rjust(length, '0')))

def bin2block(b):
    return int("".join(map(str, b)), 2)

	
n = "./dir"
n = n.encode("hex")
n = int(n,16)

print(bin(n)[2:].rjust(40, '0'))

n = "cat *"
n = n.encode("hex")
n = int(n,16)

print(bin(n)[2:].rjust(40, '0'))

s = "0010111000101111011001000110100101110010"
d = "0010111000101111011001000110100101110010"
d = "0010111000101111011001000110100101110010"
d = bin2block(d)
print("%x" % d)
d=str(hex(d))[2:]
d=d.decode("hex")
print(d)




