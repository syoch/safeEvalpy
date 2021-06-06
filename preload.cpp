#include <stdio.h>
#include <dlfcn.h>
#include <string.h>
#include <unistd.h>

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

extern "C" int fork()
{
  auto org = (int (*)())(dlsym(RTLD_NEXT, "fork"));

  if (fork_enabled)
  {
    return ((int (*)())dlsym(RTLD_NEXT, "fork"))();
  }
  else
  {
    auto fp = fopen("safeEvalPy.log", "a+");
    fprintf(fp, "syscall::fork() is blocked\n");
    fclose(fp);
    return 0;
  }
}
extern "C" pid_t forkpty(int *amaster, char *name,
                         const struct termios *termp,
                         const struct winsize *winp)
{
  if (fork_enabled)
  {
    auto org = (pid_t(*)(int *, char *, const struct termios *, const struct winsize *))(dlsym((void *)(-1), "forkpty"));
    return org(amaster, name, termp, winp);
  }
  else
  {
    auto fp = fopen("safeEvalPy.log", "a+");
    fprintf(fp, "syscall::forkpty() is blocked\n");
    fclose(fp);
    return 0;
  }
}