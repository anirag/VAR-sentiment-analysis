import os
import tweepy as tw
import pandas as pd
import config
import daiquiri, logging
import json
from tqdm import tqdm

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger()

logger.info("Setting up the twitter app authentication...")
auth = tw.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)
logger.info("API setup DONE!!!")

logger.info("Extract tweets containing VAR and premier league...")
search_query = "(VAR epl) OR (VAR Premier League) OR (VAR premier league) OR (VAR EPL) OR (var epl) OR (var Premier League) OR (var premier league) -filter:retweets"
date_since = "2019-09-01"
date_until = "2019-10-01"
tweets = tw.Cursor(
    api.search, q=search_query, lang="en", since=date_since, until=date_until
).items(config.limit)
# print(f"Number of Tweets Extracted : {tweets.count()}")
pBar = tqdm(tweets, ascii=True, total=config.limit, desc="Getting Tweets!")

F_NAME = config.DATA_DIR + "VAR_tweets.json"
with open(F_NAME, "w") as f_out:
    for cnt, tweet in enumerate(pBar):
        pBar.update(1)
        if not cnt < config.limit:
            break
        json.dump(tweet._json, f_out)
        f_out.write("\n")
logger.info("Tweets Extracted!!!")

