from . import _eval

print(".exit for exit")

while True:
    src = input('>>> ')

    if src == ".exit":
        break

    ret, out = _eval(src)
    print(ret)
    print("---")
    print(out)
