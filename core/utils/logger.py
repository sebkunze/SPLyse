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