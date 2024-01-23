import sys
import os
import pandas as pd
import glob
from moviepy.editor import VideoFileClip
from tqdm import tqdm
sys.path.append(os.path.join('utils'))
from slice_videos import *

# load csv files
politicians = pd.read_csv('data/politicians.csv')
directory_path = "data/transcripts"
all_transcripts = load_all_csv_to_df(directory_path)

# filter and remove speaches where duration is under 30
all_transcripts = all_transcripts[all_transcripts['duration'] > 30]
all_transcripts = all_transcripts[all_transcripts['duration'] < 200]

# get a sample of 20 politicians (gender balanced)
politician_sample = gender_balanced_sample(politicians, all_transcripts, 20)

# Initialize an empty DataFrame for the result
sample_clips = pd.DataFrame()

# sample <120 seconds of video for each politician
for politician in politician_sample:
    # Filter all_transcripts for the current politician
    politician_transcripts = all_transcripts[all_transcripts['name'] == politician]
    
    # Initialize a DataFrame for accumulating transcripts for the current politician
    accumulated_transcripts = pd.DataFrame()

    # Loop until the sum of duration exceeds 120 seconds
    while accumulated_transcripts.empty or accumulated_transcripts['duration'].sum() < 120:
        # Sample a random row
        random_row = politician_transcripts.sample(n=1)
        
        # If accumulated_transcripts is empty, directly append random_row
        if accumulated_transcripts.empty:
            accumulated_transcripts = pd.concat([accumulated_transcripts, random_row])
        else:
            # Create a boolean series to check if the row already exists in accumulated_transcripts
            exists = accumulated_transcripts.isin(random_row.to_dict(orient='list')).all(axis=1).any()

            # Check if the random row has already been added
            if not exists:
                # Append the random row to the accumulated_transcripts DataFrame
                accumulated_transcripts = pd.concat([accumulated_transcripts, random_row])

        # Check if the accumulated transcripts exceed the desired duration
        if accumulated_transcripts['duration'].sum() >= 120:
            break

    # Append the accumulated_transcripts for this politician to the result_df
    sample_clips = pd.concat([sample_clips, accumulated_transcripts])

#save the sample_clips to a csv, semi-colon separated, encoding
sample_clips.to_csv('data/sample_clips.csv', sep=';', encoding='utf-8', index=False)

# create a folder within data/raw_videos/politicians/ for each politician
for politician in politician_sample:
    os.makedirs(f"data/politicians/{politician}", exist_ok=True)

# slice and save each video
for index, row in tqdm(sample_clips.iterrows()):
    # Replace colon in 'start_min' with an underscore for the filename
    start_min_formatted = row['start_min'].replace(':', '-')

    # Create a filename for saving the trimmed video
    save_path = f"data/politicians/{row['name']}/video_{row['video_id']}_start_{start_min_formatted}.mp4"

    # if the file already exists, skip it
    if os.path.exists(save_path):
        continue

    #create a path to the original video
    video_file_path = f"data/raw_videos/{row['video_id']}.mp4"

    #trim the video
    trim_video(video_file_path, row['start_sec'], row['end_sec'], save_path)