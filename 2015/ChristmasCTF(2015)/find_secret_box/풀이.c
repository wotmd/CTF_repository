#include <stdio.h>

int main()
{
	int s[4];
	int result[8][4];
	char gate[9]="HESBRAYT";
	int i,j;
	int a,b,c,d;

	scanf("%d %d %d %d", &s[0], &s[1], &s[2], &s[3]);

	for(s[0]=0; s[0]<2; s[0]++){
		for(s[1]=0; s[1]<2; s[1]++){
			for(s[2]=0; s[2]<2; s[2]++){
				for(s[3]=0; s[3]<2; s[3]++){


	printf("%d%d%d%d : ",s[0],s[1],s[2],s[3]);

	//A스위치의 역할
	for(i=0; i<8; i++){
		result[i][0]=s[0];
	}

	//B스위치의 역할
	for(i=0; i<4; i++){
		result[i][1]=s[1];
	}
	for(i=4; i<8; i++){
		result[i][1]=!s[1];
	}

	//C스위치의 역할
	for(i=0; i<8; i++){
		if(i==0 || i==1 || i==4 || i==5)
			result[i][2]=s[2];
		if(i==2 || i==3 || i==6 || i==7)
			result[i][2]=!s[2];
	}

	//D스위치의 역할
	for(i=0; i<8; i++){
		if(i==0 || i==2 || i==4 || i==6)
			result[i][3]=s[3];
		if(i==1 || i==3 || i==5 || i==7)
			result[i][3]=!s[3];
	}

	for(i=0; i<8; i++)
	{
		if((result[i][0]+result[i][1]+result[i][2]+result[i][3])==4)
			printf("%c",gate[i]);
	}
	printf("\n");



				}
			}
		}
	}



}