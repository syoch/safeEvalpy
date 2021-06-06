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
