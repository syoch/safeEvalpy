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
