import spacy
import gensim.downloader as api
from nltk import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import google.generativeai as genai
import time

genai.configure(api_key="")  # Replace with your API key

model = genai.GenerativeModel('gemini-pro')


safety_setting = {
    "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
    "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
    "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
}


# Download a pre-trained SpaCy model 
nlp = spacy.load("en_core_web_sm")

import en_core_web_sm

nlp = en_core_web_sm.load()

# Download pre-trained word embeddings
word_vectors = api.load("glove-wiki-gigaword-50")  


class Tweet:

    prompt = ""

    def __init__(self, id, tweet_url, user_screen_name, text, tweet_type, retweet_count):
        self.id = id
        self.tweet_url = tweet_url
        # self.created_at = created_at
        # self.parsed_created_at = parsed_created_at
        self.user_screen_name = user_screen_name
        self.text = text
        self.tweet_type = tweet_type
        self.retweet_count = retweet_count

    def set_prompt(self, prompt):
        self.prompt = prompt

    def get_tweet(self):
        return self.text

    def sentiment_analysis(self):
        tweet = self.text
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(tweet)
        compound_score = scores['compound']
        #return true if negative sentiment
        if compound_score <= -0.25: 
            return True
        else:
            return False
        
    def check_misinformation(self):
        try:
            response = model.generate_content(self.prompt, safety_settings=safety_setting)
            if str(response.text).strip().lower() == "yes":
                return True
            else:
                return False
        except:
            print(self.text)
            time.sleep(10)  
            return False


    def flag_tweet(self, keyword_list):

        # for keyword in keyword_list:
        #     if keyword not in word_vectors:
        #         print(keyword)
        #         keyword_list.remove(keyword)

        tweet = self.text
        tweet = word_tokenize(tweet.lower()) 
        # Named Entity Recognition
        doc = nlp(" ".join(tweet))
        entities = [(entity.text, entity.label_) for entity in doc.ents] 
        # Word Embedding Similarity
        for word in tweet:
            # if word in word_vectors:
            for fact_word in keyword_list:
                # similarity = word_vectors.similarity(word, fact_word)
                # if similarity >= 0.75:
                if fact_word == word:
                    print("Word Matched: ", word)
                    if self.check_misinformation() == True:
                        print("Tweet found: ", self.text)
                        return True
                        #run sentiment analysis
                        # if self.sentiment_analysis():
                        #     return True
                        # else: 
                        #     return False
            
        return False





  # def __init__(self, id, tweet_url, created_at, parsed_created_at, user_screen_name, text, tweet_type, hashtags, media, urls, favorite_count, in_reply_to_screen_name, in_reply_to_status_id, in_reply_to_user_id, lang, place, possibly_sensitive, retweet_count, retweet_or_quote_id, retweet_or_quote_screen_name, retweet_or_quote_user_id, source, user_id, user_created_at, user_default_profile_image, user_description, user_favorites_count, user_followers_count, user_friends_count, user_listed_count, user_location, user_name, user_statuses_count, user_time_zone, user_urls, user_verified):
    # self.hashtags = hashtags
    # self.media = media
    # self.urls = urls
    # self.favorite_count = favorite_count
    # self.in_reply_to_screen_name = in_reply_to_screen_name
    # self.in_reply_to_status_id = in_reply_to_status_id
    # self.in_reply_to_user_id = in_reply_to_user_id
    # self.lang = lang
    # self.place = place
    # self.possibly_sensitive = possibly_sensitive
    # self.retweet_count = retweet_count
    # self.retweet_or_quote_id = retweet_or_quote_id
    # self.retweet_or_quote_screen_name = retweet_or_quote_screen_name
    # self.retweet_or_quote_user_id = retweet_or_quote_user_id
    # self.source = source
    # self.user_id = user_id
    # self.user_created_at = user_created_at
    # self.user_default_profile_image = user_default_profile_image
    # self.user_description = user_description
    # self.user_favorites_count = user_favorites_count
    # self.user_followers_count = user_followers_count
    # self.user_friends_count = user_friends_count
    # self.user_listed_count = user_listed_count
    # self.user_location = user_location
    # self.user_name = user_name
    # self.user_statuses_count = user_statuses_count
    # self.user_time_zone = user_time_zone
    # self.user_urls = user_urls
    # self.user_verified = user_verified   