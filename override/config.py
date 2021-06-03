blocks = {
    "file": ["main.py", "token", ],
    "builtinFuncs": {
        "__import__": "override",
        "range": "override",
        "open": "override",
        "print": "override",
        "iter": "override",
        "globals": "block",
        "locals": "block",
        "input": "block",
        "exit": "block",
        "exec": "block",
        "quit": "block"
    }
}
blockedFunctions = {
    "sys": ["exit"],
    "os": ["system", "fork", "_exit", "kill", "killpg", "popen", "abort", "chdir", "fchdir", "getcwd", "open", "fdopen", ],
    "_thread": ["exit", "exit_thread"],
    "time": ["sleep"],
    "io": ["open", "open_code", "FileIO"],
    "_io": ["open", "open_code", "FileIO"],
    "tokenize": ["open", "_builtin_open"]
}
blockedModules = [
    "subprocess", "pty", 
    "ctypes", "signal",
    "pip",
    "importlib", "imp",
    "socket", "urllib", "http",
    "fileinput", "pathlib"
]
