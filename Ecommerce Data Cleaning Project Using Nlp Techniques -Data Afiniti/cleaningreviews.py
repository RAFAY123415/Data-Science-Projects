# Install necessary libraries
#Here's the complete set of pip install commands for the libraries that need to be installed:

'''!pip install vaderSentiment
!pip install pandas
!pip install numpy
!pip install nltk
!pip install wordcloud
!pip install matplotlib'''

import nltk
# Ensure the necessary NLTK data packages are downloaded (only needed for first-time setup in a new environment)
# nltk.download('stopwords')  # Remove comment and Download stopwords if not already downloaded
# nltk.download('punkt')      # Remove comment and Download the Punkt tokenizer if not already downloaded

#Importing Libraries
import pandas as pd
#import numpy as np
import json
from collections import OrderedDict
from html import unescape
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
#from wordcloud import WordCloud
#import matplotlib.pyplot as plt
import re
import os

# This Function Converts JSON Data File Into DataFrame.
def load_json_to_df(file_path,encoding='utf-8'):
    """
    Load JSON data from a text file line by line, convert to DataFrames, and concatenate them.

    Parameters:
    file_path (str): The path to the text file containing JSON data.

    Returns:
    pd.DataFrame: A combined DataFrame containing all the JSON data.
    """

    # Read the JSON data from the text file line by line and normalize it directly
    #df = pd.concat([pd.json_normalize(json.loads(line.strip())) for line in open(file_path, 'r',encoding=encoding)], ignore_index=True)
    #df=pd.read_json(file_path, encoding=encoding)
    #df.head(2)
    with open(file_path, 'r',encoding=encoding) as file:
       data = json.load(file)
    # Normalize JSON data
    df = pd.json_normalize(data)
    return df
    #return df

# This Function Extracts The Domain Name From The Url String.
def extract_domain(url):
    """
    Extract the domain name from a given URL using a regular expression.

    Parameters:
    url (str): The URL string from which to extract the domain name.

    Returns:
    str: The extracted domain name if a match is found, otherwise an empty string.
    """
    # Search for the domain name in the URL using a regex pattern.
    match = re.search(r'https?://(?:www\.)?(?:[^./]+\.)?([^./]+\.[^./]+)', url)
    return match.group(1) if match else 'null'

# This Function Is Taking The Values In the Form Of List And Return Tuple After Performing Calculation.
def calculate_product_recommendation_percentage(values):
    """
    Calculate the percentages of 'true' and 'false' values in the 'reviewsdo_recommend' column.

    Parameters:
    List (pd.Series): A List of the Rating will Pass to this Function.
    Returns:
    tuple: A tuple with the 'Recommendation Yes Percentage' and 'Recommendation No Percentage' values.
    """

    if not values:
    # Return 0% for both percentages if the list is empty
        return '0%','0%'
    # Count the Values For True and False.
    count_true = sum(value.lower() == 'true' for value in values)
    count_false = sum(value.lower() == 'false' for value in values)
    total_count = len(values)

    # Calculating The Percentage of Data.
    percentage_true = f"{round((count_true / total_count) * 100)}%"
    percentage_false = f"{round((count_false / total_count) * 100)}%"

    return percentage_true, percentage_false

# This Function Is Accepting The List And Calculates The Average Rating On Data.
def calculate_average(ratings):
    """
    Calculate the average rating from a list of ratings.

    Parameters:
    ratings (list): List of numerical ratings.

    Returns:
    float: The average rating rounded to one decimal place. Returns 0 if the list is empty.
    """
    return round(sum(ratings) / len(ratings), 1) if ratings else 0

# This Function Finds The Average Ratings Per Domain And Returns The Updated Dict.
def update_average_ratings_per_domain(source_text_map):
    """
    Update the source_text_map with the average rating for each domain.

    Args:
        source_text_map (dict): A dictionary mapping source URL domains to their texts and ratings.

    Returns:
        dict: The updated source_text_map with average ratings included.
    """
    for domain in source_text_map:
        ratings = source_text_map[domain]['ratings']
        average_rating_per_domain = calculate_average(ratings)
        source_text_map[domain]['average_rating'] = average_rating_per_domain

    return source_text_map

#This Function Accepting the Unique List and  Extract The Unique Values From The Data.
def extract_unique_values(list_):
    """
    Extract unique values from a list while maintaining their original order.

    Parameters:
    reviews (list): List containing review texts.

    Returns:
    list: A list of unique review texts in their original order.
    """
    return list(OrderedDict.fromkeys(list_))

