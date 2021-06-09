#include <stdio.h>
#include <dlfcn.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <stdarg.h>

// global variables
bool fork_enabled = true;
char *blockedFname = nullptr;
// overrides

// (controller) py=>open() C=>? C++=>?
extern "C" int open64(const char *pathname, int flags, ...)
{
  // code by : https://code.woboq.org/userspace/glibc/sysdeps/unix/sysv/linux/open64.c.html#36
  int mode = 0;
  if (__OPEN_NEEDS_MODE(flags))
  {
    va_list arg;
    va_start(arg, flags);
    mode = va_arg(arg, int);
    va_end(arg);
  }
  // end code (copy) thanks!
  fprintf(stdout, "> %d | %s %#4x %#4x\n", fork_enabled, pathname, flags, mode);
  auto org = (int (*)(const char *, int, mode_t))(dlsym((void *)(-1), "open64"));
  if (!strcmp(pathname, "%fb"))
  {
    fork_enabled = false;
    return org("/dev/null", O_RDWR, 0);
  }
  else if (!strcmp(pathname, "%fnb"))
  {
    fork_enabled = true;
    return org("/dev/null", O_RDWR, 0);
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

    return org("/dev/null", O_RDWR, 0);
  }
  else if (!strncmp(pathname, "%bnf", 3))
  {
    if (blockedFname != nullptr)
    {
      free(blockedFname);
      blockedFname = nullptr;
    }

    return org("/dev/null", O_RDWR, 0);
  }

  if (fork_enabled)
  {
    return org(pathname, flags, mode);
  }

  if (blockedFname)
  { // check 'token'
    auto work = org(pathname, flags, mode);
    auto token = org(blockedFname, O_RDWR, 0);

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
        return org("%%", flags, mode);
      }
    }

    close(work);
    close(token);
  }
  if ((strstr(pathname, "..") != NULL or pathname[0] == '/'))
  {
    auto fp = fopen("safeEvalPy.log", "a+");
    fprintf(fp, "directory traversal was detected\n");
    fclose(fp);
    return org("/dev/null", O_RDWR, 0);
  }
  if (flags & O_CREAT)
  {
    auto fp = fopen("safeEvalPy.log", "a+");
    fprintf(fp, "make file was detected\n");
    fclose(fp);
    return org("/dev/null", O_RDWR, 0);
  }
  return org(pathname, flags, mode);
}