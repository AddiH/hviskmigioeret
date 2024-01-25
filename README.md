# Hvisk mig i øret
Exam for NLP, Cognitive Science Masters

https://www.youtube.com/watch?v=L_R-9w-75YQ

https://youtu.be/K_S9Pso91qU?si=_Og0OCoQoZTHnzU4&t=833 


1) Have a huggingface account and token ready
2) Make sure you have access to https://huggingface.co/mhenrichsen/hviske (you must request access)


On the mac i am using, i need to install ffmpeg with brew. SO make sure you have brew also


Noter:
Hvordan fungerer den der WER egentligt?
Hvor mange timers video har vi brug for?
Hvilket udsnit af politikere?
Hvordan definerer vi seres dialekt (hvis det er det vi vil)?
Hvad vil vi egentligt?

## Setup
- try it on ucloud

- run setup env

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

1. **Structure**: Ensure the file includes at least `gender` and `name` columns.
2. **Source Data**: Initial data was sourced from [Wikipedia's list of Folketingsmedlemmer elected in 2022](https://da.wikipedia.org/wiki/Folketingsmedlemmer_valgt_i_2022). Additional columns present are due to this origin, and not necessary for the project.

(project developed on mac/tested on ucloud check your paths etc)

## Purpose of the scripts in /src
**01_transcripts.py**
-> IN 
    -> data/urls.csv            List of urls to the transcripts
<- OUT 
    <- transcripts/file.csv     Csv file with transcript for each URL

Downloads the transcripts from folketingets website. The transcripts contain timestamps as well as the name of the speaker



This is what you can do to improve this project:
The videos are saved in a folder called politicians. We found this useful for the alignment process. That way we could confirm the speaker and get clues to how we might have to fiddle with the timestamps. You could easily incorporate a line of code that deletes the videos, thus freeing up space on your computer.

combine transcripts and audiofiles into one database
While it worked just fine for our purposes to have the transcripts and audiofiles in separate folders, it might be useful to combine them into one database. Again, this is something you can easily do with a few lines of code.



link til deling og rettigheder på FT hjemmeside



we've chosen to only transcribe a sample (20 women and 20 men speaking for <120 sec). You can easily take another sample and extract the soundfiles, or even transcribe everything, by giving 03 another sample.

Perhaps it is better to first pull out sound? Then clip? Could sound be downloaded directly. Important to note that this was developed for our exam, there is probably a lot you can do to make it work better for your project.