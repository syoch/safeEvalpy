#!/bin/python3
import os
os.chdir(os.path.dirname(__file__))

fp = open("preload.cpp", "w")
with open("tmpl_header.cpp", "r") as header:
    fp.write(header.read())
for name, default, ret_type, *args_type in [
    ["forkpty", "0", "pid_t",
     "int*", "char*", "const struct termios*", "const struct winesize*"],  # forkpty
    ["openpty", "0", "int", "int*", "char*",
        "const struct termios*", "const struct winesize*"],  # os.openpty, pty.openpty
    ["login_tty", "0", "int", "int"],

    ["fork", "-1", "int"],  # os.fork

    ["rmdir", "0", "int", "const char*"],  # shutil.rmtree os.rmdir

    ["mkdir", "0", "int", "const char *", "mode_t"],  # os.mkdir
    ["mkdirat", "0", "int", "int", "const char *", "mode_t"],

    ["mknod", "0", "int", "const char *", "mode_t", "dev_t"],  # os.mknod
    ["mknodat", "0", "int", "int", "const char *", "mode_t", "dev_t"],

    ["mkfifo", "0", "int", "const char *", "mode_t"],  # os.mkfifo
    ["mkfifoat", "0", "int", "int", "const char *", "mode_t"],  # os.mkfifo

    ["mkdtemp", "0", "char*", "char*"],  # tempfile.mkdtemp
    ["mktemp", "0", "char*", "char*"],  # tempfile.mktemp
    ["mkstemp", "0", "int", "char*"],  # tempfile.mkstemp

    ["opendir", "0", "DIR *", "const char *"],  # os.listdir
    ["fdopendir", "0", "DIR *", "int"],

    ["unlink", "0", "int", "const char*"],  # os.unlink
    ["unlinkat", "0", "int", "int", "const char*", "int"],

    ["posix_spawn", "0", "int",  # os.posix_spawn
        "pid_t*",
        "const char*",
        "const posix_spawn_file_actions_t*",
        "const posix_spawnattr_t*",
        "char* const*",
        "char* const*"
     ],
    ["posix_spawnp", "0", "int",  # os.posix_spawnp
        "pid_t*", "const char*",
        "const posix_spawn_file_actions_t*",
        "const posix_spawnattr_t*",
        "char* const*", "char* const*"
     ],

    ["exit_group", "0", "void", "int"],
    ["_exit", "0", "void", "int"],
    ["_Exit", "0", "void", "int"],
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
    attr = "__attribute__ ((noreturn))" if "exit" in name.lower() else ""
    fp.write(
        f"extern \"C\" {ret_type} {attr} {name}({namedargs}){{" + "\n"
        f"  auto org = ({ret_type} (*)({arg_type}))(dlsym(RTLD_NEXT, \"{name}\"));" + "\n"
        f"  if (fork_enabled==true){{" + "\n" +
        f"    "+(
            f"return org({argnames});\n" if ret_type != "void"
            else f"org({argnames});\n"
        ) +
        f"  }}else{{" + "\n"
        f"    writelog(\"syscall::{name}() is blocked\\n\");" + "\n" +
        (
            f"    return {default};\n" if ret_type != "void"
            else ""
        ) +
        f"  }}" + "\n"
        f"}}\n"
    )
fp.close()

os.system("gcc -shared -fPIC preload.cpp -o preload -ldl")
