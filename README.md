# Danish Folketing Audio Transcription Toolkit

## Project Introduction

This repository is developed as part of an academic exam project focused on creating a new dataset of transcribed Danish audio and evaluating various Automatic Speech Recognition (ASR) models. It addresses a common challenge in ASR research: testing models on diverse and previously unseen data. Our solution involves collecting and transcribing audio from the Danish Parliament (Folketinget), a rich source of linguistic material that is, to our knowledge, not included in current ASR datasets.

### Objective

The primary goal is to document the process of assembling a unique dataset from the Folketinget's proceedings, and then evaluate two main ASR models. While the repository serves as a comprehensive guide to our approach, users should anticipate adjusting and tinkering with the code to tailor the dataset generation to their specific needs. This project underscores the importance of expanding the availability of Danish language resources for ASR and other language processing applications.

### Usage and Adaptation

Given the exploratory nature of this work, the code and methodologies presented are not flawless. Users are encouraged to view this repository as a starting point for developing their own Folketing audio dataset. Through community engagement and iterative refinement, we hope this toolkit will evolve, enhancing its utility and accuracy for future ASR research and development.


## Setup
This project was initially developed on an Apple M1 computer (python 3.11.6) and subsequently deployed on the Aarhus University's [Ucloud](cloud.sdu.dk) computing resources (python 3.10.12), which run on an Ubuntu 22.04.3 LTS machine. Due to differences in operating systems, Windows users might encounter issues related to file path conventions (e.g., the use of \ instead of /) among others. We recommend using Unix-like environments (Linux or macOS) for smoother operation.
To set up the needed environment on a Ucloud machine, you can run:

```bash
bash setup_env.sh
```

#### `setup_env.sh` Script Overview

The `setup_env.sh` script automates the setup process with the following steps:

1. Updates the package lists for upgrades and new package installations.
2. Installs `ffmpeg`, a crucial tool for processing video files.
3. Creates a Python virtual environment named `audio_env`.
4. Activates the virtual environment.
5. Upgrades `pip` to the latest version.
6. Installs the project's Python dependencies listed in `requirements.txt`.





## Manual Setup

Due to the constraints of this project's timeline, the process of obtaining videos and transcripts from the Folketinget's website couldn't be fully automated. As such, there are a few manual steps you'll need to undertake to prepare the data for use.

### Choose and Download Videos

1. **Select Videos**: Visit the [Folketinget's archive of past meetings](https://www.ft.dk/da/aktuelt/tv-fra-folketinget/tidligere-moeder) to choose the videos you wish to analyze. Note that transcripts may take a few days to become available after a meeting has occurred.
   
2. **Download and Organize Videos**: Download the selected video files and save them in the `data/raw_videos` directory. It's recommended to name the files using the meeting number for easy reference. Ensure the video file names correspond with the entries in the `urls.csv` file for consistency.

### Create `urls.csv`

Manually create a `urls.csv` file within the `data` directory. This file should follow the format:

```
nr, url, min, sec
```

- **nr**: Corresponds to the video file name.
- **url**: The direct URL to the video on the Folketinget website.
- **min** and **sec**: Indicate the timestamp (minutes and seconds) where the first speaker starts. Note that this refers to the first official speaker (speaker 1, NOT speaker 0 in the official transcript), not preliminary proceedings like the meeting's opening. Accurately determining this timestamp is crucial for correctly aligning the data; adjustments may be needed upon reviewing the cut videos.

### Create `politicians.csv`

This step may be optional if using the repository close to its creation date (January 2024), assuming no significant changes have occurred in the Folketinget's composition. If needed:

1. **Structure**: Ensure the file includes at least the `name` columns, which is used to clear the transcripts of titles. 
2. **Source Data**: Initial data was sourced from [Wikipedia's list of Folketingsmedlemmer elected in 2022](https://da.wikipedia.org/wiki/Folketingsmedlemmer_valgt_i_2022). Additional columns present are due to this origin, and not necessary for the project.


## Purpose of the scripts in /src
The functions written for this project are available in the utils folder. Below you can see the purpose of each of the scripts in the src/ folder. You can run them in succession to replicate our project, or you can pick and choose the ones you need for your own project. 
**01_transcripts.py**

Downloads the transcripts from Folketingets website. The transcripts contain timestamps as well as the name of the speaker, stripped of their title.
-> IN 
    -> data/urls.csv             List of urls to the videos
    -> data/politicians.csv      Names of politicians in Folketinget
<- OUT 
    <- transcripts/file.csv      Csv file with transcript for each URL

**02_take_sample.py**
Samples of speeches from the transcripts. Tailored to our project, taking 20 female and 20 male speakers, collecting>120 seconds of audio for each speaker.
-> IN
   -> data/transcripts/*.csv      The transcriptions collected in the previous step
   -> data/politicians.csv         List of politicians, used to get even gender spread
<- OUT
   <- 


This is what you can do to improve this project:
The videos are saved in a folder called politicians. We found this useful for the alignment process. That way we could confirm the speaker and get clues to how we might have to fiddle with the timestamps. You could easily incorporate a line of code that deletes the videos, thus freeing up space on your computer.

combine transcripts and audiofiles into one database
While it worked just fine for our purposes to have the transcripts and audiofiles in separate folders, it might be useful to combine them into one database. Again, this is something you can easily do with a few lines of code.



link til deling og rettigheder på FT hjemmeside



we've chosen to only transcribe a sample (20 women and 20 men speaking for <120 sec). You can easily take another sample and extract the soundfiles, or even transcribe everything, by giving 03 another sample.

Perhaps it is better to first pull out sound? Then clip? Could sound be downloaded directly. Important to note that this was developed for our exam, there is probably a lot you can do to make it work better for your project.
