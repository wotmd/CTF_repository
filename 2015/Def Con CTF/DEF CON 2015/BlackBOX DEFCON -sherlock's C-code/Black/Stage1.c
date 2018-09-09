#include <stdio.h>
#include <string.h>

void Stage1()
{
   char str[]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ ";
   int i,j,alen,n,blen;
   int ar[15],br[23];

   char a[]="CRRNG",b[]="tujc),WTXGF),NQUG){JGOGU";

   alen=strlen(a);
   blen=strlen(b);

   for(i=0; i<alen; i++)
   {
      for(j=0; j<96; j++)
         if(a[i]==str[j])
            ar[i]=j;
   }

   for(i=0; i<blen; i++)
   {
      for(j=0; j<96; j++)
         if(b[i]==str[j])
            br[i]=j;
   }




   for(n=1; n<96; n++)
   {
      printf("%d Password : ", n);
      for(i=0; i<alen; i++)
      {
         printf("%c", str[(ar[i]+n)%95]);
      }
      printf("    ");
      for(i=0; i<blen; i++)
      {
         printf("%c", str[(br[i]+n)%95]);
      }
      
      printf("\n");
   }
   printf("\n");

}   