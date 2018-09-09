
f = open("drill","r")
drill = f.read()
f.close()

print(drill)

f = open("drill_hex","w")
f.write(drill.decode("hex"))
f.close()
