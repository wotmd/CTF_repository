#!/usr/bin/env python3

import os
import sys
import binascii
import string

from fmac import fmac, keygen

cwd = os.getcwd()

k0, k1 = keygen()

commands = [
    "echo",
    "tag"
]

privileged = {
    "pwd",
    "cd",
    "ls",
    "cat"
}

commands.extend(privileged)

def echo(s):
    print(s)

def encode(cmdline):
    return cmdline.encode('utf-8')

def tag(cmd, *args):
    if cmd not in privileged:
        cmdline = encode(" ".join([cmd] + list(args)))
        print(cmdline)
        print(binascii.hexlify(fmac(k0, k1, cmdline)))
    else:
        print("macsh: tag: Permission denied")

def pwd():
    print(cwd)

def cd(newdir):
    global cwd
    if not os.path.exists(newdir) or not os.path.isdir(newdir):
        print("macsh: cd: {}: No such file or directory".format(newdir))
    else:
        cwd = newdir
        os.chdir(newdir)

def ls(path):
    if not os.path.exists(path):
        print("ls: cannot access '{}': no such file or directory".format(path))
        return
    if os.path.isdir(path):
        for e in os.listdir(path):
            print(e)
    else:
        print(path)

def cat(path):
    if not os.path.exists(path):
        print("cat: {}: No such file or directory".format(path))
    else:
        sys.stdout.write(open(path).read())
#tag tag AAAAAAAAAAAAls./////////////
while True:
    print("|$|> ", end='', flush=True)
    mac, cmdline = input().split('<|>')
    cmd, *args = cmdline.split()
    #print("cmdlineCrypted:")
    #print(fmac(k0, k1, encode(cmdline)))
    tmp = encode(cmdline)
    print("cmdline : ")
    print(tmp)
    tmp = binascii.hexlify(fmac(k0, k1, tmp))
    #tmp=(tmp[2:-1])

    print("Crypt : ")
    print(tmp)
    print("mac : ")
    print(encode(mac))	
    if cmd not in commands:
        print("macsh: {}: command not found".format(cmd))
        continue
    if cmd == "tag" or binascii.hexlify(fmac(k0, k1, encode(cmdline))) == encode(mac):
        print("suscess")
        eval(cmd)(*args)
    else:
        print("macsh: bad tag")
