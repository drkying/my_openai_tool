import os
from pydub import AudioSegment

def compress_audio(input_file, output_file, target_bitrate="64k"):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format="mp3", bitrate=target_bitrate)

def compress_all_mp3_in_directory(directory, target_bitrate="64k"):
    for filename in os.listdir(directory):
        if filename.endswith('.mp3'):
            input_file = os.path.join(directory, filename)
            output_file = os.path.join(directory, filename.rsplit('.', 1)[0] + '-zip.mp3')
            compress_audio(input_file, output_file, target_bitrate)
            print(f"Compressed {input_file} to {output_file}")

# 示例用法
directory = os.path.dirname(os.path.abspath(__file__))
compress_all_mp3_in_directory(directory)