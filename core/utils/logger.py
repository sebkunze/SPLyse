import os
import logging.config

import yaml

# NOTE: See Logging Cookbook for reference at https://docs.python.org/2/howto/logging-cookbook.html#logging-cookbook

def setup(default_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)

    if value:
        path = value

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

# filename = 'SPLyse.log'
#
# log = logging.getLogger("SPLyse")
# log.setLevel(logging.DEBUG)
#
# # create a file handler.
# handler = logging.FileHandler(filename)
# handler.setLevel(logging.DEBUG)
#
# # create a logging format.
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
#
# # add the handler to the logger.
# log.addHandler(handler)
#
# # use for a serious error, indicating that the program itself may be unable to continue running.
# def critical(msg, args = []):
#     log.critical(msg, args);
#
# # use for a more serious problem, the software has not been able to perform some function.
# def error(msg, args = []):
#     log.error(msg, args)
#
# # use for an indication that something unexpected happened, or indicative of some problem in the near future. The software is still working as expected.
# def warn(msg, args = []):
#     log.warn(msg, args)
#
# # use for confirmation that things are working as expected.
# def info(msg, args = []):
#     log.info(msg, args)
#
# # use for detailed information, typically of interest only when diagnosing problems.
# def debug(msg, args = []):
#     log.debug(msg, args)