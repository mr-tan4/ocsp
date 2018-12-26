import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = 'DEBUG'
    TESTING = False

    def __getitem__(self, key):
        return self.__getattribute__(key)

    # 数据库相关配置
    db_url = '192.168.10.133'
    user_name = 'cloudpki-dev'
    password = 'cloudpki-dev'
    db = 'cloudpki_dev'
    sql = 'SELECT cert,privatekey FROM cloudpki_dev.Ocsp where ocsp_responder = \'{}\''
    port = 3306

    # redis 连接设置
    redis_host = '127.0.0.1'
    redis_port = '6379'
    redis_db = '1'
    redis_password = ''

    # restful 相关配置
    rest_server_url = '192.168.10.133'
    rest_server_port = 8889
    getUpCAData = 'http://' + rest_server_url + '/ocsp/getUpCAData?serialNumber={}'
    checkAllUpCAStatus = 'http://' + rest_server_url + '/ocsp/checkAllUpCAStatus?serialNumber={}'
    getMyData = 'http://' + rest_server_url + '/ocsp/getMyData?serialNumber={}'
    checkMyStatus = 'http://' + rest_server_url + '/ocsp/checkMyStatus?serialNumber={}'
    checkInDataTable = 'http://' + rest_server_url + '/ocsp/checkInDataTable?serialNumber={}'

    # 日志配置
    log_file = '/Users/robert/ocsp/log/log.txt'

    def getLogger(cls, file=None, level='INFO'):
        import logging
        logger = logging.getLogger(cls)
        logger.setLevel(level=level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        if file is not None:
            handler = logging.FileHandler(file)
            handler.setLevel(level=level)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        console = logging.StreamHandler()
        console.setLevel(level=level)
        console.setFormatter(formatter)
        logger.addHandler(console)
        return logger


class DevelopmentConfig(Config):
    db_url = '192.168.10.133'
    user_name = 'cloudpki-dev'
    password = 'cloudpki-dev'
    db = 'cloudpki_dev'
    sql = 'SELECT cert,privatekey FROM cloudpki_dev.Ocsp where ocsp_responder = \'{}\''
    port = 3306

    log_file = '/Users/robert/ocsp/log/log.txt'

    license_port = 8080


class TestingConfig(Config):
    db_url = '192.168.10.133'
    user_name = 'cloudpki-dev'
    password = 'cloudpki-dev'
    db = 'cloudpki_dev'
    sql = 'SELECT cert,privatekey FROM cloudpki_dev.Ocsp where ocsp_responder = \'{}\''
    port = 3306

    log_file = '/Users/robert/ocsp/log/log.txt'


class ProductionConfig(Config):
    db_url = '192.168.10.133'
    user_name = 'cloudpki-dev'
    password = 'cloudpki-dev'
    db = 'cloudpki_dev'
    sql = 'SELECT cert,privatekey FROM cloudpki_dev.Ocsp where ocsp_responder = \'{}\''
    port = 3306

    log_file = '/Users/robert/ocsp/log/log.txt'


mapping = {
    'Development': DevelopmentConfig,
    'Testing': TestingConfig,
    'Production:': ProductionConfig,
    'default': DevelopmentConfig
}

APP_ENV = os.environ.get('APP_ENV', 'default').lower()
config = mapping['default']()
