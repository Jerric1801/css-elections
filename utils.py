import requests
from bs4 import BeautifulSoup
import json
import re  
import nltk 
from collections import Counter
import pandas as pd

# nltk.download('vader_lexicon')
# nltk.download('punkt') # Download for sentence tokenization (if needed)
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

def scrapper(url, div_class = "entry-content", output_file="data/scrapped_data.json"):
    response = requests.get(url)
    response.raise_for_status()  # Check for errors

    soup = BeautifulSoup(response.text, "html.parser")

    scrapped_data = {}

    title = soup.find("h1").text
    scrapped_data["title"] = title

    # change this based on site you are scrapping
    site_class = div_class

    div = soup.find("div", {"class": site_class})
    info = div.find_all("p")

    content = []

    for p in info:
        content.append(p.text)

    scrapped_data["content"] = content

    return scrapped_data


def normalization(content):

    normalized_content = []
    for text in content:
        # 1. Lowercasing
        text = text.lower()

        # 2. Punctuation Removal (adjust as needed)
        text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation except for basic word characters and spaces

        # 3. Tokenization (optional, for word-by-word analysis)
        tokens = nltk.word_tokenize(text) 

        # 4. Stop Word Removal (optional)
        stop_words = set(nltk.corpus.stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]

        # 5. Recombine tokens into text (if you did tokenization):
        normalized_text = " ".join(tokens)

        normalized_content.append(normalized_text)

    return normalized_content

def write_json(data, output_file):
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)


def read_json(json_file):
    with open(json_file, 'r') as f:
        scrapped_data = json.load(f)
    
    return scrapped_data

def get_keywords(normalized_content):
    if not isinstance(normalized_content, list):
        raise ValueError("normalized_content must be a list")
    word_counts = Counter()

    for paragraph in normalized_content:
        words = paragraph.split() 
        word_counts.update(words)

    keywords_df = pd.DataFrame.from_dict(dict(word_counts.items()), orient='index', columns=['Count'])
    keywords_df.sort_values(by='Count', ascending=False, inplace=True)

    #if want to see word count
    # print(keywords_df)
    keyword_list = keywords_df.index.tolist() 

    return keyword_list      