#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
	void (*f)();
	register unsigned long long rax asm("rax");
	register unsigned long long rbx asm("rbx");
	register unsigned long long rcx asm("rcx");
	register unsigned long long rdx asm("rdx");
	register unsigned long long rsi asm("rsi");
	register unsigned long long rdi asm("rdi");
	register unsigned long long r8 asm("r8");
	register unsigned long long r9 asm("r9");
	register unsigned long long r10 asm("r10");
	register unsigned long long r11 asm("r11");
	register unsigned long long r12 asm("r12");
	register unsigned long long r13 asm("r13");
	register unsigned long long r14 asm("r14");
	register unsigned long long r15 asm("r15");

	unsigned long long _rax=0,_rbx=0,_rcx=0,_rdx=0,_rsi=0,_rdi=0,_r8=0,_r9=0,_r10=0,_r11=0,_r12=0,_r13=0,_r14=0,_r15=0;
	unsigned char code[1024]={0,};
	unsigned char tmp[3]={0,};
	int tmp2=0;

	if(argc<17) { printf("nope\n"); return 0; }

	int i;
	for(i=0; i<atoi(argv[1]); i++) {
		memcpy(tmp, argv[16]+i*2, 2);
		tmp2=strtol(tmp, &tmp, 16);
		code[i]=tmp2;
	}
	_rax =strtoll(argv[2], 0, 16);
	_rbx =strtoll(argv[3], 0, 16);
	_rcx =strtoll(argv[4], 0, 16);
	_rdx =strtoll(argv[5], 0, 16);
	_rsi =strtoll(argv[6], 0, 16);
	_rdi =strtoll(argv[7], 0, 16);
	_r8  =strtoll(argv[8], 0, 16);
	_r9  =strtoll(argv[9], 0, 16);
	_r10=strtoll(argv[10], 0, 16);
	_r11=strtoll(argv[11], 0, 16);
	_r12=strtoll(argv[12], 0, 16);
	_r13=strtoll(argv[13], 0, 16);
	_r14=strtoll(argv[14], 0, 16);
	_r15=strtoll(argv[15], 0, 16);

/*
	printf("rax=0x%llx\n", _rax);
	printf("rbx=0x%llx\n", _rbx);
	printf("rcx=0x%llx\n", _rcx);
	printf("rdx=0x%llx\n", _rdx);
	printf("rsi=0x%llx\n", _rsi);
	printf("rdi=0x%llx\n", _rdi);
	printf("r8=0x%llx\n",  _r8);
	printf("r9=0x%llx\n",  _r9);
	printf("r10=0x%llx\n", _r10);
	printf("r11=0x%llx\n", _r11);
	printf("r12=0x%llx\n", _r12);
	printf("r13=0x%llx\n", _r13);
	printf("r14=0x%llx\n", _r14);
	printf("r15=0x%llx\n", _r15);
	printf("****************************\n");
*/
	f=(void *)code;
	rax=_rax;rbx=_rbx;rcx=_rcx;rdx=_rdx;
	rsi=_rsi;rdi=_rdi;r8=_r8;r9=_r9;
	r10=_r10;r11=_r11;r12=_r12;r13=_r13;
	r14=_r14;r15=_r15;
	/*
	printf("rax=%llx\n", rax);
	printf("rbx=%llx\n", rbx);
	printf("rcx=%llx\n", rcx);
	printf("rdx=%llx\n", rdx);
	printf("rsi=%llx\n", rsi);
	printf("rdi=%llx\n", rdi);
	printf("r8=%llx\n",  r8);
	printf("r9=%llx\n",  r9);
	printf("r10=%llx\n", r10);
	printf("r11=%llx\n", r11);
	printf("r12=%llx\n", r12);
	printf("r13=%llx\n", r13);
	printf("r14=%llx\n", r14);
	printf("r15=%llx\n", r15);
	printf("***************************************\n");
*/
//	printf("executing...\n");
//	f();
	asm volatile(
		"call -0xb8(%rbp)\n\t"
	);
	_rax=rax;_rbx=rbx;_rcx=rcx;_rdx=rdx;
	_rsi=rsi;_rdi=rdi;_r8=r8;_r9=r9;
	_r10=r10;_r11=r11;_r12=r12;_r13=r13;
	_r14=r14;_r15=r15;
//	printf("executed!\n");
	printf("rax=0x%llx\n", _rax);
	printf("rbx=0x%llx\n", _rbx);
	printf("rcx=0x%llx\n", _rcx);
	printf("rdx=0x%llx\n", _rdx);
	printf("rsi=0x%llx\n", _rsi);
	printf("rdi=0x%llx\n", _rdi);
	printf("r8=0x%llx\n",  _r8);
	printf("r9=0x%llx\n",  _r9);
	printf("r10=0x%llx\n", _r10);
	printf("r11=0x%llx\n", _r11);
	printf("r12=0x%llx\n", _r12);
	printf("r13=0x%llx\n", _r13);
	printf("r14=0x%llx\n", _r14);
	printf("r15=0x%llx", _r15);
	return 0;
}
