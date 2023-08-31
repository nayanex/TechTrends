import logging
import sys
from datetime import datetime


# https://www.datacamp.com/community/tutorials/decorators-python
# https://www.python.org/dev/peps/pep-0318/#design-goals
def logging_message(app):
    def func_wrapper(func):
        """stream logs to app.log file"""
        # logging.basicConfig(filename="app.log", level=logging.DEBUG)
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger_handler = logging.StreamHandler(sys.stdout)
        logger_handler.setLevel(logging.DEBUG)
        logger_formatter = logging.Formatter('%(levelname)s:%(name)s:%(asctime)s %(message)s',
                                             datefmt='%m/%d/%Y, %I:%M:%S')
        logger_handler.setFormatter(logger_formatter)
        logger.addHandler(logger_handler)
        logger_error_handler = logging.StreamHandler(sys.stderr)
        logger_error_handler.setLevel(logging.ERROR)
        logger_error_handler.setFormatter(logger_formatter)

        timestamp = datetime.now()
        function_name = func.__name__

        app.logger.info(f"{timestamp}, {function_name} endpoint request was reached successfully.")
        return func

    return func_wrapper
