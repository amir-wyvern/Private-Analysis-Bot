import logging
import json
 
import redis

def _checkExcept(func):

    def wrapper(*args):

        try :
            return func(*args)

        except Exception as err :
            logging.warning('| Redis.{0} => args{1} => error[{2}]'.format(func.__name__  ,args[1:] ,err) )
            return False
    
    return wrapper


class DataBase:
    """
    a layer on the dataBase to handle errors 
    """
    
    def __init__(self):

        self.__REDIS = redis.StrictRedis(host='127.0.0.1', port=6379 ,decode_responses= True)
        logging.warning( '*>Connected to DataBase ' )

    @_checkExcept
    def _get(self ,arg1):
        try:
            return json.loads( self.__REDIS.get(arg1) )
        
        except json.decoder.JSONDecodeError as e:
            return self.__REDIS.get(arg1) 

    @_checkExcept
    def _hget(self ,arg1 ,arg2):
        try:
            return json.loads( self.__REDIS.hget(arg1 ,arg2) )
            
        except json.decoder.JSONDecodeError as e:
            return self.__REDIS.hget(arg1 ,arg2)

    @_checkExcept
    def _set(self ,arg1 ,arg2):
        
        self.__REDIS.set(arg1 ,json.dumps(arg2))
        return True

    @_checkExcept
    def _hset(self ,arg1 ,arg2 ,arg3):
        
        self.__REDIS.hset(arg1 ,arg2 ,json.dumps(arg3))
        return True 

    @_checkExcept
    def _exists(self ,arg1):
    
        return self.__REDIS.exists(arg1 )

    @_checkExcept
    def _hexists(self ,arg1 ,arg2):
        
        return self.__REDIS.hexists(arg1 ,arg2)
            
    @_checkExcept
    def _hgetall(self ,arg1):
       
        return self.__REDIS.hgetall(arg1)
    
    @_checkExcept
    def _lrange(self ,arg1 ,start ,end):
        
        return self.__REDIS.lrange(arg1 ,start ,end)

    @_checkExcept
    def _hkeys(self ,arg1):
    
        return self.__REDIS.hkeys(arg1)

    @_checkExcept
    def _hdel(self ,arg1 ,arg2):

        return self.__REDIS.hdel(arg1 ,arg2)

    @_checkExcept
    def _pubsub(self):

        return self.__REDIS.pubsub()

    @_checkExcept
    def _hsetnx(self ,arg1 ,arg2 ,arg3):

        return self.__REDIS.hsetnx(arg1 ,arg2 ,arg3)
