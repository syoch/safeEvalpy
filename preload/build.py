#!/bin/python3
import os
os.chdir(os.path.dirname(__file__))

fp = open("preload.cpp", "w")
with open("tmpl_header.cpp", "r") as header:
    fp.write(header.read())
for name, ret_type, *args_type in [
    ["forkpty", "pid_t",
     "int*", "char*", "const struct termios*", "const struct winesize*"],

    ["fork", "int"],

    ["rmdir", "int", "const char*"],

    ["mkdir", "int", "const char *", "mode_t"],
    ["mkdirat", "int", "int", "const char *", "mode_t"],

    ["mknod", "int", "const char *", "mode_t", "dev_t"],
    ["mknodat", "int", "int", "const char *", "mode_t", "dev_t"],

    ["mkdtemp", "char*", "char*"],
    ["mkfifo", "int", "const char *", "mode_t"],
    ["mktemp", "char*", "char*"],
    ["mkstemp", "int", "char*"],
]:
    arg_type = ", ".join(args_type)
    namedargs = ", ".join([
        T+f" arg{idx}"
        for idx, T in enumerate(args_type)
    ])
    argnames = ", ".join([
        f"arg{idx}"
        for idx, T in enumerate(args_type)
    ])
    fp.write(
        f"extern \"C\" {ret_type} {name}({namedargs})" + "\n"
        f"{{" + "\n"
        f"  auto org = ({ret_type} (*)({arg_type}))(dlsym(RTLD_NEXT, \"{name}\"));" + "\n"
        f"" + "\n"
        f"  if (fork_enabled)" + "\n"
        f"  {{" + "\n"
        f"    return org({argnames});" + "\n"
        f"  }}" + "\n"
        f"  else" + "\n"
        f"  {{" + "\n"
        f"    auto fp = fopen(\"safeEvalPy.log\", \"a+\");" + "\n"
        f"    fprintf(fp, \"syscall::{name}() is blocked\\n\");" + "\n"
        f"    fclose(fp);" + "\n"
        f"    return 0;" + "\n"
        f"  }}" + "\n"
        f"}}\n"
    )


os.system("g++ -shared -fPIC -rdynamic -g preload.c -o preload -ldl")
os.system("nm preload")
