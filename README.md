# Danish Folketing Audio Transcription Toolkit

## Project Introduction

This repository is developed as part of an academic exam project focused on creating a new dataset of transcribed Danish audio and evaluating various Automatic Speech Recognition (ASR) models. It addresses a common challenge in ASR research: testing models on diverse and previously unseen data. Our solution involves collecting and transcribing audio from the Danish Parliament (Folketinget), a rich source of linguistic material that is, to our knowledge, not included in current ASR datasets. [If you choose to use any of the code in this repository, please ensure it is not in conflict with the license provided by Folketinget](https://www.ft.dk/da/aktuelt/tv-fra-folketinget/deling-og-rettigheder)


### Objective

The primary goal is to document the process of assembling a unique dataset from the Folketinget's proceedings, and then evaluate two main ASR models. While the repository serves as a comprehensive guide to our approach, users should anticipate adjusting and tinkering with the code to tailor the dataset generation to their specific needs. This project underscores the importance of expanding the availability of Danish language resources for ASR and other language processing applications.


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





### Manual Setup

Due to the constraints of this project's timeline, the process of obtaining videos and transcripts from the Folketinget's website couldn't be fully automated. As such, there are a few manual steps you'll need to undertake to prepare the data for use.

#### Choose and Download Videos

1. **Select Videos**: Visit the [Folketinget's archive of past meetings](https://www.ft.dk/da/aktuelt/tv-fra-folketinget/tidligere-moeder) to choose the videos you wish to analyze. Note that transcripts may take a few days to become available after a meeting has occurred.
   
2. **Download and Organize Videos**: Download the selected video files and save them in the `data/raw_videos` directory. It's recommended to name the files using the meeting number for easy reference. Ensure the video file names correspond with the entries in the `urls.csv` file for consistency.

#### Create `urls.csv`

Manually create a `urls.csv` file within the `data` directory. This file should follow the format:

```
nr, url, min, sec
```

- **nr**: Corresponds to the video file name.
- **url**: The direct URL to the video on the Folketinget website.
- **min** and **sec**: Indicate the timestamp (minutes and seconds) where the first speaker starts. Note that this refers to the first official speaker (speaker 1, NOT speaker 0 in the official transcript), not preliminary proceedings like the meeting's opening. Accurately determining this timestamp is crucial for correctly aligning the data; adjustments may be needed upon reviewing the cut videos.

#### Create `politicians.csv`

This step may be optional if using the repository close to its creation date (January 2024), assuming no significant changes have occurred in the Folketinget's composition. If needed:

1. **Structure**: Ensure the file includes at least the `name` columns, which is used to clear the transcripts of titles. 
2. **Source Data**: Initial data was sourced from [Wikipedia's list of Folketingsmedlemmer elected in 2022](https://da.wikipedia.org/wiki/Folketingsmedlemmer_valgt_i_2022). Additional columns present are due to this origin, and not necessary for the project.


## Purpose of the scripts in /src
The functions written for this project are available in the utils folder. Below you can see the purpose of each of the scripts in the src/ folder. You can run them in succession to replicate our project, or you can pick and choose the ones you need for your own project. 


#### Overview of Scripts in `/src`
The `/src` folder contains scripts essential for replicating our project or for use in similar projects. Here's a breakdown:

| Script               | Description | Input | Output |
|----------------------|-------------|-------|--------|
| `01_transcripts.py`  | Downloads transcripts from Folketingets website, removing speaker titles. | `data/urls.csv` (URLs), `data/politicians.csv` (Politician names) | `transcripts/file.csv` (CSV of transcripts) |
| `02_take_sample.py`  | Samples speeches, aiming for gender balance and sufficient audio length. | `data/transcripts/*.csv` (Transcripts), `data/politicians.csv` (Politician names) | `data/sample_clips.csv` (Subset of transcripts) |
| `03_slice_videos.py` | Cuts videos based on timestamps, sorting them by speaker names. | `data/sample_clips.csv` (Transcripts subset) | `data/politicians/` (Folder with video clips) |
| `04_audio.py`        | Extracts and processes audio from video clips. | `data/politicians/` (Video clips) | `data/audio` (Processed audio in .wav) |
| `05_whisper.py` and `06_hviske.py` | Transcribes audio using a chosen model, saving interim results for efficiency. | `data/audio/resampled/*` (Resampled audio clips) | `data/models/` (Transcription DataFrame and audio file names) |


To run the `whisper.py` script with a specific model, use the `--model_name` flag in the command line. This allows you to specify which model the script should use for transcription. If no model is specified, the default model used is `whisper-tiny`. 

#### Example Command
```bash
python whisper.py --model_name whisper-medium
```
- The model name should match one of the available models in the Whisper framework. Please refer to the Whisper documentation for a list of available models.


## Suggestions for Enhancing the Project

This section outlines potential improvements and alternative approaches that could enhance the functionality and efficiency of the project. These suggestions are based on our experiences and are intended to guide you in customizing the project to better suit your needs.

#### 1. Efficient Management of Video Files
- **Current Approach**: Videos are saved in a folder named `politicians`, which aids in the alignment process by allowing easy confirmation of the speaker.
- **Improvement Suggestion**: Implement a code snippet to automatically delete the video files after processing. This can help in freeing up storage space on your computer.

#### 2. Integrating Transcripts and Audio Files
- **Current Approach**: Transcripts and audio files are stored in separate folders.
- **Improvement Suggestion**: Combine these elements into a single database. This can be achieved with a few lines of code and may enhance data management and accessibility.

#### 3. Flexible Sampling and Transcription
- **Current Approach**: We transcribed a sample consisting of 20 women and 20 men, each speaking for less than 120 seconds.
- **Improvement Suggestion**: 
   - You can modify the sampling strategy to include a different set of speakers or a larger sample size.
   - Consider transcribing the entire dataset, which can be done by adjusting the input for `03_slice_videos.py`.

#### 4. Revisiting the Processing Sequence
- **Current Approach**: The project sequence involves pulling audio from video clips and then processing them.
- **Improvement Suggestion**: 
   - Explore the possibility of directly downloading or extracting sound from the source, which might streamline the process.
   - Consider reversing the order of clipping and extracting audio to see if it enhances efficiency.

#### Final Note
This project was developed specifically for our academic examination. While it served our purposes well, there is significant scope for customization and improvement to adapt it to different project requirements. We encourage users to experiment with these suggestions and find what works best for their unique objectives.

If you're unsure of whether you can use Folketingets data for your project, [you can have a look at the license here](https://www.ft.dk/da/aktuelt/tv-fra-folketinget/deling-og-rettigheder)
