import pika
from core.redisClient.redisResultCache import Cache
from modules.configuration import Config
import os


class ampqClient:
    logger = Config.getLogger(__name__, Config.log_file, 'DEBUG')

    def __init__(self):
        credentials = pika.PlainCredentials('admin', 'admin')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=Config.rebbitmq_server_url, port=Config.rebbitmq_server_port,
                                      credentials=credentials))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='status', durable=True)
        self.channel.basic_consume(self.callback, queue='status', no_ack=True)
        self.logger.info('当前线程ID为: %s，当前子线程ID为 %s' % (os.getpid(), os.getppid()))
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        if body is not None and body.decode('utf-8') != '':
            self.logger.info('获取序列号为 %s' % body.decode('utf-8'))
            Cache().del_cache(key=body.decode('utf-8'))
            self.logger.info('key 为 %s 的cache处理成功' % body.decode('utf-8'))
        else:
            self.logger.error('消息体为空！')
            pass
