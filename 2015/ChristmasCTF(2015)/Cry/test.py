from flag import a, b, c, key

def what(n):
    A = [[1, 1], [1, 0]]
    res = [[1, 0], [0, 1]]
    for i in xrange(n):
        tmp = [[0, 0], [0, 0]]
        tmp[0][0] = ( res[0][0] + res[1][0]) % n
        tmp[0][1] = ( res[0][1] + res[1][1]) % n
        tmp[1][0] = ( res[0][0] ) % n
        tmp[1][1] = ( res[0][1] ) % n
        res = tmp

    return res

n = a * b * c
m = int(key.encode('hex'), 16)

assert pow(2, n-1, n) == 1
assert what(n)[0][0] == 0
##2^n-1을 n으로 나눈건 1이다
##피보나치 수열에서 n번째수를 mod n한것
##위 내용은 맞는게 틀림없다

print a + b + c
print sum(divmod(m, a) + divmod(m, b) + divmod(m, c))
##나머지 몫 죄다 더햇네 이거;