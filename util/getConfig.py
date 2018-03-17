import configparser

def go():
    config = configparser.SafeConfigParser()
    config.read('config.ini')
    return config