

BlindDate = open("BlindDate.jpeg","r").read()
recoverBlind = ""

for i in range(4, len(BlindDate),4):
	for j in range(i-1,i-5,-1):
		recoverBlind += BlindDate[j]

f = open("BlindDate_recover.jpeg", 'w')
f.write(recoverBlind)
f.close()