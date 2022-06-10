import configparser


def generateConfig():
    config = configparser.ConfigParser()
    config["default"] = {
        "database_user": "bluevoyant",
        "database_password": "saurabh_is_hired",
        "database_host": "localhost",
        "database_name": "saurabh_bluevoyant",
        "table_name": "marvel"
    }

    with open('configuration.ini', 'w') as configfile:
        config.write(configfile)


generateConfig()
