#include <dirent.h>
#include <dlfcn.h>
#include <fcntl.h>
#include <spawn.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

// global variables
bool fork_enabled = true;
char *blockedFname = nullptr;
// overrides

// (controller) py=>open() C=>? C++=>?
extern "C" void writelog(const char *fmt, ...) {
  va_list ap;
  va_start(ap, fmt);

  char buf[1024];
  vsnprintf(buf, 1024, fmt, ap);

  auto fp = fopen("safeEvalPy.log", "a+");
  fprintf(fp, "%s", buf);
  fclose(fp);

  va_end(ap);
}
extern "C" bool processcmd(const char *cmd) {
  if (!strcmp(cmd, "%fb")) {
    fork_enabled = false;
  } else if (!strcmp(cmd, "%fnb")) {
    fork_enabled = true;
  } else if (!strncmp(cmd, "%bf ", 3)) {
    auto target = cmd + 4;
    auto len = strlen(target);
    if (blockedFname != nullptr) {
      free(blockedFname);
      blockedFname = nullptr;
    }
    blockedFname = (char *)malloc(len);
    for (size_t i = 0; i < len; i++) {
      blockedFname[i] = target[i];
    }
  } else if (!strncmp(cmd, "%bnf", 3)) {
    if (blockedFname != nullptr) {
      free(blockedFname);
      blockedFname = nullptr;
    }
  } else if (!strncmp(cmd, "%dbg", 3)) {
    fprintf(stderr, "%s\n", cmd + 5);
  } else {
    return false;
  }
  return true;
}
extern "C" int open64(const char *pathname, int flags, ...) {
  // code by :
  // https://code.woboq.org/userspace/glibc/sysdeps/unix/sysv/linux/open64.c.html#36
  int mode = 0;
  if (__OPEN_NEEDS_MODE(flags)) {
    va_list arg;
    va_start(arg, flags);
    mode = va_arg(arg, int);
    va_end(arg);
  }
  // end code (copy) thanks!

  auto org =
      (int (*)(const char *, int, mode_t))(dlsym((void *)(-1), "open64"));
  if (processcmd(pathname)) {
    return org("/dev/null", O_RDONLY, 0);
  }

  if (fork_enabled) {
    return org(pathname, flags, mode);
  }

  if (blockedFname) {  // check 'token'
    auto work = org(pathname, flags, mode);
    auto token = org(blockedFname, O_RDWR, 0);

    struct stat w;

    fstat(work, &w);
    auto work_size = w.st_size;
    fstat(token, &w);
    auto token_size = w.st_size;

    if (work_size == token_size) {
      char work_buf, token_buf;
      bool isnot = false;
      for (size_t i = 0; i < work_size; i++) {
        read(work, &work_buf, 1);
        read(token, &token_buf, 1);
        if (work_buf != token_buf) {
          isnot = true;
          break;
        }
      }

      if (not isnot) {
        close(work);
        close(token);
        writelog("opening blocked file detected");
        return org("/dev/null", O_RDWR, 0);
      }
    }

    close(work);
    close(token);
  }
  if ((strstr(pathname, "..") != NULL or pathname[0] == '/') and
      strncmp(pathname, "/usr/lib/python", 15)) {
    writelog("directory traversal was detected\n");
    return org("/dev/null", O_RDWR, 0);
  }
  if (flags & O_CREAT) {
    writelog("creating file was detected\n");
    return org("/dev/null", O_RDWR, 0);
  }
  return org(pathname, flags, mode);
}