# Pre-compile regular expressions for efficiency.
URL_PATTERN = re.compile(r'http\S+')
NON_ALPHANUMERIC_PATTERN = re.compile(r'[^a-zA-Z\s]')
EXTRA_SPACES_PATTERN = re.compile(r'\s+')

#This Function Is Accepting Input As A Str And Provide Us A Clean Text.
def clean_text(text):
    """
    Clean the review text by unescaping HTML entities, removing URLs, non-alphanumeric characters,
    converting to lowercase, and stripping extra spaces including newlines and tabs.

    Parameters:
    text (str): The review text to be cleaned.

    Returns:
    str: The cleaned review text.
    """
    if not isinstance(text, str):
        return ''

    text = unescape(text)
    text = URL_PATTERN.sub(' ', text)
    text = NON_ALPHANUMERIC_PATTERN.sub(' ', text)
    text = text.lower()
    text = EXTRA_SPACES_PATTERN.sub(' ', text).strip()

    return text

# This Function Is Used To Clean Tags In the Data .
def clean_tags(text):
    """
    Clean the tags in the text by performing several preprocessing steps:
    - Convert to lowercase
    - Remove HTML tags
    - Remove URLs
    - Remove special characters and punctuation
    - Remove numbers
    - Remove extra spaces
    - Tokenize the text
    - Remove stopwords

    Parameters:
    text (str): The text containing tags to be cleaned.

    Returns:
    str: The cleaned text.
    """
    
    # Convert to lowercase
    text = text.lower()
    # Remove HTML tags
    text = re.sub(r'<.*?>', ' ', text)
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', ' ', text, flags=re.MULTILINE)
    # Remove special characters and punctuation
    text = re.sub(r'\W', ' ', text)
    # Remove numbers
    text = re.sub(r'\d+', ' ', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove stopwords
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(tokens)

# This Function Cleans The Username From The Data.
def clean_username(username):
    """
    Remove the username after the dot (.) in the 'username' field.
    If the username starts with "Review provided by" or "· Review provided by" followed by any domain,
    contains "★★★★★", "anonymous", or "customer", return an empty string.

    Parameters:
    username (str): The username string.

    Returns:
    str: The username string with the part after the dot removed or an empty string for certain cases.
    """
    # Define the regex patterns for the specific cases
    if re.match(r'^(Review provided by|· Review provided by) \S+\.com|★★★★★|anonymous$|NA', username, re.IGNORECASE):
        return "null"
    
    # Define the regex pattern to match the username and remove it
    pattern = r' ·.*'
    cleaned_username = re.sub(pattern, '', username)
    return cleaned_username


# This Function Is Accepting Input As A Str and Provide Us The Sentiment Of Text.
def get_sentiment(text):
    """
    Perform sentiment analysis on the cleaned text using VADER sentiment analysis.

    Parameters:
    text (str): The cleaned review text.

    Returns:
    str: The sentiment of the text ('positive', 'negative', or 'neutral').
    """
    score = analyzer.polarity_scores(text)['compound']
    return 'positive' if score > 0.05 else 'negative' if score < -0.05 else 'neutral'

# This Function Is Taking Most Common Tags In The Form Of List And Then Classify Into Positive and Negative After That It Return A List
def classify_sentiment_tags(most_common_tags):
    """
    Classify the sentiment of the most common tags.

    Parameters:
    most_common_tags (list): A list of the most common tags.

    Returns:
    tuple: Two lists - one for positive sentiment tags and one for negative sentiment tags.
    """
    # Classify the tags into categories.
    positive_tags = [tag for tag in most_common_tags if get_sentiment(tag) == 'positive']
    negative_tags = [tag for tag in most_common_tags if get_sentiment(tag) == 'negative']
    return positive_tags, negative_tags

# This Function Is Accepting A List Of Sentiments And Return The Percentage Of Sentiments.
def calculate_sentiment_percentages(sentiments):
    """
    Calculate the percentages of positive and negative sentiments.

    Parameters:
    sentiments (list): List of sentiment strings ('positive', 'negative', 'neutral').

    Returns:
    tuple: Two strings representing the positive and negative sentiment percentages.
    """
    if not sentiments:
        return '0%', '0%'

    positive_count = sentiments.count('positive')
    negative_count = sentiments.count('negative')
    total_count = len(sentiments)

    positive_percentage = f"{round((positive_count / total_count) * 100)}%"
    negative_percentage = f"{round((negative_count / total_count) * 100)}%"
    # Answer Is Return In Tuple.
    return positive_percentage, negative_percentage

# This Function Accepts Cleaned_text And Sentiments Of The Data And Seperate Out Positive And Negative Reviews.
'''
def separate_review(text, sentiment):
    """
    Classify the text into positive or negative review based on sentiment.

    Parameters:
    text (str): Cleaned review text.
    sentiment (str): Sentiment of the text ('positive', 'negative', 'neutral').

    Returns:
    dict: Dictionary with keys 'positive_review' and 'negative_review'.
    """
    if sentiment == 'positive':
        return {'positive_review': text, 'negative_review': 'There are currently no instances of favorable feedback recorded.'}
    elif sentiment == 'negative':
        return {'positive_review': 'There are currently no instances of favorable feedback recorded.', 'negative_review': text}
    else:
        return {'positive_review': 'There are currently no instances of favorable feedback recorded.', 'negative_review': 'There are currently no instances of favorable feedback recorded.'}

'''
# This Function Recieve A List Of Reviews And Return A Common Tags In The Data.
def finding_most_common_tags(reviews):
    """
    Preprocess a list of reviews and return the common tags.

    Parameters:
    reviews (list): A list of review texts.

    Returns:
    list: A list of the most common tags.
    """
    # Preprocess the reviews
    reviews_cleaned = [clean_tags(review) for review in reviews]
    # Flatten the list of lists
    all_words = [word for review in reviews_cleaned for word in review.split()]
    # Get frequency distribution
    freq_dist = FreqDist(all_words)
    # Filter out words that appear more than once
    most_common_tags = [(word, freq) for word, freq in freq_dist.items() if freq > 1]
    # Further this function reverse and provide the most common tags first 
    most_common_tags = sorted(most_common_tags, key=lambda x: x[1], reverse=True)
    # Extract just the words from the most common tags and Return the value 
    return [word for word, score in most_common_tags if len(word) > 2]

# This Function Separate Reviews Into Positive And Negative Sentiment And Provide Us A List.
def separate_reviews(cleaned_texts, sentiments):
    """
    Separate positive and negative reviews from cleaned texts based on sentiments.

    Parameters:
    cleaned_texts (list): List of cleaned review texts.
    sentiments (list): List of sentiments corresponding to the cleaned texts ('positive', 'negative', 'neutral').

    Returns:
    tuple: Two strings representing the concatenated positive and negative reviews.
    """
    # Separate positive and negative reviews
    positive_reviews = ' '.join(cleaned_texts[i] for i in range(len(cleaned_texts)) if sentiments[i] == 'positive')
    negative_reviews = ' '.join(cleaned_texts[i] for i in range(len(cleaned_texts)) if sentiments[i] == 'negative')

    # Handle cases where one type of review is absent
    if positive_reviews and not negative_reviews:
        negative_reviews = "At this time, there is a complete lack of any critical or adverse assessments."
    elif negative_reviews and not positive_reviews:
        positive_reviews = "There are currently no instances of favorable feedback recorded."
    elif not positive_reviews and not negative_reviews:
        positive_reviews = "There are currently no instances of favorable feedback recorded."
        negative_reviews = "At this time, there is a complete lack of any critical or adverse assessments."

    return positive_reviews, negative_reviews

#This Function Accepts The Positive Reviews And Negative Reviews As A Str and Provide Us Unique.
def remove_common_words(positive_reviews, negative_reviews):
    """
    Remove common words from positive and negative review strings and ensure accurate word clouds.

    Parameters:
    positive_reviews (str): String containing all positive reviews.
    negative_reviews (str): String containing all negative reviews.

    Returns:
    tuple: Two strings with common words removed, (positive_reviews, negative_reviews).
    """
    # Convert the strings to sets of words
    positive_words = set(positive_reviews.split())
    negative_words = set(negative_reviews.split())

    # Find and remove common words from both sets
    common_words = positive_words.intersection(negative_words)
    positive_words -= common_words
    negative_words -= common_words

    # Subtract negative words from positive words and vice versa
    positive_words -= negative_words
    negative_words -= positive_words

    # Convert sets back to strings
    positive_reviews = ' '.join(positive_words)
    negative_reviews = ' '.join(negative_words)

    return positive_reviews, negative_reviews

# This Function Extracts All Of The Required Data From The Reviews Column And Return The Required Tuple.
def extract_data_from_reviews(reviews):
    """
    Extract individual components from a list of review dictionaries and return them in a list of dictionaries.

    Parameters:
    reviews (list): List of review dictionaries.

    Returns:
    list: List of dictionaries with keys like: date, dateSeen, rating, text, title, source_url, tags, doRecommend.
    """
    # Initialize the list to store the extracted components
    texts, titles, do_recommend, average_ratings,extracted_reviews, source_text_map, review_tags, common_tags_values = [], [], [], [], [], {}, [], {"common_tags": [], "negative_sentiment_tags": [], "positive_sentiment_tags": []}

    try:
        # Iterate over each review in the reviews list
        for review in reviews:
            try:
                review_tags_data = {
                    'findingTags': review.get('text', 'null'),
                }
                # Extract data, assign 'Null' if the corresponding keys are not present in the review dictionary
                review_data = {
                    'merchant': extract_domain(review.get('sourceURLs', ['null'])[0]),
                    'date': review.get('date', 'null'),
                    'dateSeen': review.get('dateSeen', 'null'),
                    'rating': review.get('rating', 0),
                    'text': clean_text(review.get('text', 'null')),
                    'sentiment': get_sentiment(clean_text(review.get('text', 'null'))),
                    'title': clean_text(review.get('title', 'null')),
                    'doRecommend': review.get('doRecommend', 'null'),
                    'username': clean_username(review.get('username', 'null')),
                    'didPurchase': review.get('didPurchase', 'null'),
                }
                # Get positive and negative reviews
                #separated_reviews = separate_review(review_data['text'], review_data['sentiment'])
                #review_data.update(separated_reviews)
            except Exception:
                # In case of any exception, assign 'Null' to all fields
                review_data = {
                    'merchant': 'null',
                    'date': 'null',
                    'dateSeen': 'null',
                    'rating': 0,
                    'text': 'null',
                    'sentiment': 'null',
                    'title': 'null',
                    'doRecommend': 'null',
                    'username': 'null',
                    'didPurchase': 'null',
                    #'positive_review': 'There are currently no instances of favorable feedback recorded.',
                    #'negative_review': 'There are currently no instances of favorable feedback recorded.'

                }
                review_tags_data = {
                    'findingTags': 'null',
                }
            
            if 'merchant' in review_data and 'text' in review_data:
                source_Url_domain = review_data['merchant']
                ratings_of_cus=review_data['rating']
                text_clean=review_data['text']
                if source_Url_domain not in source_text_map:
                    source_text_map[source_Url_domain] = {'texts': [], 'ratings': []}
                source_text_map[source_Url_domain]['texts'].append(text_clean)
                source_text_map[source_Url_domain]['ratings'].append(ratings_of_cus)
               
            # Append the extracted review data to the list
            extracted_reviews.append(review_data)
            average_ratings.append(review_data['rating'])
            titles.append(review_data['title'])
            texts.append(review_data['text'])
            review_tags.append(review_tags_data['findingTags'])
            cleaned_texts = extract_unique_values(texts)
            cleaned_titles = extract_unique_values(titles)
            do_recommend.append(review_data['doRecommend'])

        most_common_tags_data = finding_most_common_tags(review_tags)
        positive_tags, negative_tags = classify_sentiment_tags(most_common_tags_data)
        common_tags_values["common_tags"].extend(most_common_tags_data)
        common_tags_values["positive_sentiment_tags"].extend(positive_tags)
        common_tags_values["negative_sentiment_tags"].extend(negative_tags)
        sentiments = [get_sentiment(text) for text in cleaned_texts]
        positive_sentiment_percentage, negative_sentiment_percentage = calculate_sentiment_percentages(sentiments)
        recommendation_yes_percentage, recommendation_no_percentage = calculate_product_recommendation_percentage(do_recommend)
        total_ratings = calculate_average(average_ratings)
        source_text_map=update_average_ratings_per_domain(source_text_map)
        source_domains_list_=list(source_text_map.keys())
        positive_reviews, negative_reviews = separate_reviews(cleaned_texts, sentiments)
        overall_positive_reviews, overall_negative_reviews = remove_common_words(positive_reviews, negative_reviews)
        return total_ratings, cleaned_texts, cleaned_titles, positive_sentiment_percentage, negative_sentiment_percentage, recommendation_yes_percentage, recommendation_no_percentage, source_domains_list_, source_text_map, common_tags_values, extracted_reviews, overall_positive_reviews, overall_negative_reviews

    except Exception as e:
        # In case of a major exception, return a list with a single dictionary assigning 'Null' to all fields
        return 0, [], [],"0%","0%","0%","0%", [], {}, {}, [{
            'merchant': 'null',
            'date': 'null',
            'dateSeen': 'null',
            'rating': 0,
            'text': 'null',
            'sentiment': 'null',
            'title': 'null',
            'doRecommend': 'null',
            'username': 'null',
            'didPurchase': 'null',
            #'positive_review': 'There are currently no instances of favorable feedback recorded.',
            #'negative_review': 'There are currently no instances of favorable feedback recorded.'
        }],'There are currently no instances of favorable feedback recorded', 'At this time, there is a complete lack of any critical or adverse assessments'
    
# This Function Is Calling extract_data_from_reviews Sub Function To Process The Review Colum  To Extract Feature And
# Assign Back Values To DataFrame After That This DataFrame Converts Into Json Format To Store At The Exact Location.
# We Will Also Add Exception Handling Techniques In This Function
def assign_reviews_data_and_convert_into_json(input_file_path,output_file_path,reviews='reviews', orient='records', lines=True):
    """
    Apply the extraction function to each row in the DataFrame, assign the extracted data to new columns,
    and convert the DataFrame into a JSON file.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the reviews.
    extract_func (function): The function to extract data from the reviews column.
    json_file_path (str): The file path where the JSON file will be saved.
    reviews_col (str): The name of the column containing the reviews. Default is 'reviews'.
    orient (str): Indication of expected JSON string format. Default is 'records'.
    lines (bool): Whether to write the JSON file as a JSON object per line. Default is True.

    Returns:
    None

    """
    try:

      # If The Input File Not Found.
      if not os.path.isfile(input_file_path):
            raise FileNotFoundError(f"The input file path '{input_file_path}' does not exist.")

      # Check the Output Path Exists.
      output_dir = os.path.dirname(output_file_path)
      if output_dir and not os.path.exists(output_dir):
            raise FileNotFoundError(f"The directory for the output file path '{output_file_path}' does not exist.")

      # Load the JSON data from the file
      Reviews_DataFrame = load_json_to_df(input_file_path)
      
      # Check The DataFrame Is Empty Or Not
      if Reviews_DataFrame.empty:
          raise ValueError("Loaded DataFrame is empty. Please check the input file and its contents.")

      # Check if the specified reviews column exists in the DataFrame
      if reviews not in Reviews_DataFrame.columns:
          raise ValueError(f"The specified reviews column '{reviews}' does not exist in the DataFrame.")

      # Apply the extraction function to each row in the DataFrame
      extracted_data = Reviews_DataFrame[reviews].apply(extract_data_from_reviews)
      Reviews_DataFrame["overall_average_rating"], Reviews_DataFrame['review_texts'], Reviews_DataFrame['review_titles'], Reviews_DataFrame["overall_positive_sentiment_percentage"], Reviews_DataFrame["overall_negative_sentiment_percentage"], Reviews_DataFrame["product_recommendation_yes_percentage"], Reviews_DataFrame["product_recommendation_no_percentage"], Reviews_DataFrame["source_domains"], Reviews_DataFrame["ratings_text_domain_sources"], Reviews_DataFrame["review_tags"], Reviews_DataFrame["reviews"], Reviews_DataFrame["overall_positive_reviews"], Reviews_DataFrame["overall_negative_reviews"]=zip(*extracted_data)
      Reviews_DataFrame= Reviews_DataFrame[["ean", "ean13", "gtins", "upca", "asins", "overall_average_rating", "source_domains", "overall_positive_sentiment_percentage", "overall_negative_sentiment_percentage", "product_recommendation_yes_percentage", "product_recommendation_no_percentage", "review_tags", "review_texts", "review_titles", "ratings_text_domain_sources", "reviews", "overall_positive_reviews", "overall_negative_reviews"]]
      # Assign extracted data to DataFrame columns
      # Convert the DataFrame to JSON
      json_data = Reviews_DataFrame.to_json(orient=orient, lines=lines)
      # Write the JSON data to a file
      with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)

    # Handles the case when the input file path does not exist
    except FileNotFoundError as fnf_error:
      print(f"FileNotFoundError: {fnf_error}")

    # Handles invalid data formats and writes an empty JSON to the output file
    except ValueError as ve:
      with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write('{}')

    # Handles OS-related errors such as issues with file paths or permissions
    except OSError as os_error:
      print(f"OSError: {os_error}")

    # Handles any other unexpected exceptions and writes an empty JSON to the output file.
    except Exception as e:
      # If the Exception Occurs It Will Return The Empty Json
      with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write('{}')

# Commenting This
#if __name__ == "__main__":
    #assign_reviews_data_and_convert_into_json(input_file_path=r"air purifier\Extracted_info_reviews\0031262098467.json",output_file_path=r"air purifier\Extracted_info_reviews\0031262098467.json")