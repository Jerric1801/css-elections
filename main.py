from utils import scrapper, normalization, read_json, write_json, get_keywords
import pandas as pd 
from tweet import Tweet
from text_analysis import is_possibly_declarative
import csv

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
    # keyword_list = read_json("./scrapped_data/clinton_classified_keywords.json")["keywords"]
    # keyword_list = ["hillary", "emails", "email", "benghazi", "clinton", "fbi", "classified", "classification", "confidential", "leaked"]
    keyword_list = [
        "pizzagate",
        "Podesta",
        "Comet",
        "ping",
        "pong",
        "Trafficking",
        "Pedophilia",
        # "WikiLeaks",
        "james",
        "Alefantis",
        "PizzaGate",
        "Theory",
        "Satanic",
        # "Shop",
        "Parlors"
        "human",
        "ritual",
        "welch",
        "#pizzagate",
        "pizzeria",
        "child",
        "sex"
    ]

    keyword_list = [keyword.lower() for keyword in keyword_list]


    directory = "../datasets/"
    file = "election-day"
    elections_dataset = pd.read_csv(directory + file + ".csv", chunksize=2000)

    stop_running = False
    run_count = 0
    end_count = 10000
    misinformation = []

    try_count = 0
    for chunk in elections_dataset:
        for index, row in chunk.iterrows():
            tweet = Tweet(row.id, row.tweet_url, row.user_screen_name, row.text, row.tweet_type, row.retweet_count)
            if tweet.tweet_type == "original":
                prompt = f"Can the tweet below be considered misinformation about the Pizzagate incident in 2016 US elections? \n '{tweet.text}' \n Please reply with only one answer - 'yes' or 'no'"
                tweet.set_prompt(prompt)
                try_count += 1
                if tweet.flag_tweet(keyword_list):
                    misinformation.append(row)
                    run_count += 1
                    print(run_count)

            if run_count == end_count:
                stop_running = True
                break

        if stop_running == True:
            break

    # write_json({"tweets":potential_tweets},"./scrapped_data/third_debate_pizzagate.json.json")
    print("No. of lines runned ", try_count)

    # Define the filename for the new CSV file
    output_path = "results/debate_day_misinformation.csv"
    misinformation_df = pd.DataFrame(misinformation)
    misinformation_df.to_csv(output_path, index=False)




    # count = 0

    # potential_tweets = read_json("./scrapped_data/third_debate_pizzagate.json")["tweets"]

    # potential_declarative = []

    # for sentence in potential_tweets:
    #     if is_possibly_declarative(sentence):
    #         potential_declarative.append(sentence)

    # print('number of declarative ', count)

    # write_json({"tweets":potential_declarative},"./scrapped_data/potential_declarative.json")

if __name__ == "__main__":
    main()