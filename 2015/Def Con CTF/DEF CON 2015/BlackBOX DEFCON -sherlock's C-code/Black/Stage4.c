#include <stdio.h>
#include <string.h>

void Stage4()
{
   char str[]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ ";
   int i,j,temp;
   int alen,n,blen,len;
   int ar[63],br[63];
   int x,y,h;

   char a[]="A)tU",b[]="{bHQ^I#l/0zs&1qj`/E";
   int c[63]={0};


   len=strlen(str);
   alen=strlen(a);
   blen=strlen(b);
   j=0;
   
   /*
   for(i=0; i<95; i++)
	   if('9'==str[i])
		   printf("%d\n", i);	   
		   */

   for(i=0; i<alen; i++)
   {
      for(j=0; j<95; j++)
         if(a[i]==str[j])
            ar[i]=j;
   }

   for(i=0; i<blen; i++)
   {
      for(j=0; j<95; j++)
         if(b[i]==str[j])
            br[i]=j;
   }
   printf("0 \n");
   for(i=0; i<95; i++)
   {
	   if(str[ar[1]]==str[i])
	   {
		   printf("%d\n", (95+(i-1))%95);
		   c[1]=(95+(i-1))%95;
		   temp=(95+(i-2))%95;
	   }
   }
   for(i=0; i<95; i++)
	   if(str[ar[2]]==str[i])
		   printf("%d\n", (95+(i-2))%95),c[2]=(95+(i-2))%95;



   for(i=0; i<95; i++)
	   if(str[ar[3]]==str[i])
		   printf("%d\n", (95+(i-3))%95),c[3]=(95+(i-3))%95;
   printf("\n");

  if((95+c[1]-c[0])%95==(95+c[2]-c[1])%95 && (95+c[2]-c[1])%95>0)
  {
	  n=2;
	  x=(95+c[1]-c[0])%95;
  }
  else if((95+c[1]-c[0])%95==(95+c[2]-c[1])%95 && (95+c[2]-c[1])%95<0)
  {
	  n=3;
	  x=(95+c[1]-c[0])%95;
  }
  else
  {
	  n=1;
  }

   if(n==1)
   {
	   scanf("%d %d", &x, &h);
	   j=0;
	   printf("Password : ");
	   for(i=0; i<alen; i++)
	   {
		   if(i%2==0)
			   printf("%c", str[(95+ar[i]-x*(j++))%95]); 
		   else
			   printf("%c", str[(95+ar[i]-(temp-h+x*j))%95]);
	   }
	   printf("\n");
	   j=0;
	   for(i=0; i<blen; i++)
	   {
		   if(i%2==0)
			   printf("%c", str[(95+br[i]-x*(j++))%95]);
		   else
			   printf("%c", str[(95+br[i]-(temp-h+x*j))%95]);
	   }
	   printf("\n\n");
   }
   else if(n==2)
   {
	   //scanf("%d", &x);
	   j=0;
	   printf("Password : ");
	   for(i=0; i<alen; i++)
	   {
		   printf("%c", str[(95+ar[i]-(x*(j++)%95))%95]);
	   }
	   printf("\n");
	   j=0;
	   for(i=0; i<blen; i++)
	   {
		   printf("%c", str[(95+br[i]-(x*(j++)%95))%95]);
	   }
	   printf("\n\n");
   }
   else if(n==3)
   {
	   //scanf("%d", &x);
	   j=0;
	   printf("Password : ");
	   for(i=0; i<alen; i++)
	   {
		   printf("%c", str[(95+ar[i]-(95+x*j++))%95]);
	   }
	   printf("\n");
	   j=0;
	   for(i=0; i<blen; i++)
	   {
		   printf("%c", str[(95+br[i]-(95+x*j++))%95]);
	   }
	   printf("\n\n");
   }
   
}