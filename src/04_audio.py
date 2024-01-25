import os
import sys
import torchaudio
import torchaudio.transforms as T
import torch
from moviepy.editor import VideoFileClip
from tqdm import tqdm
sys.path.append(os.path.join('utils'))
from audio_preprocess import *

video_paths = folder_walker('data/politicians')
for path in video_paths:
    audio_save_path = path.replace('politicians', 'audio/raw')
    audio_save_path = audio_save_path[:-27] + '_' + audio_save_path[-26:-4] + '.wav'

    # Extract audio from trimmed video
    extract_audio_from_video(path, audio_save_path)

audio_paths = folder_walker('data/audio/raw')
for path in audio_paths:
    audio_save_path = path.replace('audio/raw', 'audio/resampled')
    resample_audio(path, audio_save_path)