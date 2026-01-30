import os
from gtts import gTTS
import uuid

def generate_voice_commentary(text, lang='en'):
    """
    Generates an MP3 file from text using gTTS and returns the filename.
    The file is saved in the static/audio directory.
    """
    try:
        if not text:
            return None
            
        static_audio_dir = os.path.join('static', 'audio')
        if not os.path.exists(static_audio_dir):
            os.makedirs(static_audio_dir)
            
        filename = f"commentary_{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(static_audio_dir, filename)
        
        tts = gTTS(text=text, lang=lang)
        tts.save(filepath)
        
        return filename
    except Exception as e:
        print(f"Error generating voice: {e}")
        return None

def cleanup_old_audio(max_files=10):
    """
    Cleans up old audio files in the static/audio directory.
    """
    try:
        static_audio_dir = os.path.join('static', 'audio')
        if not os.path.exists(static_audio_dir):
            return
            
        files = [os.path.join(static_audio_dir, f) for f in os.listdir(static_audio_dir) if f.endswith('.mp3')]
        if len(files) > max_files:
            # Sort by modification time
            files.sort(key=os.path.getmtime)
            for f in files[:-max_files]:
                os.remove(f)
    except Exception as e:
        print(f"Error cleaning up audio: {e}")
