import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("testrun.log", mode='w')
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def log_method_calls(func):
    def wrapper(*args, **kwargs):
        args_str = ', '.join(map(repr, args[1:]))  # Exclude the first argument (self)
        kwargs_str = ', '.join(f"{key}={value!r}" for key, value in kwargs.items())
        arg_list = [arg for arg in [args_str, kwargs_str] if arg]
        logger.debug(f"{func.__name__}({', '.join(arg_list)})")
        return func(*args, **kwargs)
    return wrapper


def log_test(func):
    def wrapper(*args, **kwargs):
        logger.debug(f"\n* Starting test: {func.__name__} *\n")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  # Preserve the original method name
    return wrapper


def log_step(func):
    def wrapper(*args, **kwargs):
        logger.debug(f"\n\t- Test Step: {func.__name__}")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper