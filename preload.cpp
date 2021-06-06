#include <stdio.h>
#include <dlfcn.h>
#include <string.h>

// global variables
bool fork_enabled = true;

// overrides

// (controller) py=>open() C=>? C++=>?
extern "C" int open64(const char *pathname, int flags, unsigned int mode)
{
  auto org = (int (*)(const char *, int, unsigned int))(dlsym((void *)(-1), "open64"));
  if (!strcmp(pathname, "%fb"))
  {
    fork_enabled = false;
    return org("/dev/null", flags, mode);
  }
  else if (!strcmp(pathname, "%fnb"))
  {
    fork_enabled = true;
    return org("/dev/null", flags, mode);
  }
  return org(pathname, flags, mode);
}

long prev = 0;
extern "C" int fork()
{
  auto org = (int (*)())(dlsym(RTLD_NEXT, "fork"));
  auto clock = (long (*)())(dlsym(RTLD_NEXT, "clock"));

  if (prev == 0)
    prev = clock();

  if (fork_enabled)
  {
    return ((int (*)())dlsym(RTLD_NEXT, "fork"))();
  }
  else
  {
    fprintf(stdout, "syscall::fork() is blocked %ld \n", clock() - prev);
    return 0;
  }

  prev = clock();
  return 0;
}