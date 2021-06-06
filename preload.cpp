#include <stdio.h>
#include <dlfcn.h>
long prev = 0;
extern "C" int fork()
{
  auto org = (int (*)())(dlsym(RTLD_NEXT, "fork"));
  auto clock = (long (*)())(dlsym(RTLD_NEXT, "clock"));

  if (prev == 0)
    prev = clock();

  // ((int (*)())dlsym(RTLD_NEXT, "fork"))();

  fprintf(stdout, "fork is blocked(by preload) %ld \n", clock() - prev);

  prev = clock();
  return 0;
}