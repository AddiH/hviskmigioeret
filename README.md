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

### Manual labor
Unfortunately with the time constraints of this exam, it was not possible to fully automate the process of pulling videos and transcripts from folketingets website. This means that you will have to do some manual labor to get the data.
#### Choose and download videos
You will need to download the videos you want to use. Folketinget publishes all their meetings on their website https://www.ft.dk/da/aktuelt/tv-fra-folketinget/tidligere-moeder
Be aware that it can take a couple of days before the transcripts are available.
Download the files and save them in data/raw_videos. Give them a sensible name, I have chosen the number of the meeting. The name should correspond with the name in the urls.csv file.
#### Create urls.csv
You will need to manually create the file data/urls.csv. This file should contain
nr, url, min, sec
    The nr should correspond with the name of the video file. 
    The url should be the url to the video on folketingets website. 
    The min and sec should be the time in the video where the FIRST speaker starts speaking. **This is NOT speaker 0!** This is the biggest hassle with this dataset. The first part of the video is not transcibed, as it is  technically not a speach, but just the formand of the folketinget opening the meeting, by reading the agenda. Pay a lot of attention to this part. You might need to return here and fiddle with the numbers, once you realise the videaos have been sliced wrong.
#### Create politicians.csv
If you are using this repository around the time it was created (january 2024) you can omit this step, as the politicians within the folketing most likely hasn't changed. If you are making a new one, just make sure it has a gender and name column. I pulled the data from wikipedia, which is why there are additional columns. https://da.wikipedia.org/wiki/Folketingsmedlemmer_valgt_i_2022 


## Purpose of the scripts in /src
**01_transcripts.py**
-> IN 
    -> data/urls.csv            List of urls to the transcripts
<- OUT 
    <- transcripts/file.csv     Csv file with transcript for each URL

Downloads the transcripts from folketingets website. The transcripts contain timestamps as well as the name of the speaker
