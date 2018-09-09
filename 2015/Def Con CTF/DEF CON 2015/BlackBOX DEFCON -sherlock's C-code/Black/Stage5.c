#include <stdio.h>
#include <string.h>

void Stage5()
{
   char str[]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ ";
   int i,j,len,clen, swi=0;
   int cr[63];

   char c[]="l-Tn/o,fXzpd3DZXbEHLWF";
   int ci[63]={0};
   int pl[63],repl[63];

   len=strlen(str);
   clen=strlen(c);
   j=0;
   
   for(i=0; i<clen; i++)
      for(j=0; j<95; j++)
         if(c[i]==str[j])
            cr[i]=j;


   for(i=0; i<clen-1; i++)
   {
	   ci[i]=2*cr[i]-cr[i+1];
	   if(ci[i]<0)
		   ci[i]+=95;
	   else if(ci[i]>95)
		   ci[i]%=95;
   }
   

   pl[0]=0;

   for(i=0; i<clen-1; i++)
	   pl[i+1]=((pl[i]+ci[i])+95)%95;
   j=0;
   for(i=clen-1; i>=0; i--)
	   repl[i]=pl[j++];

   for(i=0; i<clen; i++)
	   pl[i]=95-repl[i];

   printf("Answer : \n");
   for(j=0; j<95; j++)
   {
	   for(i=0; i<clen; i++)
		   if(str[(pl[i]+j)%95]==' ')
			   swi=1;

	   if(swi==1)
	   {
		   for(i=0; i<clen; i++)
			   printf("%c", str[(pl[i]+j)%95]);
		   printf("\n");
	   }
	   swi=0;
   }
}   