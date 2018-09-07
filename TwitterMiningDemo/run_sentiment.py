import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import config


class COSC6342Mining(object):

    def __init__(self):
        try:
            #Authentication process
            self.auth = OAuthHandler(config.consumer_key, config.consumer_secret)
            self.auth.set_access_token(config.access_token, config.access_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("***Authentication Failed***")

    def data_clean(self, tweet):
        # Removing unnecessary details
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    def sentiment_gather(self, data):
        #To get the sentiment of the data
        #Object TextBlod similar to NLTK - tokenizes and parses data
        test = TextBlob(self.data_clean(data))
        #finding sentiment of the data
        if test.sentiment.polarity > 0:
            return 'POSITIVE'
        elif test.sentiment.polarity == 0:
            return 'NEUTRAL'
        else:
            return 'NEGATIVE'

    def fetching_data(self, query, count = 100):
        #getting data and parsing it
        tweets_data = []

        try:
            # getting all tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # checking individual tweet
            for tweet in fetched_tweets:
                # to store details about the tweet
                parsed_data = {}

                parsed_data['text'] = tweet.text

                parsed_data['sentiment'] = self.sentiment_gather(tweet.text)

                if tweet.retweet_count > 0:
                    # if tweeted multiple times add only once
                    if parsed_data not in tweets_data:
                        tweets_data.append(parsed_data)
                else:
                    tweets_data.append(parsed_data)

            return tweets_data

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def main():
    # COSC6342Mining application instance
    api = COSC6342Mining()
    # getting twitter data from the account
    All_Tweets_Data = api.fetching_data(query='peace', count=500)

    # Finding Positive Data
    Tweets_Positive = [tweet for tweet in All_Tweets_Data if tweet['sentiment'] == 'POSITIVE']
    # Positive data Percent
    Positive_Percent = len(Tweets_Positive)* 100/len(All_Tweets_Data)
    print("Positive tweets percentage: {} %".format(Positive_Percent))
    # Finding Negative Data
    Tweets_Negative = [tweet for tweet in All_Tweets_Data if tweet['sentiment'] == 'NEGATIVE']
    # Negative data Percent
    Negative_Percent = len(Tweets_Negative) * 100 / len(All_Tweets_Data)
    print("Negative tweets percentage: {} %".format(Negative_Percent))
    # Neutral data Percent
    num = len(All_Tweets_Data)-len(Tweets_Negative) - len(Tweets_Positive)
    num = num /len(All_Tweets_Data)
    print("Neutral tweets percentage: {} % ".format(100 * num))

    f = open("tweets_positive.txt", "w+")
    # Printing Few Positive Tweets
    print("\n\nPositive tweets:")
    for tweet in Tweets_Positive[:50]:
        print(tweet['text'])
        f.write(tweet['text'])
        f.write('\n')
    f.close()

    f = open("tweets_negative.txt", "w+")

    # Printing Few Negative Tweets
    print("\n\nNegative tweets:")
    for tweet in Tweets_Negative[:50]:
        print(tweet['text'])
        f.write(tweet['text'])
        f.write('\n')
    f.close()


if __name__ == "__main__":
    # calling main function
    main()