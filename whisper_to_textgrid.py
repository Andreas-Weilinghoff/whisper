##########################################################################################################################
# This python script is designed to implement OpenAI Whisper on a particular sound file on your machine. The script 
# transforms the output and saves it into a .TextGrid file.
#
# This script is distributed under the GNU General Public License.
# Copyright 22/01/2023 by Andreas Weilinghoff.
# You may use/modify this script as you wish. It would just be nice if you cite me:
# Weilinghoff, A. (2023): whisper_to_textgrid+eaf.py (Version 1.0) [Source code]. https://www.andreas-weilinghoff.com/#code
##########################################################################################################################

### Import dependencies
import whisper
import ffmpeg

### Specify directory,file,extension
DIRECTORY = "C:\\Users\\User\\Desktop\\Whisper\\"
FILE_NAME = "testfile"
FILE_EXTENSION = ".wav"
# Specify whisper model, (medium is best for English, but takes longest; the strongest model for any language is "large-v2")
WHISPER_MODEL = "medium"

INPUT_FILE = DIRECTORY + FILE_NAME + FILE_EXTENSION
OUTPUT_FILE = str(INPUT_FILE).replace(FILE_EXTENSION,'.TextGrid')

### Get duration of audiofile to overwrite whisper's weird sound chunking at the end
endtime = ffmpeg.probe(INPUT_FILE)["format"]["duration"]

### Build TextGrid helper functions
def textgrid_header(endtime, interval_total):
    return f'File type = "ooTextFile"\n' \
           f'Object class = "TextGrid"\n\n' \
           f'xmin = 0\n' \
           f'xmax = {endtime}\n' \
           f'tiers? <exists>\n' \
           f'size = 1\n' \
           f'item []:\n' \
           f'\titem [1]:\n' \
           f'\t\tclass = "IntervalTier"\n' \
           f'\t\tname = "whisper"\n' \
           f'\t\txmin = 0\n' \
           f'\t\txmax = {endtime}\n' \
           f'\t\tintervals: size = {str(interval_total)}'

def textgrid_item(xmin, xmax, text, interval_number):
    return f'\t\tintervals [{interval_number}]:\n' \
           f'\t\t\txmin = {xmin}\n' \
           f'\t\t\txmax = {xmax}\n' \
           f'\t\t\ttext = \"{text.strip()}\"'

### Specify language and run whisper
model = whisper.load_model(WHISPER_MODEL)
result = whisper.transcribe(model, INPUT_FILE, language = "en")

### Build TextGrid
intervals = []
for idx, segment in enumerate(result["segments"]):
    xmin = segment["start"]
    xmax = segment["end"]
    text = segment["text"]
    if idx == len(result["segments"])-1:
        xmax = endtime

    intervals.append(textgrid_item(xmin, xmax, text, idx+1))

interval_total = len(result["segments"])
content = [textgrid_header(endtime, interval_total)] + intervals
content = '\n'.join(content)

### Write Textgrid
with open(OUTPUT_FILE, "w", encoding = "utf-8") as f:
    f.write(content)