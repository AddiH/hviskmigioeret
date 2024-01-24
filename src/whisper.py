import os
import sys
from tqdm import tqdm
import torchaudio
import pandas as pd
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import argparse
sys.path.append(os.path.join('utils'))
from audio_preprocess import folder_walker

def input_parse():
    parser = argparse.ArgumentParser() # initialise parser
    parser.add_argument('--model_name', type=str, default='whisper-tiny') # add arguments
    args = parser.parse_args() # parse the arguments from command line
    return args # get the variables

def main(model_name):

    # set up paths
    load_model = 'openai/' + model_name
    save_path_model = 'models/' + model_name
    full_save_path_model = '../data/' + save_path_model
    if not os.path.exists(full_save_path_model): # check that the save folder exists
        os.makedirs(full_save_path_model) # if not, create it
    paths = folder_walker('../data/audio/resampled') # the audio files to be transcribed

    # load model and processor
    processor = WhisperProcessor.from_pretrained(load_model)
    model = WhisperForConditionalGeneration.from_pretrained(load_model)
    model.config.forced_decoder_ids = None

    # TRANCRIBE
    for path in tqdm(paths):
        # create save path by replacing from the original path
        save_path = path.replace('audio/resampled', save_path_model)
        save_path = save_path.replace('.wav', '.txt')

        # if the path already exists, skip - (that way, if the script is interrupted, it can be restarted)
        if os.path.exists(save_path):
            continue
        
        waveform, sample_rate = torchaudio.load(path) # load in audio
        waveform_np = waveform.squeeze().numpy() # convert to numpy array
        input_features = processor(waveform_np, sampling_rate=sample_rate, return_tensors="pt").input_features # load data into processor
        predicted_ids = model.generate(input_features) # generate token ids from the model
        result = processor.batch_decode(predicted_ids, skip_special_tokens=True) # decode token ids to text (remove special tokens)

        # save the string to a file
        with open(save_path, 'w') as f:
            f.write(result[0])

    # CLEAN UP - delete the single files and save the data as a csv
    paths = folder_walker(full_save_path_model) # get the paths to the .txt files
    data = [] # Initialize a list to store the data
    # Loop through each file path
    for path in paths:
        with open(path, 'r', encoding='utf-8') as file: # Read the content of the file
            content = file.read()
            variable_path = path.replace(full_save_path_model + '/', '') # remove the path to the folder
            variable_path = variable_path[:-4] # remove the .txt extension
            data.append([content, variable_path]) # Append both the content and the file path to the data list

    df = pd.DataFrame(data, columns=[model_name, 'file']) # Create a DataFrame with the data
    df.to_csv('../data/models/' + model_name + '.csv', index=False) # Save the DataFrame as a CSV file
    
    for path in paths:
        os.remove(path) # Delete all the .txt files that only held a single string
    os.rmdir(full_save_path_model) # Delete the folder that held the .txt files
    return None

if __name__ == '__main__': # if the script is called from the command line
    args = input_parse() # get the variables
    main(args.model_name) # run the main function