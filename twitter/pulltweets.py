import got
from datetime import datetime
import peewee

BUFFER_LENGTH = 5
SINCE = "2018-01-01"
UNTIL = "2018-01-02"
MAX_TWEETS = 10

myDB = peewee.MySQLDatabase("seniorproject", host="seniorproject.cxbqypcd9gwp.us-east-2.rds.amazonaws.com", 
   port=3306, user="", passwd="")

class Tweet(peewee.Model):
   id = peewee.BigIntegerField()
   text = peewee.CharField()
   date = peewee.TimestampField()
   favorites = peewee.IntegerField()
   retweets = peewee.IntegerField()

   class Meta:
      database = myDB

def send_to_aws(tweet_array):
   # global test
   for t in tweet_array:
      # id, text, date, favorites, retweets
      # t.id, t.text.encode('utf-8')[:140], t.date.replace(second=0), t.favorites, t.retweets
      stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)
      pw_tweet = Tweet.create(id=t.id, text=stripped(t.text)[:140], date=t.date.replace(second=0),
         favorites=t.favorites, retweets=t.retweets)
      pw_tweet.save()

   print "Tweets: {} CurTime: {}\n    DateTime:{}".format(BUFFER_LENGTH, datetime.now(), tweet_array[BUFFER_LENGTH-1].date)


def main():
   # WRITE BEGINNING INFO
   print "Starting tweet download.\nBufferSize = {}\nStartTime = {}\n".format(BUFFER_LENGTH, datetime.now())

   tweetCriteria = got.manager.TweetCriteria().setQuerySearch('#bitcoin -giveaway -#freebitcoin').setSince(SINCE).setUntil(UNTIL)
   if(MAX_TWEETS):
      tweetCriteria.setMaxTweets(MAX_TWEETS)
   
   start = datetime.now()
   lap_time = datetime.now()

   try:
      got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer=send_to_aws, bufferLength=BUFFER_LENGTH)
   except Exception as e:
      print "Error occured at {}".format(datetime.now())
      print e.message

   end = datetime.now()
   myDB.close()

   print "\nFinished. Recieved tweets in {}".format(end-start)


if __name__ == '__main__':
   main()