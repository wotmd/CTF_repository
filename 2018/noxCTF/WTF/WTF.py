
"""
Rolalala - 2016 - Wiener's attack 
useful link : http://math.unice.fr/~walter/L1_Arith/cours2.pdf
"""
import math

def DevContinuedFraction(num, denum) :
	partialQuotients = []
	divisionRests = []
	for i in range(int(math.log(denum, 2)/1)) :
		divisionRests = num % denum
		partialQuotients.append(num / denum)
		num = denum
		denum = divisionRests
		if denum == 0 :
			break
	return partialQuotients

""" (cf. useful link p.2) Theorem :
p_-2 = 0 p_-1 = 1   p_n = a_n.p_n-1 + p_n-2
q_-2 = 1 q_-1 = 0   q_n = a_n.q_n-1 + q_n-2 
"""
def DivergentsComputation(partialQuotients) :
	(p1, p2, q1, q2) = (1, 0, 0, 1)
	convergentsList = []
	for q in partialQuotients :
		pn = q * p1 + p2
		qn = q * q1 + q2
		convergentsList.append([pn, qn])
		p2 = p1
		q2 = q1
		p1 = pn
		q1 = qn
	return convergentsList    

"""  
https://dzone.com/articles/cryptographic-functions-python
Be careful to physical attacks see sections below
"""
def SquareAndMultiply(base,exponent,modulus):
	binaryExponent = []
	while exponent != 0:
		binaryExponent.append(exponent%2)
        	exponent = exponent/2
	result = 1
	binaryExponent.reverse()
	for i in binaryExponent:
		if i == 0:
			result = (result*result) % modulus
		else:
			result = (result*result*base) % modulus
	return result

def WienerAttack(e, N, C) :
	testStr = 42 
	C = SquareAndMultiply(testStr, e, N)
	for c in DivergentsComputation(DevContinuedFraction(e, N)) :
		if SquareAndMultiply(C, c[1], N) == testStr :
			FullReverse(N, e, c)
			return c[1]
	return -1

"""
Credit for int2Text : 
https://jhafranco.com/2012/01/29/rsa-implementation-in-python/
"""
def GetTheFlag(C, N, d) :
	p = pow(C, d, N)
	print p
	size = len("{:02x}".format(p)) // 2
	print "Flag = "+"".join([chr((p >> j) & 0xff) for j in reversed(range(0, size << 3, 8))])

"""
http://stackoverflow.com/questions/356090/how-to-compute-the-nth-root-of-a-very-big-integer
"""
def find_invpow(x,n):
	high = 1
	while high ** n < x:
		high *= 2
	low = high/2
	while low < high:
		mid = (low + high) // 2
		if low < mid and mid**n < x:
			low = mid
		elif high > mid and mid**n > x:
			high = mid
		else:
			return mid
	return mid + 1

"""
On reprend la demo on cherche (p, q), avec la recherche des racines du P
de scd degre : x^2 - (N - phi(N) + 1)x + N
"""
def FullReverse(N, e, c) :
	phi = (e*c[1]-1)//c[0]
	a = 1
	b = -(N-phi+1)
	c = N
	delta =b*b - 4*a*c
	if delta > 0 :
		x1 = (-b + find_invpow((b*b - 4*a*c), 2))/(2*a)
		x2 = (-b - find_invpow((b*b - 4*a*c), 2))/(2*a)
		if x1*x2 == N :
			print "p = "+str(x1)
			print "q = "+str(x2)
		else :
			print "** Error **"
	else :
		print "** ERROR : (p, q)**"

"""
Si N, e, C en hex ::> int("0x0123456789ABCDEF".strip("0x"), 16)
"""
if __name__ == "__main__":
	N = 106464658120038110366171046017584728605432723415099799671398095113303220554018149888866005570730116293196252665770382258833879353944414043672822102509840890423260826373058255315521685967807858850204383823245609286166175687064317570157147353365780181201403742497875436372013183350667001942660780839408462806879
	e = 18165674577527345773800436360005849487629584246818834218136555374150149407637407524285601002127374055517203100485286275425145721883636036574242949710753834106366928190387866524288552807173498852374689387479028711005571557055252495247965030797704485232834280077859527260792773150470416827810790513797809193767
	C = 50580369027283924057750666670063776841058648997085062866999922168619348147835294586026456440255964021397419618768574389303695295198185200651940566009361144298479342683804462799603255800822644178980917553507665174247302696908288887870589321087856967128660867568458719153439705061463984601603743261513119776696

	print "e : "+str(e)
	print "N : "+str(N)
	print "C : "+str(C)
	d = WienerAttack(e, N, C)
	if d != -1 :
		print "d = "+str(d)
		GetTheFlag(C, N, d)
	else :
		print "** ERROR : Wiener's attack Impossible**"