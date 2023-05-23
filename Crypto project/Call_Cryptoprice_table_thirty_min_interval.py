import GetDatabaseConnection
from CryptoNewsSentiment import CryptoControlAPI
from ValueInsert import ValueInsertion
import GetCoinMarketCapApiConnection

if __name__ == '__main__':
    try:
        mydb: object = GetDatabaseConnection.ReturnDatabaseConnection()
        session: object = GetCoinMarketCapApiConnection.ReturnApiConnection()
        Ticker = list(CryptoControlAPI.GetTickers())
        for Tickers in Ticker:
            CryptoValues = ValueInsertion.GetCryptoFeatureValues(session, Tickers)
            ValueInsertion.InsertIntoCryptoPricesTableThirtyMinuteInterval(CryptoValues, mydb)


    finally:
        if (type(mydb) == str):
            print('Connect not exsists')
        else:
            mydb.close()
