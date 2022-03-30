from . import _eval, set_do_logging

set_do_logging(True)

print(".exit for exit")

while True:
    src = input('>>> ')

    if src == ".exit":
        break

    ret, out = _eval(src)
    print(ret)
    print("---")
    print(out)
