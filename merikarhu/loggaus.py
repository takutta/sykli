import logging
import os


def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    # create the logging file handler (scriptname.log)
    fh = logging.FileHandler(os.path.splitext(os.path.basename(__file__))[0] + ".log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # add console handler (stdout) to logger object
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


logger = create_logger()


def exception(error_text):
    """
    A decorator that wraps the passed-in function and logs
    exceptions should one occur
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = f"{error_text}. Function: {func.__name__}"
                logger.exception(err)

            # re-raise the exception
            # raise

        return wrapper

    return decorator

@exception("Can't create logging message")
def log(level, message, *args):
    log_function = getattr(logger, level, None)
    log_function(message, *args)