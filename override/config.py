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
    "os": ["system", "ofork", "forkpty", "register_at_fork", "_exit", "kill", "killpg", "popen", "abort", "chdir", "fchdir", "getcwd", "open", "fdopen", "mkdir"],
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
