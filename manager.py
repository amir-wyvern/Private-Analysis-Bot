import redis
import logging
import eventlet
from flask import Flask
from flask_socketio import SocketIO , emit
from hashlib import md5
import pickle

from binancePrivate import Client
from analysis import Indicator
from database import DataBase

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p' )


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*" ,async_mode='eventlet')

redis_conn = DataBase()
eventlet.monkey_patch()

ID = 0

class RedisChannel :

    @staticmethod
    def subcriber():
        global ID

        pubsub = redis_conn._pubsub()
        pubsub.subscribe("broadcast")
        for message in pubsub.listen(): 
            print(message)
            if ID:
                print('send to :' , ID)
                socketio.emit('userAddedResponse', {'resp': 'sub'} , to=ID) 


class Connection:

    @socketio.on('UserAdded')
    def connected(sid , message):
        global ID
        ID = sid
        print('UserAdded !' , message , sid)
        emit('userAddedResponse', {'resp': 'ok'})
        pass

    
    # ===================================================================


    @socketio.on('connect')
    def connected(sid):

        print('Connected !' ,sid)
        pass

    @socketio.on('disconnect')
    def disconnected(sid):

        print('Disconnected !' ,sid)
        pass

    @socketio.on('AddStrategy')
    def AddStrategy(sid ,message):

        stra = message['stra']
        timeSpan = message['time_span']

        hashStra = md5(pickle.dumps(stra)).hexdigest()[:12]
        hashCoins = md5(pickle.dumps(['BNBUSDT'])).hexdigest()[:12]

        if timeSpan :
            typeStra = 'backTest'
            hashTimeSpan = md5(pickle.dumps(timeSpan)).hexdigest()[:12]
            hashes = f'{hashStra}:{hashCoins}:{hashTimeSpan}'

        else:
            typeStra = 'current'
            hashes = f'{hashStra}:{hashCoins}'


        user = f'{typeStra}:123456'
        redis_resp = redis_conn._hsetnx(user ,hashes ,'0')

        if redis_resp:
            resp = 'existStra'

        else:
            resp = 'ok'

        emit('responseAddStrategy', {'resp': resp})
        

    @socketio.on('StreamResultPossition')
    def userAdded(message):

        print('Strategy Added\nMessage : {0}'.format(message))
        emit('responseAddStrategy', {'resp': 'ok'})
        pass

    @socketio.on('StrategiesList')
    def userAdded(message):

        print('Strategy Added\nMessage : {0}'.format(message))
        emit('responseAddStrategy', {'resp': 'ok'})
        pass


if __name__ == '__main__':

    eventlet.spawn(RedisChannel().subcriber) 
    socketio.run(app)