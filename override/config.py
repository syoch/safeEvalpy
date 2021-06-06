blocks = {
    "file": ["main.py", "token", ],
    "builtinFuncs": [
        "__import__",
        "range",
        "open",
        "print",
        "iter",
        "globals",
        "locals",
        "input",
        "exit",
        "exec",
        "quit",
    ]
}
blockedFunctions = {
    "sys": ["exit"],
    "os": [
        "system",
        "fork", "forkpty",  # overrided by preload
        "_exit", "kill", "killpg", "abort",
        "popen",
        "chdir", "fchdir",
        "getcwd",
        "open", "fdopen",
        "mkdir", "makedev", "makedirs"
        "rename", "renames", "replace",
        "remove", "removexattr",
        "removedirs", "rmdir",  # overrided by preload
    ],
    "shutil": [
        "_rmtree_isdir",
        "_rmtree_islink",
        "_rmtree_safe_fd",
        "_rmtree_unsafe",
        "rmtree",
    ],
    "_thread": ["exit", "exit_thread"],
    "time": ["sleep"],
    "io": ["open", "open_code", "FileIO"],
    "_io": ["open", "open_code", "FileIO"],
    "tokenize": ["open", "_builtin_open"],
    "pty": ["fork"],
    "threading": ["_after_fork"]
}
blockedModules = [
    "subprocess", "pty",
    "ctypes", "signal",
    "pip",
    "importlib", "imp",
    "socket", "urllib", "http",
    "fileinput", "pathlib"
]
