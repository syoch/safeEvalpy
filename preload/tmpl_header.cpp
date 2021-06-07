#include <stdio.h>
#include <dlfcn.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

// global variables
bool fork_enabled = true;

// overrides

// (controller) py=>open() C=>? C++=>?
extern "C" int open64(const char *pathname, int flags, ...)
{
  auto org = (int (*)(const char *, int, ...))(dlsym((void *)(-1), "open64"));
  if (!strcmp(pathname, "%fb"))
  {
    fork_enabled = false;
    return org("/dev/null", flags);
  }
  else if (!strcmp(pathname, "%fnb"))
  {
    fork_enabled = true;
    return org("/dev/null", flags);
  }
  else if (!strncmp(pathname, "%bf ", 3))
  {
    fprintf(stdout, "registered");
    fork_enabled = true;
    return org("/dev/null", flags);
  }

  auto fd = org(pathname, flags);
  { // check 'token'
    auto work = dup(fd);
    auto token =

        close(work);
  }
  return org(pathname, flags);
}