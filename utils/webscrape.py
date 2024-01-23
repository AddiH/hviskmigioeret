import requests # Downloading webpages
from bs4 import BeautifulSoup # Extracting data from html files
import pandas as pd
import re
from datetime import datetime
from pandas import DataFrame
from requests import Response

def extract_transcript(req: Response) -> pd.DataFrame:
    '''
    Extracts transcript data from a given Response object.

    This function parses the HTML content of a Response object to extract 
    names, texts, and IDs, and then structures this data into a pandas DataFrame. 
    It filters out any rows where the ID is 'N/A'.
    The first row is also dropped, as it hard to define when this speach starts.

    Parameters:
    - req (Response): The Response object obtained from a web request.

    Returns:
    - pd.DataFrame: A pandas DataFrame containing columns for 'name', 'text', and 'ID'.
    '''
        
    soup = BeautifulSoup(req.text, 'html.parser') # Parse the HTML as a string

    # Initialize lists to store the extracted data
    names = []
    texts = []
    numbers = []

    # Find all divs with class 'video-item-referat' - this is one speach
    for div in soup.find_all("div", class_="video-item-referat"):
        # Extract name and clean it
        name_div = div.find("div", class_="name")
        name = name_div.get_text(strip=True)
        name = re.sub(r'\([^)]*\)', '', name) # Remove everything within parentheses and parentheses themselves
        name = name.strip() # Remove whitespace at beginning and end

        # Extract texts from all <p> with class 'Tekst' and 'TekstIndryk' - this is the transcript
        text_elements = div.find_all("p", class_=["Tekst", "TekstIndryk"])
        combined_text = ' '.join(p.get_text(strip=True) for p in text_elements)

        # Extract number (from id of 'video-item-content') - this is and ID for the speach
        content_div = div.find("div", class_="video-item-content")
        number = content_div['id'].split('_')[-1] if content_div and 'id' in content_div.attrs else 'N/A'

        # Append to lists
        names.append(name)
        texts.append(combined_text)
        numbers.append(number)

    # Create DataFrame
    df = pd.DataFrame({
        'name': names,
        'text': texts,
        'ID': numbers
    })

    # Remove rows that contain 'N/A'
    df = df[df.ID != 'N/A']

    # Drop the first row
    df = df.drop(df.index[0])

    # Return DataFrame
    return df


def extract_duration(req):
    '''
    Extracts duration of speeches from a given Response object, skipping the last item.
    
    Parameters:
    - req (Response): The Response object obtained from a web request.

    Returns:
    - pd.DataFrame: A pandas DataFrame containing columns for 'duration', 'start_clock', and 'ID', excluding the last speech.
    '''

    soup = BeautifulSoup(req.text, 'html.parser')  # Parse the HTML as a string

    script_tag = soup.find('script', text=re.compile('SpeachItem'))  # Find the script tag containing the timestamps
    speach_items = re.findall(r'new SpeachItem\(.*\)', script_tag.string)  # Extract all instances of SpeachItem
    speach_items = [re.sub(r'new SpeachItem', '', item) for item in speach_items]  # Remove 'new SpeachItem'

    # Initialize lists for data collection
    id = []
    duration = []
    start_clock = []

    # Loop over speach_items, excluding the last one for duration calculation
    for index in range(len(speach_items) - 1):  # Stop before the last item
        # Get start clock for current and next speech
        current_start_clock = speach_items[index][19:27]
        next_start_clock = speach_items[index + 1][19:27]

        # Convert to datetime
        current_start_clock_datetime = datetime.strptime(current_start_clock, '%H:%M:%S')
        next_start_clock_datetime = datetime.strptime(next_start_clock, '%H:%M:%S')

        # Calculate the timedelta (difference) for duration
        seconds = (next_start_clock_datetime - current_start_clock_datetime).total_seconds()

        # Append duration and other details to lists
        duration.append(seconds)
        id.append(speach_items[index][58:-2])
        start_clock.append(current_start_clock)

    # Create DataFrame
    durations = pd.DataFrame({
        'duration': duration,
        'start_clock': start_clock,
        'ID': id
    })

    return durations


