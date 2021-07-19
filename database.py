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