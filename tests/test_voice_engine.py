import os
import pytest
from voice_engine import generate_voice_commentary, cleanup_old_audio

@pytest.fixture
def mock_audio_dir(tmp_path, monkeypatch):
    audio_dir = tmp_path / "static" / "audio"
    audio_dir.mkdir(parents=True)
    monkeypatch.setattr("os.path.join", lambda *args: str(os.path.join(*args)).replace("static\\audio", str(audio_dir)) if "static" in args and "audio" in args else os.path.join(*args))
    # That join override is tricky. Let's try simpler:
    monkeypatch.setattr("voice_engine.os.path.exists", lambda path: True if str(audio_dir) in path else os.path.exists(path))
    # Actually, it might be better to just mock the directory path in the module if possible, 
    # but voice_engine uses hardcoded 'static/audio'.
    # Let's just mock os.makedirs and gTTS.save
    return audio_dir

def test_generate_voice_commentary(mocker, tmp_path):
    mock_gtts = mocker.patch("voice_engine.gTTS")
    mock_makedirs = mocker.patch("voice_engine.os.makedirs")
    mock_exists = mocker.patch("voice_engine.os.path.exists", return_value=True)
    
    filename = generate_voice_commentary("Hello world")
    
    assert filename.startswith("commentary_")
    assert filename.endswith(".mp3")
    mock_gtts.assert_called_once_with(text="Hello world", lang='en')
    mock_gtts.return_value.save.assert_called_once()

def test_generate_voice_commentary_empty():
    assert generate_voice_commentary("") is None

def test_cleanup_old_audio(mocker, tmp_path):
    audio_dir = tmp_path / "audio"
    audio_dir.mkdir()
    
    # Create 5 dummy mp3 files
    for i in range(5):
        f = audio_dir / f"test_{i}.mp3"
        f.write_text("dummy")
        # Ensure different mtimes
        os.utime(f, (1000 + i, 1000 + i))
        
    mocker.patch("voice_engine.os.path.exists", return_value=True)
    mocker.patch("voice_engine.os.listdir", return_value=[f"test_{i}.mp3" for i in range(5)])
    mocker.patch("voice_engine.os.path.join", side_effect=lambda *args: "/".join(args))
    mocker.patch("voice_engine.os.path.getmtime", side_effect=lambda path: int(path.split("_")[-1].split(".")[0]))
    mock_remove = mocker.patch("voice_engine.os.remove")
    
    # Cleanup to keep only 2 files
    cleanup_old_audio(max_files=2)
    
    # Should remove 3 files (test_0, test_1, test_2)
    assert mock_remove.call_count == 3
