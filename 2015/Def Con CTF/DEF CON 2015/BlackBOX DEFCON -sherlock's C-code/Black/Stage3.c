#include <stdio.h>
#include <string.h>

void Stage3()
{
   char str[]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ ";
   char restr[95];
   int i,j;
   int alen,n,blen,len;
   int ar[63],br[63];

   char a[]="?`~~;",b[]="tt}}I;!z_=DC)z?|]\\)zKL";

   len=strlen(str);
   alen=strlen(a);
   blen=strlen(b);
   j=0;
   for(i=len-1; i>=0; i--)
      restr[j++]=str[i];

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




   for(n=1; n<95; n++)
   {
      printf("%d Password : ", n);
      for(i=alen-1; i>=0; i--)
      {
         printf("%c", str[(ar[i]+n)%95]);
      }
      printf("\n");
      for(i=blen-1; i>=0; i--)
      {
         printf("%c", str[(br[i]+n)%95]);
      }
      
      printf("\n\n");
   }
   printf("\n");
}