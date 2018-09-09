dic = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "


raw_expected="/j'@{JHWx6p`F}6n|DJy";


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
	j=0
	for i in range(0, expected_len):
		index += j
		for j in range(0, len(dic)):
			if(expected[i] == dic[j]):
				break
		tmp_index = j-index
		while tmp_index < 0:
			tmp_index += 95
		print dic[tmp_index]

Stage1("n22yr","]]'+MYn70puMYn9s7yMO7t","apple")
Stage2(raw_expected)