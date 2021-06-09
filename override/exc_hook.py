def myRaise(exc_type, exc_value, tb):
    print('Exception:')

    while tb:
        print(
            '  in %s:%d' %
            (tb.tb_frame.f_code.co_name, tb.tb_lineno)
        )
        tb = tb.tb_next

    print('  Detail: (%s) %s' % (exc_type.__name__, str(exc_value)))
