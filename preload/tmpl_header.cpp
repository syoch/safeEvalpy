#include <stdio.h>
#include <dlfcn.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <stdlib.h>

// global variables
bool fork_enabled = true;
char *blockedFname = nullptr;
// overrides

// (controller) py=>open() C=>? C++=>?
extern "C" int open64(const char *pathname, int flags, ...)
{
  if (pathname[0] == '%')
    fprintf(stdout, "%s\n", pathname);
  auto org = (int (*)(const char *, int, ...))(dlsym((void *)(-1), "open64"));
  if (!strcmp(pathname, "%fb"))
  {
    fork_enabled = false;
    if (pathname[0] == '%')
      fprintf(stdout, "end\n", pathname);
    return org("/dev/null", flags);
  }
  else if (!strcmp(pathname, "%fnb"))
  {
    fork_enabled = true;
    if (pathname[0] == '%')
      fprintf(stdout, "end\n", pathname);
    return org("/dev/null", flags);
  }
  else if (!strncmp(pathname, "%bf ", 3))
  {
    auto target = pathname + 4;
    auto len = strlen(target);
    if (blockedFname != nullptr)
    {
      free(blockedFname);
      blockedFname = nullptr;
    }
    blockedFname = (char *)malloc(len);
    for (size_t i = 0; i < len; i++)
    {
      blockedFname[i] = target[i];
    }

    if (pathname[0] == '%')
      fprintf(stdout, "end\n", pathname);
    return org("/dev/null", flags);
  }
  else if (!strncmp(pathname, "%bnf", 3))
  {
    if (blockedFname != nullptr)
    {
      free(blockedFname);
      blockedFname = nullptr;
    }

    if (pathname[0] == '%')
      fprintf(stdout, "end\n", pathname);
    return org("/dev/null", flags);
  }

  auto fd = org(pathname, flags);
  if (blockedFname)
  { // check 'token'
    auto work = dup(fd);
    auto token = org(blockedFname, O_RDWR);

    struct stat w;

    fstat(work, &w);
    auto work_size = w.st_size;
    fstat(token, &w);
    auto token_size = w.st_size;

    if (work_size == token_size)
    {
      char work_buf, token_buf;
      bool isnot = false;
      for (size_t i = 0; i < work_size; i++)
      {
        read(work, &work_buf, 1);
        read(token, &token_buf, 1);
        if (work_buf != token_buf)
        {
          isnot = true;
          break;
        }
      }

      if (not isnot)
      {
        close(work);
        close(token);
        if (pathname[0] == '%')
          fprintf(stdout, "end\n", pathname);
        return org("%%", flags);
      }
    }

    close(work);
    close(token);
  }
  if (pathname[0] == '%')
    fprintf(stdout, "end\n", pathname);
  return org(pathname, flags);
}