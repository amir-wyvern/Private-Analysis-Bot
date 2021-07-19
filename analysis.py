import pandas_ta as ta
import pandas as pd

class Indicator:

    @staticmethod
    def rsi(pricePakage ,buy= 30 ,sell= 70 ,length= 14 ,source= 'close'):
        
        pd_price = pd.DataFrame(pricePakage)
        rsi_data = pd_price.ta.rsi(close=source ,length=length)

        xpoint = rsi_data.iloc[-1]

        if max(rsi_data.iloc[-4:]) >= sell:
            return 'sell'
        
        elif min(rsi_data.iloc[-4:]) <= buy:
            return 'buy'

        return None

    @staticmethod
    def ma_vs_price(pricePakage):
        
        pd_price = pd.DataFrame(pricePakage)
        ma_data = pd_price.ta.ma(close=source ,length=length)

    

