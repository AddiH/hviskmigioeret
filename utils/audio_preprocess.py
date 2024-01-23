import os
import sys
import torchaudio
import torchaudio.transforms as T
import torch
from moviepy.editor import VideoFileClip
from tqdm import tqdm

def extract_audio_from_video(video_file_path, audio_file_path):
    video = VideoFileClip(video_file_path)
    video.audio.write_audiofile(audio_file_path, codec='pcm_s16le')

# walk folder to find all paths within
def folder_walker(folder):
    paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            # is file does not start with a .
            if not file.startswith('.'):
                # append to list
                paths.append(os.path.join(root, file))
    return paths

def resample_audio(load_path, save_path):
    waveform, sample_rate = torchaudio.load(load_path) # load in audio
    waveform_mono = torch.mean(waveform, dim=0, keepdim=True) # Convert stereo audio to mono by averaging the two channels
    resampler = T.Resample(orig_freq=sample_rate, new_freq=16000) # Fix the sample rate
    waveform_resampled = resampler(waveform_mono)
    torchaudio.save(save_path, waveform_resampled, 16000) # save the audio