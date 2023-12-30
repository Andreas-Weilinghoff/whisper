##########################################################################################################################
# This python script is designed to implement OpenAI Whisper on your machine. With this script, Whisper parses through a 
# directory and transcribes all sound files with a specific format (e.g. .wav) in that directory. The transcriptions are 
# saved as txt files. 
#
# This script is distributed under the GNU General Public License.
# Copyright 13/12/2023 by Andreas Weilinghoff.
# You may use/modify this script as you wish. It would just be nice if you cite me:
# Weilinghoff, A. (2023): whisper_to_txt_directory.py (Version 1.0) [Source code]. https://www.andreas-weilinghoff.com/#code
##########################################################################################################################

import os
import whisper
from tqdm import tqdm

# Define the folder where the sound files are located
root_folder = "C:\\Users\\"

# Set up Whisper client
print("Loading whisper model...")
MODEL = whisper.load_model("small")
print("Whisper model complete.")
INPUT_FORMAT =".mp3"
INPUT_LANGUAGE = "en"

# Get the number of sound files in the root folder and its sub-folders
print("Getting number of files to transcribe...")
num_files = sum(1 for dirpath, dirnames, filenames in os.walk(root_folder) for filename in filenames if filename.endswith(INPUT_FORMAT))
print("Number of files: ", num_files)

# Transcribe the wav files and display a progress bar
with tqdm(total=num_files, desc="Transcribing Files") as pbar:
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(INPUT_FORMAT):
                filepath = os.path.join(dirpath, filename)
                result = MODEL.transcribe(filepath, fp16=False, verbose=True, language = INPUT_LANGUAGE)
                transcription = result['text']
                # Write transcription to text file
                filename_no_ext = os.path.splitext(filename)[0]
                with open(os.path.join(dirpath, filename_no_ext + '_whisper.txt'), 'w') as f:
                    f.write(transcription)
                pbar.update(1)