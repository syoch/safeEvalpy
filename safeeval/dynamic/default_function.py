table = {}


def backup_default_function(name, func):
    table[name] = func


def backup_default_functions(dic: dict[str, callable]):
    for name, func in dic.items():
        backup_default_function(name, func)


def get_default_function(name):
    if name in table:
        return table[name]
    else:
        return None
