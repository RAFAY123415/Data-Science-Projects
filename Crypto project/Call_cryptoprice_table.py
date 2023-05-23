
# I AM USING CALL CRYPTOPRICE_TABLE_DAILY_INTERVAL.PY INSTEAD OF THIS CALL_CRYPTOPRICE_TABLE TO READ DAILY DATA.

'''
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
            ValueInsertion.InsertIntoCryptoPricesTable(session, Tickers, mydb)


    finally:
        if (type(mydb) == str):
            print('Connect not exsists')
        else:
            mydb.close()

'''