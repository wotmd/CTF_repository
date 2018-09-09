from whoareyou import *

class IKnowWhoYouAre(sock_handler):
    def enc(self,plain):
        return str(random.randint(1, 1000000)*p+int(plain.encode("hex"),16)%p)+', '+str(random.randint(1, 1000000)*q+int(plain.encode("hex"),16)%q)
    def handle(self):
        self.request.sendall(self.enc(flag))

if __name__ == '__main__':
    start(IKnowWhoYouAre)


#str(문자열로 바꿔주는거겟지 아마..)
#random.randint(1,1000000) : 1~1000000까지중 무작위로 하나 선택
#plain.encode("hex") : plain을 hex로 바꿈(16진수로)
#plain.decode("hex") : plain을 아스키코드로 바꿈
#int(a,16) : 16진수인 a를 10진수로 바꿈		
0x1d2b540002e56ee311ce8911e6c64ddd5a6cf39bf2878332e6da2053ae1L
	Flag{~}
	23 59 90 58 89 69 49 32 03 89 67 45 62 88
	F   l  a  g  {                          }
	46 6c 61 67 7b 00 00 00 00 00 00 00 00 7b