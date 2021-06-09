from . import core


def myRaise(exc_type, exc_value, tb):
    dest = core.ctx["stdout"]

    print('Exception:', file=dest)

    while tb:
        print(
            '  in %s:%d' %
            (tb.tb_frame.f_code.co_name, tb.tb_lineno),
            file=dest
        )
        tb = tb.tb_next

    print(f'  Detail: ({exc_type.__name__}) {exc_value}', file=dest)
