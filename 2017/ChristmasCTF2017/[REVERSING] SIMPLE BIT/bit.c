#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int sub(int* num1, int num2)
{
	int* result;
	int i;
	int random_num;
	
	result = (int*)malloc(num2);
	
	for(i=num2-1; i>=0; i--)
	{
		random_num=rand()%num2;
		//result=i;
		if(i!=random_num)
		{
			*(4 * i + num1) ^= *(4 * random_num + num1);
			*(4 * random_num + num1) ^= *(4 * i + num1);
			result = 4 * i + num1;
			*result ^= *(4 * random_num + num1);
		}
	}
	
	return 0;
}

int main()
{
	char s[2000];
	int what[2048]={0,};
	int thiswhat[2048]={0,};
	int result=0;
	int len;
	int tmp=0;
	int i,j,k;
	
	printf("input : ");
	scanf("%s",s);
	
	len = strlen(s);
	for ( i = 0; i < len; ++i )
	{
		for ( j = 8 * i; j < 8 * (i + 1); ++j )
		{
			what[j] = s[i] & 1;
			s[i] >>= 1;
		}
	}
	for(i=0; i<2048; i++)
		printf("%d",what[i]);
	printf("\n\n");
	for ( i = 0; i < 16; ++i )
	{
		tmp = 1;
		for ( j = 0; j < 8 * len; ++j )
		{
			if ( what[j] )
				tmp ^= 0x1;
			what[j] = tmp;
		}
		sub(what, 8 * len);
	}
	for(i=0; i<2048; i++)
		printf("%d",what[i]);
	for ( i = 0; i < 2048; i++ )
	{
		if ( what[i] != thiswhat[i] )
		{
			result = 0;
			printf("Wrong\n");
			//v6 = *MK_FP(__FS__, 40) ^ v146;
			return result;
		}
	}
	
	result = 1;
	printf("Collect\n");
	return result;
}