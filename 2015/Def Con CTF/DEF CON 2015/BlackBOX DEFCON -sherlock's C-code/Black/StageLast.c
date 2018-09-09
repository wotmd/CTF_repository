#include <stdio.h>
#include <string.h>

void StageLast()
{
   char str[]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ ";
   int i,j,len,clen,swi=1;
   int cr[63];

   char c[]="uMOW9ic6Y[M[q}:gf4h~[xQnjMfO*Nv%tJLh+9Kpn6tWAB";
   int ci[70]={0};
   int pl[63];

   len=strlen(str);
   clen=strlen(c);
   j=0;
   for(i=0; i<70; i++)
	   ci[i]=0;
   
   for(i=0; i<clen; i++)
      for(j=0; j<95; j++)
         if(c[i]==str[j])
            cr[i]=j;

   for(i=0; i<clen-1; i+=4)
   {
	   ci[i]=cr[i+1]-((2*cr[i])%95)-1;
	   ci[i+1]=cr[i+3]-((2*cr[i+1])%95)-1;
	   ci[i+2]=cr[i+2]-((2*cr[i+3])%95)-1;
	   ci[i+3]=cr[i+4]-((2*cr[i+2])%95)-1;	   
   }

   pl[0]=0;

   for(i=0; i<clen-1; i++)
   {
	   pl[i+1]=((pl[i]+ci[i])+95)%95;
   }

   printf("Answer : \n");
   for(j=0; j<95; j++)
   {
	   for(i=0; i<clen; i++)
		   if(str[(pl[i]+j)%95]==' ')
			   swi=1;

	   if(swi==1 && str[pl[0]+j]=='T')
	   {
		   for(i=0; i<clen; i++)
			   printf("%c", str[(pl[i]+j)%95]);
		   printf("\n");
	   }
	   swi=0;
   }
}