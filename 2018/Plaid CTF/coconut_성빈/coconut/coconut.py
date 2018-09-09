from pwn import *

def connect():
    r = remote('coconut.chal.pwning.xxx',6817)
    return r

r = connect()
print "[+] Connecting\n"

while(True):
    trash = r.recvuntil("Function to optimize:\n")
    print trash
    if trash.find("PCTF")!=-1:
	break
    opcodes = r.recvuntil("<<<EOF>>>")
    print opcodes
    tmpopcodeList = opcodes.split('\n')
    tmpopcodeList=  tmpopcodeList[:-1]
    opcodeList=[]
    for i in tmpopcodeList:  #parsing data
        tmpList = i.split('\t')
        data = []
    
        for j in tmpList:
            if j!='':
                if j.find(", ")!=-1:
                    data.append(j.split(", ")[0])
                    data.append(j.split(", ")[1])
                else:            
                    data.append(j)
        opcodeList.append(data)
    print opcodeList
    trash = r.recvuntil("only be >=")
    start = int(r.recvuntil(" ").strip())
    trash = r.recvuntil("<=")
    end = int(r.recvuntil(":")[:-1])
    
    for i in range(len(opcodeList)):
        if len(opcodeList[i]) == 4:     #only 2 operand operatoers
            opcodeList[i][0] = int(opcodeList[i][0])    #index str to index int
            opcodeList[i][2] = opcodeList[i][2]    #removing opcode splitter ','
    
    eax = '%eax'
    edi = '%edi=='
    deleteOpcodes = []
    print "%d  //  %d"%(start,end)
    for i in range(end-1,start-2,-1):
        if len(opcodeList[i]) == 4:
            print "4 elements -" + str(opcodeList[i][3]==eax) + "-\n"
            if opcodeList[i][3]==eax:
                eax = opcodeList[i][2]
                print(opcodeList[i][2])
            elif opcodeList[i][3]==edi:
                edi = opcodeList[i][2]
            else:
                deleteOpcodes.append(i+1)
        else:
            deleteOpcodes.append(i+1)
    
    ret = ""
    for i in deleteOpcodes:
        ret = ret + str(i) + "\r\n" 
    ret = ret + "#\n"
    print deleteOpcodes
    r.send(ret)
    
    trash = r.recvuntil("Result:")
    print trash
    trash = r.recvline()
    print trash
    trash = r.recv(50)
    print trash


