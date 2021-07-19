from time import time
import logging
import asyncio 
import json

import redis 
import aiohttp

from database import DataBase
from dotenv import dotenv_values

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p' )

class Log:

    def log(self ,func ,char= '>>'):

        textLog = '{0} {1} '.format( char ,func )
        logging.warning( textLog )


class AccessToDataBase( Log ):

    def __init__(self):

        self.con = DataBase()

    def _coinPrice(self ,coin ,timeFrame ,mainPrice):
        
        return self.con._hset('coinPrice' ,f'{coin}:{timeFrame}' ,mainPrice)

    def _coinsList(self ,start ,end):
        
        return self.con._lrange('coinsList' ,start ,end)


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

    async def sendRequest(self ,coin ,timeFrame):

        async with aiohttp.ClientSession() as session:
            
            try:
                _json = {'symbol': coin ,'interval': timeFrame}
                async with session.get(self.url ,params=_json ,headers= self.header ,timeout=20) as response:
                    
                    if response.status == 200:

                        mainPrice = await response.json()
                        self._coinPrice(coin ,timeFrame ,mainPrice)
                        
                    else:
                        raise f'sendRequest.[status: {response.status} ]'
                    

            except asyncio.TimeoutError as e:
                self.log(f'sendRequest.[TimeoutError | coin: {coin} ,timeFrame: {timeFrame}]' ,'-')

            except ValueError as ve :
                self.log(f'sendRequest.[Value Error in decode request Json | coin: {coin} ,timeFrame: {timeFrame}]' ,'!!')
            
            except Exception as e:
                self.log(f'Error [{e} | coin: {coin} ,timeFrame: {timeFrame}]' , '!!')

    def mainClerk(self):

        async def startJob():
            
            tempTimer = {   
                        '1m': {'remaining': 0 ,'cap': 1} ,
                        # '5m': {'remaining': 0 ,'cap': 1} ,
                        # '15m': {'remaining': 0 ,'cap': 1} ,
                        # '1h': {'remaining': 0 ,'cap': 1} ,
                        # '2h': {'remaining': 0 ,'cap': 1} ,
                        # '4h': {'remaining': 0 ,'cap': 30} ,
                        # '12h': {'remaining': 0 ,'cap': 45} ,
                        # '1d': {'remaining': 0 ,'cap': 60} ,
                        # '3d': {'remaining': 0 ,'cap': 200} ,
                        # '1w': {'remaining': 0 ,'cap': 500} 
                    }  

            while True:
                
                ls_timeFrame = []
                cp_tempTimer = tempTimer.copy()
                for frame ,value in cp_tempTimer.items() :
                    if value['remaining'] == 0: 
                        ls_timeFrame.append(frame)
                        tempTimer[frame]['remaining'] = tempTimer[frame]['cap']

                    else:
                        tempTimer[frame]['remaining'] = tempTimer[frame]['remaining'] -1

                coinList = self._coinsList(0 ,-1)

                tasks = [self.sendRequest(coin.upper() ,timeFrame) for coin in coinList for timeFrame in ls_timeFrame]

                await asyncio.gather(*tasks)

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(startJob())


RequestPrice().mainClerk()