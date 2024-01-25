import sys
import os
import pandas as pd
import glob
from moviepy.editor import VideoFileClip
from tqdm import tqdm
sys.path.append(os.path.join('utils'))
from slice_videos import *

# load in sample clips
sample_clips = pd.read_csv('data/sample_clips.csv', delimiter = ';')

# create a folder within data/raw_videos/politicians/ for each politician
for politician in sample_clips['name'].unique():
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