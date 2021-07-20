from time import time ,sleep
import logging
import asyncio 
import json

import redis 
import aiohttp

from database import DataBase
from dotenv import dotenv_values

from typing import Tuple

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p' )

class Log:

    def log(self ,func ,char= '>>'):

        textLog = '{0} {1} '.format( char ,func )
        logging.warning( textLog )


class AccessToDataBase( Log ):
    """using madual database for connect to redis"""

    def __init__(self):

        self.con = DataBase()

    def _setCurrentPrice(self ,pair ,mainPrice ,timeFrame ):
        
        return self.con._hset('pairCurrentPrice' ,f'{pair}:{timeFrame}' ,mainPrice)

    def _setHistoryPrice(self ,pair ,priceData ,timeFrame ,startTime ,endTime):

        return self.con._hset('pairHistoryPrice' ,f'{pair}:{timeFrame}|{startTime}:{endTime}' ,priceData)

    def _getCurrentList(self) -> list:
        
        return self.con._lrange('pairCurrentList' ,0 ,-1)

    def _getHistoryList(self) -> dict:

        return self.con._hgetall('pairHistoryList')

    def _delKeyHistoryList(self ,key):

        return self.con._hdel('pairHistoryList' ,key)

class RequestPrice( AccessToDataBase ):

    def __init__(self ):

        super().__init__()
        
        self.checkApiKey()

        self.header = {'X-MBX-APIKEY' : self.API_KEY}
        self.url= 'https://api.binance.com/api/v3/klines'

    def checkApiKey(self):

        dic = dotenv_values(".env")
        if 'API_KEY' not in dic:
            self.log('Not Found API_KEY in .env file' ,'!!')
            return 

        self.API_KEY = dic['API_KEY']
        
    async def sendRequest(self ,pair ,timeFrame ,tupeHistory : Tuple[int ,int] = False ) -> None:

        async with aiohttp.ClientSession() as session:
            
            try:
                
                _json = {'symbol': pair ,'interval': timeFrame ,'limit': 100}
                if tupeHistory :
                    _json.update({'startTime': tupeHistory[0] ,'endTime': tupeHistory[1] })

                async with session.get(self.url ,params=_json ,headers= self.header ,timeout=20) as response:
                    
                    if response.status == 200:

                        priceData = await response.json()
                        if tupeHistory:
                            self._setHistoryPrice(pair ,priceData ,timeFrame ,tupeHistory[0] ,tupeHistory[1])
                        
                        else:
                            self._setCurrentPrice(pair ,priceData ,timeFrame)

                    else:
                        raise f'sendRequest.[status: {response.status} ]'
                    

            except asyncio.TimeoutError as e:
                self.log(f'sendRequest.[TimeoutError | pair: {pair} ,timeFrame: {timeFrame}]' ,'-')

            except ValueError as ve :
                self.log(f'sendRequest.[Value Error in decode request Json | pair: {pair} ,timeFrame: {timeFrame}]' ,'!!')
            
            except Exception as e:
                self.log(f'Error [{e} | pair: {pair} ,timeFrame: {timeFrame}]' , '!!')

    def mainClerk(self):
        """
        Use async to send group requests Asynchronous to the binance server
        Group request means that ,A request will be sent for each currency for each time frame (in this case just use '1m')
        """

        async def startJob():
            
            while True:
                
                tasks = []
                    
                for key, value in self._getHistoryList().items() :  # {"btcusdt:1m" : "12345:12367"}

                    self._delKeyHistoryList(key)

                    pair = key.split(':')[0]
                    timeFrame = key.split(':')[1]
                    startTime = int(value.split(':')[0])
                    endTime = int(value.split(':')[1])

                    tasks.append(self.sendRequest(pair.upper() ,timeFrame ,(startTime ,endTime)))
                
                for item in self._getCurrentList():

                    pair = item.split(':')[0]
                    timeFrame = item.split(':')[1]
                    tasks.append(self.sendRequest(pair.upper() ,timeFrame))

                if not tasks :

                    sleep(1)
                    continue


                await asyncio.gather(*tasks)

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # NOTE: this line is only used in Windows | in Linux is no need to use it 
        asyncio.run(startJob())


RequestPrice().mainClerk()