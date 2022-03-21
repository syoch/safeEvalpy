import os


def getcwd():
    from .override.patches import enabled_patches, context
    if enabled_patches:
        return context.function_backups["__import__"]("os").getcwd()

    return os.getcwd()


def format(ex):
    tb = ex.__traceback__

    ret = 'Exception:\n'

    while tb:
        ret += '  in %s:%d (%s)\n' % (
            tb.tb_frame.f_code.co_filename.replace(getcwd(), "."),
            tb.tb_lineno,
            tb.tb_frame.f_code.co_name
        )
        tb = tb.tb_next

    ret += f'  Detail: ({type(ex).__name__ if ex else ""}) {ex}\n'

    return ret
