#!/bin/python3
import os
os.chdir(os.path.dirname(__file__))

fp = open("preload.cpp", "w")
with open("tmpl_header.cpp", "r") as header:
    fp.write(header.read())
for name, ret_type, *args_type in [
    ["forkpty", "pid_t",
     "int*", "char*", "const struct termios*", "const struct winesize*"],  # forkpty
    ["openpty", "int", "int*", "char*",
        "const struct termios*", "const struct winesize*"],  # os.openpty, pty.openpty
    ["login_tty", "int", "int"],

    ["fork", "int"],  # os.fork

    ["rmdir", "int", "const char*"],  # shutil.rmtree os.rmdir

    ["mkdir", "int", "const char *", "mode_t"],  # os.mkdir
    ["mkdirat", "int", "int", "const char *", "mode_t"],

    ["mknod", "int", "const char *", "mode_t", "dev_t"],  # os.mknod
    ["mknodat", "int", "int", "const char *", "mode_t", "dev_t"],

    ["mkfifo", "int", "const char *", "mode_t"],  # os.mkfifo
    ["mkfifoat", "int", "int", "const char *", "mode_t"],  # os.mkfifo

    ["mkdtemp", "char*", "char*"],  # tempfile.mkdtemp
    ["mktemp", "char*", "char*"],  # tempfile.mktemp
    ["mkstemp", "int", "char*"],  # tempfile.mkstemp

    ["opendir", "DIR *", "const char *"],  # os.listdir
    ["fdopendir", "DIR *", "int"],

    ["unlink", "int", "const char*"],  # os.unlink
    ["unlinkat", "int", "int", "const char*", "int"],

    ["posix_spawn", "int",  # os.posix_spawn
        "pid_t*",
        "const char*",
        "const posix_spawn_file_actions_t*",
        "const posix_spawnattr_t*",
        "char* const*",
        "char* const*"
     ],
    ["posix_spawnp", "int",  # os.posix_spawnp
        "pid_t*", "const char*",
        "const posix_spawn_file_actions_t*",
        "const posix_spawnattr_t*",
        "char* const*", "char* const*"
     ],

    ["exit_group", "void", "int"],
    ["_exit", "void", "int"],
    ["_Exit", "void", "int"],
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
fp.close()

os.system("gcc -shared -fPIC preload.cpp -o preload -ldl")
