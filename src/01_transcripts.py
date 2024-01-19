import sys
import os
import pandas as pd # dataframes
import requests # downloading webpages
from time import sleep # pausing the loop
from random import randint # random number generator
from tqdm import tqdm # progress bar
sys.path.append(os.path.join('utils'))
from webscrape import *

# load csv files
df = pd.read_csv('data/urls.csv')
politicians = pd.read_csv('data/politicians.csv') # for removing titles

# loop over rows in df
for index, row in tqdm(df.iterrows()):
    # get values from row
    nr = row['nr']
    url = row['url']
    min = row['min']
    sec = row['sec']

    req = requests.get(url) # download webpage
    sleep(randint(1,5)) # pause loop for 1-5 seconds

    transcripts = extract_transcript(req) # extract transcript
    durations = extract_duration(req) # extract duration
    start_time = min * 60 + sec # timestamp of first (not 0!) speaker
    timestamps = get_timestamps(durations, start_time) # get timestamps
    df = pd.merge(transcripts, timestamps, on='ID') # merge dataframes
    df = df.drop(columns=['ID']) # drop ID column
    df['video_id'] = nr # add column with nr
    df = remove_titles(df, politicians) # remove titles from names

    save_name = f'data/transcripts/{nr}_transcript.csv'
    df.to_csv(save_name, index=False) # save dataframe