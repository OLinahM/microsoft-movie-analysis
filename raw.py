from pprint import pprint
import operator
from itertools import groupby
import pandas as pd
# FILE_PATH = (Path(__file__).with_name("title.basics.csv")).absolute()

def load_datasets():
    """
    Load various data sets

    args: None
    return (dataframe): title_basics, title_ratings
    """

    title_basics = pd.read_csv("title.basics.csv")
    title_ratings = pd.read_csv("title.ratings.csv")

    return title_basics, title_ratings

def merge_datasets(dataframe_a, dataframe_b, common_column):
    """
    Merges provided dataframes and returns a common dataframe

    args (dataframes, string): dataframe_a, dataframe_b, common_column

    returns (dataframe): merged_dataframe
    """
    return pd.merge(dataframe_a, dataframe_b, on=common_column)


def remove_duplicates(dataframe, column):
    """
    Remove duplicates based on passed column

    args: dataframe, column
    """
    return dataframe.drop_duplicates(subset=column, keep="last")

def drop_empty_titles(dataframe):
    """
    args (dataframe): dataframe

    returns (dataframe): dataframe
    """

    return dataframe.dropna(subset=["genres"]) # inplace=True

def group_data_by_genre_and_start_year(data_list):
    """
    Group data based on genre

    args: (list): data_list

    return: (list of lists): grouped_data_list
    """
    print(data_list[:5])
    data_list = sorted(data_list, key=operator.itemgetter("start_year"), reverse=True)
    return [list(group_item[1]) for group_item in groupby(data_list, key=operator.itemgetter("start_year"))]

def group_data_by_year(data_list):
    """
    """

def process_data(grouped_data_list):
    """
    Process data

    return (list of dictionaries): processed_data_list

    Example Response:
    processed_data = [
        {"Year": "2012", "Genre":"War", "Votes": 200000, "AverageRating": 7},
        {"Year": "2013", "Genre":"War", "Votes": 200000, "AverageRating": 5},
        {"Year": "2014", "Genre":"Action", "Votes": 200100, "AverageRating": 7}
        ]
    """
    grouped_list = []
    
    for data_list in grouped_data_list:
        processed_data = []

        for key, data in groupby(data_list, key=operator.itemgetter("genres")):
            grouped_data = list(data)
            year = grouped_data[0].get("start_year")
            total_votes = sum(data.get("numvotes") for data in grouped_data)
            average_votes = total_votes / len(grouped_data)
            average_rating = sum(data.get("averagerating") for data in grouped_data) / len(grouped_data)
            dic = {"Year": year, "Genre": key, "Votes": total_votes,"AverageVotes":average_votes, "AverageRating": average_rating}
            processed_data.append(dic)
        lst = sorted(processed_data, key=operator.itemgetter("AverageVotes", "AverageRating"), reverse=True)
        grouped_list.append(lst[0])
    return grouped_list


title_basics, title_ratings = load_datasets()
df = merge_datasets(title_basics, title_ratings, "tconst")
df = remove_duplicates(df, "original_title")
df = drop_empty_titles(df)
data_list = df.to_dict("records")
grouped_data = group_data_by_genre_and_start_year(data_list)
grouped_data_list = process_data(grouped_data)
print(len(grouped_data_list))
print(grouped_data_list[len(grouped_data_list)-10:])


# 