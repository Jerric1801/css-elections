from utils import scrapper, normalization, read_json, write_json, get_keywords
import pandas as pd 
from tweet import Tweet
from text_analysis import is_possibly_declarative

def main():
    # web scrape
#   url = "https://www.factcheck.org/2016/07/clintons-handling-of-classified-information/"
#   scrapped_data = scrapper(url)   
#   write_json(scrapped_data, "./scrapped_data/clinton_classified.json")
    # scrapped = "./scrapped_data/clinton_classified.json"
    # scrapped_data = read_json(scrapped)["content"]
    # normalized_data = normalization(scrapped_data)
    # keyword_list = get_keywords(normalized_data)
    # write_json({"keywords":keyword_list},"./scrapped_data/clinton_classified_keywords.json")
    keyword_list = read_json("./scrapped_data/clinton_classified_keywords.json")["keywords"]
    # keyword_list = ["hillary", "emails", "email", "benghazi", "clinton", "fbi", "classified", "classification", "confidential", "leaked"]

    directory = "../datasets/"
    file = "first-debate"
    elections_dataset = pd.read_csv(directory + file + ".csv", chunksize=2000)

    stop_running = False
    run_count = 0
    end_count = 500
    potential_tweets = []

    try_count = 0

    for chunk in elections_dataset:
        for index, row in chunk.iterrows():
            tweet = Tweet(row.id, row.tweet_url, row.user_screen_name, row.text, row.tweet_type)
            if tweet.tweet_type == "original":
                try_count += 1
                if tweet.flag_tweet(keyword_list):
                    potential_tweets.append(tweet.text)
                    run_count += 1

            if run_count == end_count:
                stop_running = True
                break

        if stop_running == True:
            break

    write_json({"tweets":potential_tweets},"./scrapped_data/potential_tweets.json")
    print("No. of lines runned ", try_count)

    count = 0

    potential_tweets = read_json("./scrapped_data/potential_tweets.json")["tweets"]

    potential_declarative = []

    for sentence in potential_tweets:
        if is_possibly_declarative(sentence):
            potential_declarative.append(sentence)

    print('number of declarative ', count)

    write_json({"tweets":potential_declarative},"./scrapped_data/potential_declarative.json")

if __name__ == "__main__":
    main()