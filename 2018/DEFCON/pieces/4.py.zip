import string

def func(num, token):
	Serial = bin(num)[2:]
	token = bin(token)[2:]
	len_t = len(token)
	while not (Serial.find(token) == -1):
		fro_idx = Serial.find(token)
		end_idx = Serial.rfind(token)
		
		if(fro_idx+len_t-1 >= end_idx ):
			fro_Serial = Serial[0:fro_idx]+ Serial[fro_idx+len_t:]
			end_Serial = Serial[0:end_idx]+ Serial[end_idx+len_t:]
			cnt1 = fro_Serial.count(token)
			cnt2 = end_Serial.count(token)
			if(cnt1 > cnt2):
				Serial = fro_Serial
			else:
				Serial = end_Serial
		elif(fro_idx == end_idx):
			Serial = Serial[0:fro_idx]+ Serial[fro_idx+len_t:]
		else:
			Serial = Serial[0:fro_idx]+ Serial[fro_idx+len_t:]
			end_idx = Serial.rfind(token)
			Serial = Serial[0:end_idx]+ Serial[end_idx+len_t:]
		
	return len(Serial)

num = int(input())
token = int(input())
	
len = func(num,token)
print(len)