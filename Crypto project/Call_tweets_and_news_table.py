import GetDatabaseConnection
import GetGoogleSheetConnection
from CryptoNewsSentiment import CryptoControlAPI
from ValueInsert import ValueInsertion
import GetTweetsConnection
from TweetsSentiment import Tweets

if __name__ == '__main__':

     try:

        # reading database connection
        mydb: object = GetDatabaseConnection.ReturnDatabaseConnection()
        # reading google_api connection
        mygooglesheet: object = GetGoogleSheetConnection.Return_Connection()
        # initializing cryptoapi class to fetch list of tickers and news type like ( articles , videos )
        Api = CryptoControlAPI()
        # fetch type of news that we want to read i am reading article news and video news
        Type = list(CryptoControlAPI.GetType())
        # fetch tickers like Bitcoin, Ethereum
        Ticker = list(CryptoControlAPI.GetTickers())
        # Get Latest News and Insert Into Database
        for Tickers in Ticker:
            for Category in Type:
                data = Api.GetLatestNewsByType(Tickers, Category)
                ValueInsertion.InsertIntoNewsTable(data, Tickers, mydb)
        # Insert Value into Google Sheets
        ValueInsertion.InsertNewsIntoGoogleSheets(mydb, mygooglesheet)

        tweets = Tweets()
        # fetching api keys form the function
        TweetsConnection: object = GetTweetsConnection.GetTweetsConnection()
        # authenticate that the giving api_keys are correct to read data
        AuthenticationApi = tweets.getAuthentication(TweetsConnection)
        # search for the specific topic coin
        SearchCoin = list(tweets.getTicker())
        # Seraching for the specific query

        for query in SearchCoin:
            data = tweets.getTweets(AuthenticationApi, query)
            ValueInsertion.InsertIntoTweetsTable(data, mydb)



     finally:
         mydb.close()


