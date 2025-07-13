import os
import argparse
import uuid
from pysubparser import parser
from pydub import AudioSegment
import pyttsx3

def time_to_ms(time):
    return ((time.hour * 60 + time.minute) * 60 + time.second) * 1000 + time.microsecond / 1000

def generate_audio(path, rate=150, voice_idx=0):
    subtitles = parser.parse(path)
    
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    voices = engine.getProperty('voices')
    if voices and len(voices) > voice_idx:
        engine.setProperty('voice', voices[voice_idx].id)
    
    audio_sum = AudioSegment.empty()
    prev_time_ms = 0
    temp_id = uuid.uuid4().hex[:8]
    
    for i, subtitle in enumerate(subtitles):
        temp_file = f"temp_{temp_id}_{i}.wav"
        
        try:
            engine.save_to_file(subtitle.text, temp_file)
            engine.runAndWait()
            
            audio_segment = AudioSegment.from_wav(temp_file)
            start_time_ms = time_to_ms(subtitle.start)
            
            silence_ms = max(0, start_time_ms - prev_time_ms)
            audio_sum += AudioSegment.silent(silence_ms) + audio_segment
            prev_time_ms = start_time_ms + len(audio_segment)
            
        finally:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
    
    output_path = os.path.splitext(path)[0] + '.wav'
    audio_sum.export(output_path, format='wav')
    return output_path

if __name__ == "__main__":
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument("-p", "--path", help="subtitle file path", required=True)
  arg_parser.add_argument("-r", "--rate", help="speech rate(words per minute)", type=int, default=150)
  arg_parser.add_argument("-v", "--voice-idx", help="voice selection", type=int, default=0, choices=[0, 1])
  
  args = arg_parser.parse_args()
  
  generate_audio(path=args.path, rate=args.rate, voice_idx=args.voice_idx)    
