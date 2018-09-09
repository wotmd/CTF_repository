dic = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "

def Stage1(password,expected,original):
	password_len = len(password)
	expected_len = len(expected)
	ar = [0]*15
	br = [0]*23

	for i in range(0,password_len):
		for j in range(0,95):
			if(password[i] == dic[j]):
				ar[i] = j

	for i in range(0,expected_len):
		for j in range(0,95):
			if(expected[i] == dic[j]):
				br[i] = j
	pw = ['']*95
	ex = ['']*95

	for n in range(0,95):
		for i in range(0,password_len):
			pw[n] += dic[ (ar[i]+n) % 95 ]
		for j in range(0,expected_len):
			ex[n] += dic[ (br[j]+n) % 95 ]

	for i in range(0,95):
		if(pw[i] == original):
			print "##### ANSWER1 ######"
			print "password : " + pw[i] + "    expected : " + ex[i]
			break



def Stage2(expected):
	expected_len = len(expected)
	result = ''
	tmp = 0
	index = 0
	tmp_index = 0

	for i in range(0, expected_len):
		index += j
		for j in range(0, len(dic)):
			if(expected[i] == dic[j]):
				break
			tmp_index = j-index
			while tmp_index < 0:
				tmp_index += 95
		print dic[tmp_index]

#	print "##### ANSWER2 ######"			

#def Stage3(password,expected,original):
	

def escape_change(raw):
	for i in range(len(raw)):
		if(raw[i] == '\''):
			raw = raw.replace('\'','\\\'')
		elif(raw[i] == '\"'):
			raw = raw.replace('\"','\\\"')
		elif(raw[i] == '\\'):
                        raw = raw.replace('\\','\\\\')
	return raw





print "Stage 1"

print "raw_password, raw_expected, original"
raw_password, raw_expected, original = raw_input(), raw_input(), raw_input()

#print raw_password
#print raw_expected
Stage1(raw_password,raw_expected,original)


print "Stage 2"

print "raw_expected"
raw_expected = raw_input()

Stage2(raw_expected)

print "Stage 3"

raw_password, raw_expected, original = raw_input(), raw_input(), raw_input()

raw_password = escape_change(raw_password)
raw_expected = escape_change(raw_expected)

Stage3(raw_expected)











