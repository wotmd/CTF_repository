from whoareyou import *

class IKnowWhoYouAre(sock_handler):
    def enc(self,plain):
        return str(random.randint(1, 1000000)*p+int(plain.encode("hex"),16)%p)+', '+str(random.randint(1, 1000000)*q+int(plain.encode("hex"),16)%q)
    def handle(self):
        self.request.sendall(self.enc(flag))

if __name__ == '__main__':
    start(IKnowWhoYouAre)


#str(���ڿ��� �ٲ��ִ°Ű��� �Ƹ�..)
#random.randint(1,1000000) : 1~1000000������ �������� �ϳ� ����
#plain.encode("hex") : plain�� hex�� �ٲ�(16������)
#plain.decode("hex") : plain�� �ƽ�Ű�ڵ�� �ٲ�
#int(a,16) : 16������ a�� 10������ �ٲ�		
0x1d2b540002e56ee311ce8911e6c64ddd5a6cf39bf2878332e6da2053ae1L
	Flag{~}
	23 59 90 58 89 69 49 32 03 89 67 45 62 88
	F   l  a  g  {                          }
	46 6c 61 67 7b 00 00 00 00 00 00 00 00 7b