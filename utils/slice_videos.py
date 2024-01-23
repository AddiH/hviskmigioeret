import pandas as pd
import glob
from moviepy.editor import VideoFileClip

def load_all_csv_to_df(directory_path):
    # Create a pattern for glob to match all CSV files in the directory
    csv_pattern = f"{directory_path}/*.csv"
    
    # Use glob to get a list of CSV files in the directory
    csv_files = glob.glob(csv_pattern)
    
    # Read each CSV file into a DataFrame and store them in a list
    df_list = [pd.read_csv(file) for file in csv_files]

    # Concatenate all DataFrames in the list into a single DataFrame
    combined_df = pd.concat(df_list, ignore_index=True)

    return combined_df

def trim_video(video_file_path, start_time, end_time, trimmed_video_path):
    video = VideoFileClip(video_file_path).subclip(start_time, end_time)
    video.write_videofile(trimmed_video_path, codec="libx264", audio_codec="aac")


def gender_balanced_sample(politicians, all_transcripts, n):

    # get total duration of each speaker
    speakers_time = all_transcripts.groupby('name')['duration'].sum().reset_index()
    speakers_time.columns = ['name', 'cum_duration']

    # filter out speakers with less than 120 seconds of speaking time
    speakers_time = speakers_time[speakers_time['cum_duration'] > 120]

    # add a single column (gender) from politicians to speakers_time by joining on name
    speakers_time = speakers_time.merge(politicians[['name', 'gender']], on='name', how='left')

    # filter speakers_time to have one with males and one with females
    female = speakers_time[speakers_time['gender'] == 'f']
    female = female['name'] # keep only name column
    female = female.sample(n=n, random_state=1)  # 'random_state' for reproducibility

    male = speakers_time[speakers_time['gender'] == 'm']
    male = male['name'] # keep only name column
    male = male.sample(n=n, random_state=1)  # 'random_state' for reproducibility

    # combine male and female into one list
    politician_sample = pd.concat([female, male])
    # drop the index
    politician_sample = politician_sample.reset_index(drop=True)

    return politician_sample