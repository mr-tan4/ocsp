from redis.exceptions import RedisError
from modules.configuration import Config
import redis


class RedisClient:
    r = redis.StrictRedis(host=Config.redis_host, port=Config.redis_port, db=Config.redis_db,
                          password=Config.redis_password)


class Cache(RedisClient):
    logger = Config.getLogger(__name__, Config.log_file, 'DEBUG')

    def __set__(self, key, value):
        if not isinstance(key, str):
            self.logger.ERROR('key 的类型为 %s,redis 中 key 的类型必须是string!' % key.__class__)
            raise TypeError("key must be string type!")
        try:
            self.r.set(key, value, ex=1000 * 60 * 60 * 24 * 7)
            self.logger.info('key 为 %s 的数据插入成功' % key)
        except RedisError as e:
            self.logger.error('插入失败!', e)
            print("set cache failed!", e)

    def del_cache(self, key):
        if not isinstance(key, str):
            self.logger.ERROR('key 的类型为 %s,redis 中 key 的类型必须是string!' % key.__class__)
            raise TypeError("key must by string type")
        if self.r.exists(key):
            self.r.delete(key)
            self.logger.info('key 为 %s 的记录删除成功！' % key)
        else:
            self.logger.error('key 为 %s 的记录不存在！' % key)
            pass

    def __get__(self, key):
        if not isinstance(key, str):
            self.logger.ERROR('key 的类型为 %s,redis 中 key 的类型必须是string!' % key.__class__)
            raise TypeError('key must by string type')
        try:
            data = self.r.get(key)
            self.logger.info('key 为 %s 的记录获取成功!' % key)
            return data
        except RedisError as e:
            self.logger.error('key 为 %s 的记录获取失败' % key, e)
            pass

    def is_active(self, key):
        if self.r.exists(key):
            return True
        else:
            return False
