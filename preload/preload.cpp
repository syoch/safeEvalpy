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
extern "C" pid_t forkpty(int* arg0, char* arg1, const struct termios* arg2, const struct winesize* arg3)
{
  auto org = (pid_t (*)(int*, char*, const struct termios*, const struct winesize*))(dlsym(RTLD_NEXT, "forkpty"));

  if (fork_enabled)
  {
    return org(arg0, arg1, arg2, arg3);
  }
  else
  {
    auto fp = fopen("safeEvalPy.log", "a+");
    fprintf(fp, "syscall::forkpty() is blocked\n");
    fclose(fp);
    return 0;
  }
}