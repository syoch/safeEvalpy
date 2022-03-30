blocked_files = ["main.py", "token", ".env"]
blocked_functions = [
    "globals",
    "locals",

    "input",

    "exit",
    "exec",
    "quit",
    "bytearray",
    "license"
]
module_block = {
    "sys": ["exit"],
    "os": [
        "system",
        "fork", "forkpty",  # blocked by preload
        "_exit", "kill", "killpg", "abort",
        "popen",
        "chdir", "fchdir",
        "getcwd",
        "open", "fdopen",
        "rename", "renames", "replace",
        "remove",

        "rmdir",  "mkdir",  "mknod", "mkfifo",  # blocked by preload
        "listdir",  # blocked by preload
        "system"  # blocked by preload
    ],
    "shutil": [
        "_rmtree_isdir",
        "_rmtree_islink",
        "_rmtree_safe_fd",
        "_rmtree_unsafe",
        "rmtree",  # blocked by preload
    ],
    "_thread": ["exit", "exit_thread"],
    "time": ["sleep"],
    "io": ["open", "open_code", "FileIO"],
    "_io": ["open", "open_code", "FileIO"],
    "tokenize": ["open", "_builtin_open"],
    "pty": ["fork"],
    "threading": ["_after_fork"],
    "tempfile": ["mkdtemp", "mktemp", "mkstemp"],  # blocked by preload
    "subprocess": [...],
    "ctypes": [...],
    "signal": [...],
    "pip": [...],
    "importlib": [...],
    "imp": [...],
    "socket": [...],
    "urllib": [...],
    "http": [...],
    "fileinput": [...],
    "pathlib": [...],
    "_socket": [...],
    "dotenv": [...],
    "builtins": [...],
    "pickle": [...],
}
