import os
from pydub import AudioSegment
from openai import OpenAI

# Initialize OpenAI API key
client = OpenAI(api_key=os.environ.get('OPENAI_KEY'))

def split_mp3(file_path, chunk_length_ms=60000):
    audio = AudioSegment.from_mp3(file_path)
    chunks = [audio[i:i+chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    for j, chunk in enumerate(chunks):
        chunk.export(f"{file_path.rsplit('.', 1)[0]}_chunk{j}.mp3", format="mp3")

def transcribe_mp3_to_text(mp3_file_path):
    with open(mp3_file_path, 'rb') as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return response.text

def main():
    # Get all mp3 files in the current directory
    mp3_files = [f for f in os.listdir('.') if f.endswith('.mp3')]

    for mp3_file in mp3_files:
        file_size = os.path.getsize(mp3_file)
        if file_size > 26214400:  # 25 MB
            split_mp3(mp3_file)
            chunk_files = [f for f in os.listdir('.') if f.startswith(mp3_file.rsplit('.', 1)[0]) and f.endswith('.mp3')]
            for chunk_file in chunk_files:
                text = transcribe_mp3_to_text(chunk_file)
                txt_file = chunk_file.rsplit('.', 1)[0] + '.txt'
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Transcribed {chunk_file} to {txt_file}")
        else:
            text = transcribe_mp3_to_text(mp3_file)
            txt_file = mp3_file.rsplit('.', 1)[0] + '.txt'
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Transcribed {mp3_file} to {txt_file}")

if __name__ == '__main__':
    main()