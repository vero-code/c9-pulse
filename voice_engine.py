import os
from gtts import gTTS
import uuid
from typing import Optional, List

def generate_voice_commentary(text: str, lang: str = 'en') -> Optional[str]:
    """
    Generate an MP3 voice file from text using gTTS.
    
    Args:
        text: The text to convert to speech.
        lang: Language code for TTS.
        
    Returns:
        The generated filename, or None if it fails.
    """
    try:
        if not text:
            return None
            
        static_audio_dir: str = os.path.join('static', 'audio')
        if not os.path.exists(static_audio_dir):
            os.makedirs(static_audio_dir)
            
        filename: str = f"commentary_{uuid.uuid4().hex}.mp3"
        filepath: str = os.path.join(static_audio_dir, filename)
        
        tts: gTTS = gTTS(text=text, lang=lang)
        tts.save(filepath)
        
        return filename
    except Exception as e:
        print(f"Error generating voice: {e}")
        return None

def cleanup_old_audio(max_files: int = 10) -> None:
    """
    Remove old audio files to save space.
    
    Args:
        max_files: Maximum number of files to keep.
    """
    try:
        static_audio_dir: str = os.path.join('static', 'audio')
        if not os.path.exists(static_audio_dir):
            return
            
        files: List[str] = [os.path.join(static_audio_dir, f) for f in os.listdir(static_audio_dir) if f.endswith('.mp3')]
        if len(files) > max_files:
            # Sort by modification time
            files.sort(key=os.path.getmtime)
            for f in files[:-max_files]:
                os.remove(f)
    except Exception as e:
        print(f"Error cleaning up audio: {e}")
