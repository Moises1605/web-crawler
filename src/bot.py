from dotenv import load_dotenv
import tweepy
import gdown
import os
import uuid
class Bot:

    def __init__(self) -> None:
        load_dotenv()
        consumer_key = os.getenv("CONSUMER_KEY")
        consumer_secret = os.getenv("COMSUMER_SECRET")
        access_token = os.getenv("ACCESS_TOKEN")
        access_secret = os.getenv("ACCESS_SECRET")
        bearer_token = os.getenv("BEARER_TOKEN")

        self.client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_secret,
            bearer_token=bearer_token
        )

        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
        auth.set_access_token(
            access_token,
            access_secret
        )

        self.api = tweepy.API(auth)

    def post (self, data: dict):
        try:
            image_link = data['image']
            if image_link:
                path = "./temp/{}.jpg".format(uuid.uuid4())
                gdown.download(image_link,path)
                media = self.api.media_upload(filename=path)

            post = "Título: {}\n\nPreço anterior: R${}\nPreço Atual: R${}\n\nLink para acesso: {}".format(
                data['title'],
                str(format(data['old_price'], ".2f")).replace('.', ','),
                str(format(data['price'], ".2f")).replace('.', ','),
                data['link']
            )

            if image_link:
                self.client.create_tweet(text=post, media_ids=[media.media_id])
            else:
                self.client.create_tweet(text=post)
            
            return True

        except Exception as error:
            print(error)
            return False

        