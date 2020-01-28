import sys
import os
from staticconf.loader import yaml_loader

class Config():
    config_list = ['db_dir','jwt_secret_key']

    config_file_settings = frozenset(tuple(config_list))

    env_settings = {config_key.upper():config_key for config_key in config_list}
                        
    root_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(root_dir, 'config.yaml')

    app_config = yaml_loader(config_dir)

    for env_var, conf_var in env_settings.items():
        if env_var in os.environ:
            app_config[conf_var] = os.environ[env_var]

    if config_file_settings - frozenset(app_config.keys()):
        raise Exception(
            'config must contain %s' %
            (', '.join(
                    config_list -
                    frozenset(
                        app_config.keys()))))
    
    ########### CAPITALIZE VARIABLE IF YOU WANT TO EXPOSE IT TO app.config value
    DB_DIR = app_config['db_dir']
    JWT_SECRET_KEY = app_config['jwt_secret_key']
    LOG_LEVEL = "DEBUG"
    PROPAGATE_EXCEPTIONS = False