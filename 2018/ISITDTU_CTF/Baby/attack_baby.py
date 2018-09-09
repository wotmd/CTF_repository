import socket

flag_hash = "2c7b44d69a0f28798532e4bb606753128969e484118bd0baa215c6309ce6dc016c9a5601471abf4c556c0dc5525eb4144078a761a6456c919d134be8a10c64a0"

def recv_until(s, string):
    result = ''
    while string not in result:
        result += s.recv(1)
    return result

def get_hash(num):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(('35.185.178.212', 33337))
	recv_until(sock, ':')
	sock.send(str(num)+"\n")
	recv_until(sock, '\n')
	hash = recv_until(sock, '\n')
	sock.close()
	return hash[:-1]

flag = ""
c=0
while(True):
	onebyte = 0
	for i in range(8):
		num = (1<<i)
		hash = get_hash(num<<(8*c))
		if flag_hash==hash:
			onebyte+=num
	c+=1
	flag = chr(onebyte)+flag
	if "ISITDTU{" in flag:
		break
	print(flag)

print("FLAG : " + flag)