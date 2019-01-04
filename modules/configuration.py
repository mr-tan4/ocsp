import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = 'DEBUG'
    TESTING = False

    def __getitem__(self, key):
        return self.__getattribute__(key)

    # 数据库相关配置
    db_url = '192.168.252.130'
    user_name = 'Robert'
    password = 'Robert#2018'
    db = 'robert'
    sql = 'SELECT cert,privatekey FROM robert.ocsp where ocsp_responder = \'{}\''
    port = 3306

    # redis 连接设置
    redis_host = 'redis'
    redis_port = '6379'
    redis_db = '1'
    redis_password = ''

    # restful 相关配置
    rest_server_url = '192.168.252.31'
    rest_server_port = 20026
    getUpCAData = 'http://' + rest_server_url + '/ocsp/getUpCAData?serialNumber={}'
    checkAllUpCAStatus = 'http://' + rest_server_url + '/ocsp/checkAllUpCAStatus?serialNumber={}'
    getMyData = 'http://' + rest_server_url + '/ocsp/getMyData?serialNumber={}'
    checkMyStatus = 'http://' + rest_server_url + '/ocsp/checkMyStatus?serialNumber={}'
    checkInDataTable = 'http://' + rest_server_url + '/ocsp/checkInDataTable?serialNumber={}'

    # rebbitmq
    rebbitmq_server_url = '192.168.252.31'
    rebbitmq_server_port = 20034

    # 日志配置
    log_file = './log/log.txt'

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
    db_url = '192.168.252.130'
    user_name = 'Robert'
    password = 'Robert#2018'
    db = 'robert'
    sql = 'SELECT cert,privatekey FROM robert.Ocsp where ocsp_responder = \'{}\''
    port = 3306

    log_file = './log/'
    if os.access(log_file, os.F_OK):
        pass
    else:
        os.makedirs(log_file)
        file_name = 'log.txt'
        open(file_name, 'w')
    license_port = 8080


class TestingConfig(Config):
    db_url = '192.168.10.133'
    user_name = 'cloudpki-dev'
    password = 'cloudpki-dev'
    db = 'cloudpki_dev'
    sql = 'SELECT cert,privatekey FROM cloudpki_dev.Ocsp where ocsp_responder = \'{}\''
    port = 3306
    log_file = './log/'
    if os.access(log_file, os.F_OK):
        pass
    else:
        os.makedirs(log_file)
        file_name = 'log.txt'
        open(file_name, 'w')


class ProductionConfig(Config):
    db_url = '192.168.10.133'
    user_name = 'cloudpki-dev'
    password = 'cloudpki-dev'
    db = 'cloudpki_dev'
    sql = 'SELECT cert,privatekey FROM cloudpki_dev.Ocsp where ocsp_responder = \'{}\''
    port = 3306

    log_file = './log/'
    if os.access(log_file, os.F_OK):
        pass
    else:
        os.makedirs(log_file)
        file_name = 'log.txt'
        open(file_name, 'w')


mapping = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'product:': ProductionConfig,
    'default': DevelopmentConfig
}

APP_ENV = os.environ.get('APP_ENV').lower()
print(mapping)
config = mapping['default']()
