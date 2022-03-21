import os

base_path = os.getcwd()


def _format(ex):
    tb = ex.__traceback__

    ret = 'Exception:\n'

    while tb:
        ret += '  in %s:%d (%s)\n' % (
            tb.tb_frame.f_code.co_filename.replace(base_path, "."),
            tb.tb_lineno,
            tb.tb_frame.f_code.co_name
        )
        tb = tb.tb_next

    ret += f'  Detail: ({type(ex).__name__ if ex else ""}) {ex}\n'

    return ret


def format(ex):
    try:
        return _format(ex)
    except Exception:
        return "Exception: Unformattable exception"
