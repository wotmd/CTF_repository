#include<stdio.h>

void Stage2(int argc, char * argv[])
{
   char s[100] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ ";
   char n[] = "2P'8u^]:'\\@TSt:g?};!n?FK";


   int c=0,cc,pc=c,m;
   int i,j=0;

   for(i=0; n[i]!='\0'; i++)
   {
      c += j;
      for(j=0; n[i]!=s[j];j++);
      m = j-c;
//      printf("\nj-c : %d\n",m);
      //if(m < 0) printf("%c",s[(j-c)+95]);
      while( m < 0 ) m+=95;
      printf("%c",s[m]);
   }

   printf("\n");
}
