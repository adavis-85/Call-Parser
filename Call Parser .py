#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import speech_recognition as speech_r
import time
from os import path
from pydub import AudioSegment
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence

# assign files
input_file = "17133_56_09_20_2022_15_08_52_304.mp3"
output_file = "result.wav"
path="result.wav"
# convert mp3 file to wav file
audio = AudioSegment.from_mp3(input_file)
audio.export(output_file, format="wav")

# create a speech recognition object
cog = speech_r.Recognizer()

def call_parser(path,tongue):
    
    structured_sentences=list()
    #Opening the audio file
    call_audio = AudioSegment.from_wav(path)  
    #Splits the audio into chunks to analyze with the minimum silence is
    ##1 second
    convo_breaks_split = split_on_silence(call_audio,
                              min_silence_len = 1000,
                              ##Setting the same average amptitude of the 
                              ##audio
                              silence_thresh = call_audio.dBFS-14,
                              keep_silence=1000,
                              )
   
    ##Create a folder in computer's repository
    folder_name = "audio_snippets"
    
    # create a directory to store the audio chunks
    ##choosing language for file.....................................
    ##spanish
    if tongue.lower() == "spanish":
        chosen="es-MX"
    ##english
    if tongue.lower() == "english":
        chosen="en-US"
     ##..............................................................   
    
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
        
    entire_conversation = ""
    #Each divided snippet is processed from the file
    for i, audiofile in enumerate(convo_breaks_split, start=1):
        ##Exporting the processed snippet into folder within folder
        filename = os.path.join(folder_name, f"snippet{i}.wav")
        audiofile.export(filename, format="wav")
        ##Picking out the snippet
        with speech_r.AudioFile(filename) as source:
            cog.adjust_for_ambient_noise(source, duration=0.5)
            audio_listened = cog.record(source)
            ##Converting the audio snippet to text
            try:
                text = cog.recognize_google(audio_listened,language=chosen)
                ##If something isn't able to be translated
            except speech_r.UnknownValueError as err:
                print("Can't translate/Possible noise/Pause:", str(err))
            else:
                text = f"{text.capitalize()}. "
                print(filename, ":", text)
                structured_sentences.append([filename,text])
                entire_conversation += text
    # return the text for all chunks detected
    return entire_conversation,structured_sentences

##Function call along with time for function to run
start=time.time()
conversation,full_convo=call_parser(path,"english")
end=time.time()
print("\nFull text:", conversation)

