from socket import *

s = socket(2,1)
s.connect(('catwestern_631d7907670909fc4df2defc13f2057c.quals.shallweplayaga.me',9999))
reg = s.recv(2048)

print reg
reg = reg.split('\n')[1:]
for i in reg:
	exec i

a = s.recv(2048)
print a
a = a.split('\n')
a = '\n'.join(a[2:])
print 'LENGTH:', len(a)

regs = [rax,rbx,rcx,rdx,rsi,rdi,r8,r9,r10,r11,r12,r13,r14,r15]
for n,i in enumerate(regs):
	if i>0x7fffffffffffffff:
		regs[n] = -(0xffffffffffffffff-i+1)
cmd=('./catwestern %d ' +'%x '*14+ '%s')%(len(a),
	regs[0],regs[1],regs[2],regs[3],regs[4],
	regs[5],regs[6],regs[7],regs[8],regs[9],
	regs[10],regs[11],regs[12],regs[13],a.encode('hex'))

import subprocess
print cmd
t = subprocess.check_output(cmd, shell=True)
#print 'Output: %s\nLength: %d'% (t,len(t))

for i in t.split('\n'):
	exec i

ans = '''rax=0x%x
rbx=0x%x
rcx=0x%x
rdx=0x%x
rsi=0x%x
rdi=0x%x
r8=0x%x
r9=0x%x
r10=0x%x
r11=0x%x
r12=0x%x
r13=0x%x
r14=0x%x
r15=0x%x
''' % (rax,rbx,rcx,rdx,rsi,rdi,r8,r9,r10,r11,r12,r13,r14,r15)
print ans
s.send(ans)
print s.recv(2048)