def old_extract_duration(req: Response) -> pd.DataFrame:
    '''
    Extracts duration of speaches from a given Response object.
    
    Parameters:
    - req (Response): The Response object obtained from a web request.

    Returns:
    - pd.DataFrame: A pandas DataFrame containing columns for 'duration' and 'ID'.
    '''

    soup = BeautifulSoup(req.text, 'html.parser') # Parse the HTML as a string

    script_tag = soup.find('script', text=re.compile('SpeachItem')) # Find the script tag containing the timestamps
    speach_items = re.findall(r'new SpeachItem\(.*\)', script_tag.string) # Extract all instances of SpeachItem
    speach_items = [re.sub(r'new SpeachItem', '', item) for item in speach_items] # Remove 'new SpeachItem'

    # loop over speach_items and extract the timestamps
    id = []
    duration = []
    start_clock = []
    end_clock = []

    for item in speach_items:
        # Get start and end clock
        speach_start_clock = item[19:27]
        speach_end_clock = item[41:49]

        # Convert to datetime
        speach_start_clock_datetime = datetime.strptime(speach_start_clock, '%H:%M:%S')
        speach_end_clock_datetime = datetime.strptime(speach_end_clock, '%H:%M:%S')

        # Calculate the timedelta (difference) (duration)
        seconds = (speach_end_clock_datetime - speach_start_clock_datetime).total_seconds()

        # Append duration and ID to lists
        duration.append(seconds)
        id.append(item[58:-2])
        start_clock.append(speach_start_clock)
        end_clock.append(speach_end_clock)

    # Create DataFrame
    durations = pd.DataFrame({
        'duration': duration,
        'start_clock': start_clock,
        'end_clock': end_clock,
        'ID': id
    })

    # Drop the first row
    durations = durations.iloc[1:]
    return durations

def to_hour_min_sec(seconds: int) -> str:
    """
    Converts seconds to hours, minutes, and seconds.

    Parameters:
    - seconds (int): The total number of seconds.

    Returns:
    - str: A string representation in the format "hours:minutes:seconds".
    
    Hours will be 0 if the total time is less than an hour.
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    sec = seconds % 60
    return f"{hours}:{minutes:02d}:{sec:02d}"


def get_timestamps(df, initial_start_time):
    '''
    Calculates the start and end timestamps for each row in a DataFrame.

    Parameters:
    - df (DataFrame): The DataFrame containing the 'duration' column.

    Returns:
    - DataFrame: A pandas DataFrame containing columns for 'start_sec' and 'end_sec'.
    '''
    
    # Calculate the cumulative sum of 'Duration' for the 'end_sec' column and add the initial start time
    df['end_sec'] = df['duration'].cumsum() + initial_start_time

    # Shift the 'end_sec' column to create the 'start_sec' column, and initialize the first value with the initial start time
    df['start_sec'] = df['end_sec'].shift(1).fillna(initial_start_time)

    # Convert 'start_sec' and 'end_sec' columns to integer if necessary
    df['start_sec'] = df['start_sec'].astype(int)
    df['end_sec'] = df['end_sec'].astype(int)

    # Apply the conversion to 'start_sec' and 'end_sec' and create new columns
    df['start_min'] = df['start_sec'].apply(to_hour_min_sec)
    df['end_min'] = df['end_sec'].apply(to_hour_min_sec)

    return df

def remove_titles(df_with_titles, df_names):
    # Create a set of unique words from df_names
    unique_name_words = set(" ".join(df_names['name']).split())

    # Define a function to keep only the words that are in unique_name_words
    def remove_unwanted_words(name):
        return ' '.join(word for word in name.split() if word in unique_name_words)

    # Apply the function to the 'name' column in df_with_titles
    df_with_titles['name'] = df_with_titles['name'].apply(remove_unwanted_words)

    # Create a set of valid full names from df_names
    valid_full_names = set(df_names['name'])

    # Filter rows in df_with_titles where the name is not in valid_full_names
    df_with_titles = df_with_titles[df_with_titles['name'].isin(valid_full_names)]

    return df_with_titles