#!/bin/python3
import os
os.chdir(os.path.dirname(__file__))

fp = open("preload.cpp", "w")
with open("tmpl_header.cpp", "r") as header:
    fp.write(header.read())
for name, in [
    ["fork"]
]:
    fp.write(
        f"extern \"C\" int {name}()" + "\n"
        f"{{" + "\n"
        f"  auto org = (int (*)())(dlsym(RTLD_NEXT, \"{name}\"));" + "\n"
        f"" + "\n"
        f"  if (fork_enabled)" + "\n"
        f"  {{" + "\n"
        f"    return org();" + "\n"
        f"  }}" + "\n"
        f"  else" + "\n"
        f"  {{" + "\n"
        f"    auto fp = fopen(\"safeEvalPy.log\", \"a+\");" + "\n"
        f"    fprintf(fp, \"syscall::{name}() is blocked\\n\");" + "\n"
        f"    fclose(fp);" + "\n"
        f"    return 0;" + "\n"
        f"  }}" + "\n"
        f"}}"
    )

os.system("gcc -shared -fPIC preload.cpp -o preload -ldl -rdynamic")
