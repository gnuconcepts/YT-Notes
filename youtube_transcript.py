from youtube_transcript_api import YouTubeTranscriptApi
import os
from datetime import datetime
import csv
import openai
import sys


if len(sys.argv) <= 1:
    default_value = input("No arguments provided. Enter a value: ")
    first_argument = default_value
else:
    first_argument = sys.argv[1]

print("First argument:", first_argument)


youtubeid = first_argument

#YouTubeTranscriptApi.get_transcript(video_id, proxies={"https": "https://user:pass@domain:port"})

#youtubeid ='OTLxMmrMyYo' #'bi1eFecrOYM' #'MlASBCp3Yuw'
#'TA_NCwJmhS4'#'BIOYt-lbsJs' #4JfQZsuxnJ8'#-LhLmKIytLE' #'CePcwlHmvJI' # 'uzM_nKDwwXo'  #'32TKFsox5Co' #'dCaAfUDEFyY' #'8beoStypxrM'

transcript_list = YouTubeTranscriptApi.list_transcripts(youtubeid) # 8beoStypxrM , ny4ZAzndQFQ

transcript = transcript = transcript_list.find_transcript(['en'])

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

def concatenate_text(json_data):
    concatenated_text = ' '.join(item['text'] for item in json_data)
    return concatenated_text


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()

def split_string_with_overlap(text, length, overlap):
    if not isinstance(text, str):
        raise ValueError("Input 'text' must be a string.")
    
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Input 'length' must be a positive integer.")
    
    if not isinstance(overlap, int) or overlap < 0 or overlap >= length:
        raise ValueError("Input 'overlap' must be a non-negative integer and smaller than 'length'.")
    
    result = []
    words = text.split()
    start_idx = 0
    
    while start_idx < len(words):
        current_chunk = " ".join(words[start_idx:start_idx + length])
        result.append(current_chunk)
        start_idx += length - overlap
    
    return result




def create_file_in_subdirectory(filename, content, subdirectoryname,timestamp):
    subdirectory = "working_dir_notes"
    
    
    # Create the subdirectory if it doesn't exist
    if not os.path.exists(subdirectory):
        os.makedirs(subdirectory)
    
    if not os.path.exists(subdirectory + "/" + subdirectoryname):
        os.makedirs(subdirectory + "/" + subdirectoryname)
    
    subdirectory = subdirectory + "/" + subdirectoryname

    # Add a datetime stamp to the filename

    filename_with_timestamp = f"{filename}_{timestamp}.txt"
    
    # Combine the subdirectory path and the filename
    file_path = os.path.join(subdirectory, filename_with_timestamp)
    
    # Create the file and write content to it
    with open(file_path, "a") as file:
        file.write(content)

    
    print(f"File '{filename_with_timestamp}' created in the subdirectory '{subdirectory}'.")

# Usage example


def find_value_by_key(csv_filename, key):
    '''
    Key,Value
    OPENAI_KEY, you OpenAI Key
    '''
    with open(csv_filename,encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row['Key'] == key:
                return row['Value'].strip()
    return None

openai.api_key =  find_value_by_key("c:\Keystore\Keys.txt", "OPENAI_KEY")

def call_gpt(prompt):
    msgs = [
        {"role": "system", "content": "You are a helpful assistant that writes out lists of notes from text. Only write out notes please don't add any additional commentary. All notes should be in the third person."},
        {"role": "user", "content": "Please take notes for the following text: " +prompt}
    ]

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=msgs
    )

    return response.choices[0].message.content.strip()






concatenated_text = concatenate_text(transcript.fetch())

create_file_in_subdirectory("transcript", concatenated_text,youtubeid,timestamp)


arrText = split_string_with_overlap(concatenated_text,500,0)
for s in arrText:
    ans = call_gpt(s)
    create_file_in_subdirectory("notes",ans,youtubeid,timestamp)

