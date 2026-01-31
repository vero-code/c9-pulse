import os
import asyncio
import edge_tts
import uuid
from typing import Optional, List

async def _generate_async(text: str, voice: str, filepath: str):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filepath)

def generate_voice_commentary(text: str, voice: str = 'en-US-GuyNeural') -> Optional[str]:
    """
    Generate an MP3 voice file from text using edge-tts.
    
    Args:
        text: The text to convert to speech.
        voice: Voice name for edge-tts (default is a male voice).
        
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
        
        # edge-tts is asynchronous, so we run it in a synchronous wrapper
        asyncio.run(_generate_async(text, voice, filepath))
        
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
