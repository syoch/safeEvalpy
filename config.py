blocks = {
    "module": [
        "subprocess",
        "ctypes",
        "pip",
        "importlib", "imp",
        "socket", "urllib", "http",
        "fileinput", "pathlib"
    ],
    "file": ["main.py", "token", ],
    "builtinFuncs": {
        "__import__": "myImport",
        "range": "myRange",
        "open": "myOpen",
        "print": "myPrint",
        "iter": "myIter",
        "globals": None,
        "locals": None,
        "input": None,
        "exit": None,
        "exec": None,
        "quit": None
    },
    "funcs": {
        "sys": ["exit"],
        "os": ["system", "fork", "_exit", "popen", "abort", "chdir", "fchdir", "getcwd", "open", "fdopen", ],
        "_thread": ["exit", "exit_thread"],
        "time": ["sleep"],
        "io": ["open", "open_code", "FileIO"],
        "_io": ["open", "open_code", "FileIO"],
        "tokenize": ["open", "_builtin_open"]
    }
}
