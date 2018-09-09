





int __fastcall read_privkey(__int64 a1) //sub_101B
{
  int result; // eax@12
  FILE *stream; // [sp+18h] [bp-8h]@1

  _gmpz_init(a1);
  _gmpz_init(a1 + 16);
  _gmpz_init(a1 + 32);
  _gmpz_init(a1 + 48);
  _gmpz_init(a1 + 64);
  stream = fopen("privkey", "r");
  if ( !stream )
  {
    puts("privkey not found. Contact the admins.");
    exit(1);
  }
  fgets(byte_203160, 100, stream);
  fclose(stream);
  if ( _gmpz_set_str(a1, (__int64)byte_203160, 10LL) )
    _assert_fail("err == 0", "official.c", 0x5Au, "init_key");
  if ( _gmpz_set_str(
         a1 + 16,
         (__int64)"128135682856750887590860168748824430714190353609169438003724812869569788088376999153566856518649548751808974042861313871720093923966663967385639616771013994922707548355367088446112595542221209828926608117506259743026809879227606814076195362151108590706375917914576011875357384956337974597411261584032533163073",
         10LL) )
    _assert_fail("err == 0", "official.c", 0x5Cu, "init_key");
  if ( _gmpz_set_str(
         a1 + 32,
         (__int64)"145774370140705743619288815016506936272601276321515267981294709325646228235350799641396853482542510455702593145365689674776551326526283561120782331775753481248764911686023024656237178221049671999816376444280423000085773391715885524862881877222848088840644737895543531766907185051846802894682811137086905085419",
         10LL) )
    _assert_fail("err == 0", "official.c", 0x5Eu, "init_key");
  if ( _gmpz_set_str(a1 + 48, (__int64)"739904609682520586736011252451716180456601329519", 10LL) )
    _assert_fail("err == 0", "official.c", 0x60u, "init_key");
  result = _gmpz_set_str(
             a1 + 64,
             (__int64)"52865703933600072480340150084328845769706702669400766904467248075164948743170867377627486621900744105555465052783047541675343643777082719270261354312243195450389581166294097053506337884439282134405767273312076933070573084676163659758350542617531330447790290695414443063102502247168199735083467132847036144443",
             10LL);
  if ( result )
    _assert_fail("err == 0", "official.c", 0x62u, "init_key");
  return result;
}




__int64 sub_1DEF()
{
  __int64 result; // rax@1
  __int64 v1; // rdx@1
  unRandom_20byteed __int8 v2; // [sp+0h] [bp-20h]@1
  __int64 v3; // [sp+18h] [bp-8h]@1

  v3 = *MK_FP(__FS__, 40LL);
  sub_1D26((__int64)&v2, 0xAu);
  result = v2;
  v1 = *MK_FP(__FS__, 40LL) ^ v3;
  return result;
}

size_t Random_20byte() //sub_1317
{
  FILE *stream; // ST08_8@1

  stream = fopen("/dev/urandom", "rb");
  return fread(&byte_203140, 0x14uLL, 1uLL, stream);
}

__int64 __fastcall sub_14BF(__int64 a1)
{
  int v1; // ST1C_4@1
  char v3; // [sp+20h] [bp-130h]@1
  char v4; // [sp+30h] [bp-120h]@1
  char v5; // [sp+40h] [bp-110h]@1
  char v6; // [sp+C0h] [bp-90h]@1
  __int64 v7; // [sp+148h] [bp-8h]@1

  v7 = *MK_FP(__FS__, 40LL);
  printf("cmd:");
  v1 = sub_1D26((__int64)s1, 0x100u);
  printf("r:", 256LL);
  sub_1D26((__int64)&v5, 0x3Cu);
  printf("s:", 60LL);
  sub_1D26((__int64)&v6, 0x3Cu);
  _gmpz_init((__int64)&v3);
  _gmpz_init((__int64)&v4);
  _gmpz_set_str((__int64)&v3, (__int64)&v5, 10LL);
  _gmpz_set_str((__int64)&v4, (__int64)&v6, 10LL);
  if ( (unRandom_20byteed int)sub_1981(a1, (__int64)s1, v1, (__int64)&v3, (__int64)&v4) )
  {
    if ( !strncmp(s1, "ls", 2uLL) )
    {
      system("ls flag");
    }
    else if ( !strncmp(s1, "du", 2uLL) )
    {
      system("du flag");
    }
    else if ( !strncmp(s1, "stat", 4uLL) )
    {
      system("stat flag");
    }
    else if ( !strncmp(s1, "cat", 3uLL) )
    {
      system("cat flag");
    }
    else
    {
      puts("how did you get that?");
    }
  }
  else
  {
    puts("you are not official");
  }
  return *MK_FP(__FS__, 40LL) ^ v7;
}


__int64 __fastcall Sign_(__int64 a1, __int64 str1, __int64 len) //sub_16CF
{
  __int64 v3; // ST08_8@1
  char v5; // [sp+20h] [bp-30h]@1
  char v6; // [sp+30h] [bp-20h]@1
  __int64 v7; // [sp+48h] [bp-8h]@1

  v3 = len;

  _gmpz_init((__int64)&v5);
  _gmpz_init((__int64)&v6);
  
  sub_1770(a1, (__int64)&v5, (__int64)&v6, str1, v3);
  _gmp_printf("r: %Zd\n", &v5);
  _gmp_printf("s: %Zd\n", &v6);
}

int __fastcall sub_13C2(__int64 a1)
{
  int result; // eax@2
  int len; // [sp+1Ch] [bp-4h]@1

  printf("cmd:");
  len = sub_1D26((__int64)str1, 0x100u);
  if ( !strncmp(str1, "ls", 2uLL) )
  {
    result = Sign_(a1, (__int64)str1, len);
  }
  else if ( !strncmp(str1, "du", 2uLL) )
  {
    result = Sign_(a1, (__int64)str1, len);
  }
  else if ( !strncmp(str1, "stat", 4uLL) )
  {
    result = Sign_(a1, (__int64)str1, len);
  }
  else
  {
    result = puts("nope.");
  }
  return result;
}




void Official_Menu()	//sub_1230
{
  char v0; // al@2
  int v1; // eax@2
  char i; // [sp+1Fh] [bp-1h]@1

  for ( i = 0; i != 69; printf("'%c' is not an official command\n", (unRandom_20byteed int)i) )
  {
    Random_20byte();
    puts("------------------- OFFICIAL MENU -------------------");
    puts("(S) Random_20byte");
    puts("(X) execute");
    puts("(E) exit");
    printf(format);
    v0 = sub_1DEF();
    i = v0;
    v1 = v0 - 69;
    if ( (unRandom_20byteed int)v1 <= 0x33 )
      JUMPOUT(__CS__, (char *)dword_237C + dword_237C[(unRandom_20byteed __int64)(unRandom_20byteed int)v1]);
  }
}


int main()//__int64 sub_F90()
{
  __int64 v0; // ST08_8@1

  setbuf(stdin, 0LL);
  setbuf(stdout, 0LL);
  setbuf(stderr, 0LL);
  v0 = malloc(50);//v0 = (__int64)malloc(0x50uLL);
  read_privkey(v0);
  Official_Menu();
  puts("Offical bye bye.");
  return 0LL;
}