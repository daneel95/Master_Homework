import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

# constants
TRAIN_DATA_FILE_PATH = "Lyrics-Genre-Train.csv"
TEST_DATA_FILE_PATH = "Lyrics-Genre-Test-GroundTruth.csv"
LYRICS_COLUMN = "Lyrics"
GENRE_COLUMN = "Genre"

# useful variables
output_mappings = {}


# Pentru ca vrem ca input doar versurile si ca output genul vom citi tot setul de date si vom arunca toate datele
# care nu ne sunt de folos.
def read_data(file_path):
    data = pd.read_csv(file_path)
    # return data[LYRICS_COLUMN], data[GENRE_COLUMN]
    return pd.read_csv(file_path)[[LYRICS_COLUMN, GENRE_COLUMN]]


def create_new_dataset(dataset):
    global output_mappings
    dataset[GENRE_COLUMN] = dataset[GENRE_COLUMN].map(output_mappings)
    return dataset


# Encoding labels with [0, number of labels] so we will have proper outputs
def label_encoding(train_data, test_data):
    possible_labels = train_data[GENRE_COLUMN].unique()
    global output_mappings
    output_mappings = {genre: index for index, genre in enumerate(possible_labels)}
    new_train_data = create_new_dataset(train_data)
    new_test_data = create_new_dataset(test_data)
    return new_train_data, new_test_data


def bag_of_words(train_data, test_data):
    vectorizer = CountVectorizer()
    data = np.concatenate((train_data[LYRICS_COLUMN].as_matrix(), test_data[LYRICS_COLUMN].as_matrix()), axis=0)
    bow_model = vectorizer.fit(data)
    bow = vectorizer.transform(data)
    print(bow)
    return bow


if __name__ == "__main__":
    # Read data
    train_data = read_data(TRAIN_DATA_FILE_PATH)
    test_data = read_data(TEST_DATA_FILE_PATH)
    # changel labeling from string to int
    train_data, test_data = label_encoding(train_data, test_data)

    # Feature extraction

    # Machine learning
