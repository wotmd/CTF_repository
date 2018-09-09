
f = open("basic_crypto","r")
basic_crypto = f.read()
f.close()

basic_decrypt=""
for i in basic_crypto:
	basic_decrypt += chr(ord(i)^0xFF)

f = open("decrypt_png.png","w")
f.write(basic_decrypt)
f.close()
