from Crypto.Util.number import *
from hashlib import sha256
import random
import sys
import key

p = 267336782497463360204553349940982883027638137556242083062698936408269688347005688891456763746542347101087588816598516438470521580823690287174602955234443428763823316700034360179480125173290116352018408224011457777828019316565914911469044306734393178495267664516045383245055214352730843748251826260401437050527
q = 133668391248731680102276674970491441513819068778121041531349468204134844173502844445728381873271173550543794408299258219235260790411845143587301477617221714381911658350017180089740062586645058176009204112005728888914009658282957455734522153367196589247633832258022691622527607176365421874125913130200718525263
g = 2
pk = pow(g, key.sk, p)

with open("/dev/urandom") as f:
    _random_seed = bytes_to_long(f.read(1024/8))
def myRandom():
    global _random_seed
    _random_seed = (_random_seed * 713030730552717 + 123456789) & ((1 << 1024) - 1)
    return _random_seed

# secret key: x
def sign(m, x):
    z = bytes_to_long(sha256(m).digest())
    k = myRandom() % q
    r = pow(g, k, p) % q
    s = (inverse(k, q) * (z + x * r)) % q
    return (r, s)

def verify(m, y, sig):
    (r, s) = sig
    if not (1 <= r <= q - 1): return False
    if not (1 <= s <= q - 1): return False
    z = bytes_to_long(sha256(m).digest())
    w = inverse(s, q)
    u1 = z * w % q
    u2 = r * w % q
    v = pow(g, u1, p) * pow(y, u2, p) % p % q
    return r == v

if __name__ == "__main__":
    for m in ["foo", "bar"]:
        sig = sign(m, key.sk)
        print (m, sig)
        #print verify(m, pk, sig)

