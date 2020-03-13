import sys
import os
import datetime
from staticconf.loader import yaml_loader

class Config():
    config_list = ['db_uri','ui_url','google_api_key_dir','mailer_email','jwt_secret_key','jwt_access_token_expires']

    env_settings = {config_key.upper():config_key for config_key in config_list}
                        
    root_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(root_dir, 'config.yaml')

    app_config = yaml_loader(config_dir)

    for env_var, conf_var in env_settings.items():
        if env_var in os.environ:
            app_config[conf_var] = os.environ[env_var]

    ########### CHECK IF REQUIRED CONFIG EXIST
    required_config_list = frozenset(tuple(['db_uri','ui_url','google_api_key_dir','mailer_email','jwt_secret_key']))
    
    if required_config_list - frozenset(app_config.keys()):
        list_var = required_config_list-frozenset(app_config.keys())
        list_of_config_on_file = ', '.join(list_var)
        list_of_config_on_env = ', '.join({var.upper():var for var in list_var})

        raise Exception('config file must contain: ' + list_of_config_on_file + ' or environmental variable must contain: '+ list_of_config_on_env)
    
    ########### CAPITALIZE VARIABLE IF YOU WANT TO EXPOSE IT TO app.config value
    DB_URI = app_config['db_uri']
    UI_URL = app_config['ui_url']
    GOOGLE_API_KEY_DIR = app_config['google_api_key_dir']
    MAILER_EMAIL = app_config['mailer_email']
    JWT_SECRET_KEY = app_config['jwt_secret_key']

    if "jwt_access_token_expires" not in app_config:
        JWT_ACCESS_TOKEN_EXPIRES = False
        
    elif (isinstance(app_config['jwt_access_token_expires'], str) and app_config['jwt_access_token_expires'].isdigit()) or isinstance(app_config['jwt_access_token_expires'], int):
        JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=int(app_config['jwt_access_token_expires']))

    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False