
from random import randrange
import fractions


def get_primes(n):
	numbers = set(range(n, 1, -1))
	primes = []
	while numbers:
		p = numbers.pop()
		primes.append(p)
		numbers.difference_update(set(range(p*2, n+1, p)))
	return primes

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def miller_rabin(n, k):
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

while 1:
	### main #################
	primes = get_primes(443)
	primes.sort()
	del primes[0]
	##print primes

	pi = 1;
	for x in primes:
		pi *= x
	##print "pi=%X" % pi

	while True:
		kp = randrange(1, 2**12) + 2**12 + 2**13 + 2**14 + \
				2**15 + 2**16 + 2**17 + 2**18 + 2**19
		#print "kp=%X" % kp

		tp = 0
		while fractions.gcd(tp, pi) != 1:
			#print "trying..."
			tp = randrange(1, 2**399);
		#print "tp=%X" % tp

		p = kp * pi * 2**400 + tp
		#print "p=%X" % p
		#print "bitlength(p)=", len(bin(p))-2

		if miller_rabin(p, 40) == True:
			break

	while True:
		kq = randrange(1, 2**12) + 2**12 + 2**13 + 2**14 + \
				2**15 + 2**16 + 2**17 + 2**18 + 2**19
		#print "kq=%X" % kq

		tq = 0
		while fractions.gcd(tq, pi) != 1:
			#print "trying..."
			tq = randrange(1, 2**399);
		#print "tq=%X" % tq

		q = kq * pi * 2**400 + tq
		#print "q=%X" % q
		#print "bitlength(q)=", len(bin(q))-2

		if miller_rabin(q, 40) == True:
			break

	#print "p=%X" % p
	#print "q=%X" % q
	
	n = p * q
	
	if n == A4E20DDB854955794E7ABF4AE40051C0FC30488C82AB93B7DD046C1CC094A54334C97E84B523BD3F79331EBEAF5249200D729A483D5B8D944D58DF18D2CA9401B1A1A6CDA8A3AC5C234A501794B76886C426FAC35AD9615ADAB5C94B58C03CCFFA891CE0156CBC14255F019617E40DE9124FBBE70D64CD823DCA870FF76B649320927628250D47DB8DFA9BBCE9964CB3FE3D1B69845BD6FA2E6938DDA1F109E5F4E4170C845B976BBD5121107642FC00606208F9BC83322532739BCFEAF706FB2AF985EBD9769C7FBD50ECBF55566BD44FB241F9FD2DE25069AA8C744F0558514F1E9C8E4297A4D4B25D9F2B7494B466C2E6E2834BA68C5C824215018368B4FB :
		
		#print "n=%X" % n
		#print "bitlength(n)=", len(bin(n))-2

		e = 2**16 + 1
		#print "e=%X" % e
		##print "bitlength(e)=", len(bin(e))-2

		d = modinv(e, (p-1)*(q-1))
		#print "d=%X" % d
		##print "bitlength(d)=", len(bin(d))-2

		m = 12354178254918274687189741234123412398461982374619827346981756309845712384198076
		#print "m=%X" % m
		#print "bitlength(m)=", len(bin(m))-2

		#c = pow(m, e, n)
		#print "c=%X" % c
		#print "bitlength(c)=", len(bin(c))-2

		c=64A3F710E3CB9B114FD112B45AC4845292D0B1FEE1468147E80FABA3CD56B1206F5C59E5D400A7F20C9BCD5B42C7197A0D07FBBA48BFBDA550C5CAFB562BEC1B1CB301D131E13233F2BD1C80EEB48956FF0BC8DB6AE2CD727FB1DAC62822331B15A6044F825D01D81036DA3CC8A3575165E813051036715CDF5F7865676DC2513AAD08C5113DFFDC4E6B13E6FFCA2FAD1AA6986D3ED9F1896C109F641074DA7DBFE62CCAD3CACE4B80332475FE3C9EC4869FCA31EE2860D45959F8583C2AEC7A00FC2FD63DBF6CBEB1C604D60CF780FE028ED0AD65DC74BC5335F96EE7CEDEA292F76B427E5F402BCC609B39302CD4A51F405C6ACF8B8A7569AAD9A9318F060B

		m2 = pow(c, d, n)
		print "m2=%X" % m2
		print "bitlength(m2)=", len(bin(m2))-2
		
		break
