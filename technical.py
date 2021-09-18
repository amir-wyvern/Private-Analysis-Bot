import pandas_ta as ta
import pandas as pd

class Indicator:

    @staticmethod
    def rsi(pricePackage ,buy= 30 ,sell= 70 ,length= 14 ,source= 'close' ,start_index = 0):
        
        pd_price = pd.DataFrame(pricePackage)
        rsi_data = pd_price.ta.rsi(close=source ,length=length)

        if start_index < length :
            start_index = length
            
        res = []

        for i in range(start_index , len(rsi_data)):

            maxPrice = max([ pricePackage[i]['open'] ,pricePackage[i]['close'] ,pricePackage[i]['high'] ,pricePackage[i]['low']])
            minPrice = min([ pricePackage[i]['open'] ,pricePackage[i]['close'] ,pricePackage[i]['high'] ,pricePackage[i]['low']])

            if min(rsi_data.iloc[i-4:i+1]) <= buy :
                res.append( [
                            'buy' ,                     # type
                            rsi_data.iloc[i],           # rsi
                            pricePackage[i]['open'] ,   # open
                            pricePackage[i]['close'] ,  # close
                            pricePackage[i]['high'] ,   # high
                            pricePackage[i]['low']      # low
                            ]  
                            )

            elif max(rsi_data.iloc[i-4:i+1]) >= sell :
                res.append( [
                            'sell' ,                    # type
                            rsi_data.iloc[i],           # rsi
                            pricePackage[i]['open'] ,   # open
                            pricePackage[i]['close'] ,  # close
                            pricePackage[i]['high'] ,   # high
                            pricePackage[i]['low']      # low
                            ]  
                            )

            else:
                res.append( [
                            '' ,                        # type
                            rsi_data.iloc[i],           # rsi
                            pricePackage[i]['open'] ,   # open
                            pricePackage[i]['close'] ,  # close
                            pricePackage[i]['high'] ,   # high
                            pricePackage[i]['low']      # low
                            ]  
                            )

        return res

    @staticmethod
    def ma_vs_price(pricePackage ,buy= 30 ,sell= 70 ,length= 14 ,source= 'close' ,start_index = 0):
        
        pd_price = pd.DataFrame(pricePackage)
        sma_data = pd_price.ta.sma(close=source ,length=length)

        if start_index < length :
            start_index = length

        res = []

        for i in range(start_index , len(sma_data)):

            maxPrice = max([ pricePackage[i]['open'] ,pricePackage[i]['close'] ,pricePackage[i]['high'] ,pricePackage[i]['low']])
            minPrice = min([ pricePackage[i]['open'] ,pricePackage[i]['close'] ,pricePackage[i]['high'] ,pricePackage[i]['low']])

            if minPrice > sma_data.iloc[i] :
                res.append( [
                            'buy' ,                     # type
                            sma_data.iloc[i],           # sma
                            pricePackage[i]['open'] ,   # open
                            pricePackage[i]['close'] ,  # close
                            pricePackage[i]['high'] ,   # high
                            pricePackage[i]['low']      # low
                            ]  
                            )

            elif maxPrice < sma_data.iloc[i] :
                res.append( [
                            'sell' ,                    # type
                            sma_data.iloc[i],           # sma
                            pricePackage[i]['open'] ,   # open
                            pricePackage[i]['close'] ,  # close
                            pricePackage[i]['high'] ,   # high
                            pricePackage[i]['low']      # low
                            ]  
                            )

            else:
                res.append( [
                            '' ,                        # type
                            sma_data.iloc[i],           # sma
                            pricePackage[i]['open'] ,   # open
                            pricePackage[i]['close'] ,  # close
                            pricePackage[i]['high'] ,   # high
                            pricePackage[i]['low']      # low
                            ]  
                            )

        return res


    

