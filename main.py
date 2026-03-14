import os
from audio.audio_manager import AudioManager
from visualization.gui import run_gui

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_VER = "v1.3.1"
music_path = os.path.join(BASE_DIR, "audio", "music")
sound_path = os.path.join(BASE_DIR, "audio", "sound")

audio = AudioManager(music_folder=music_path, sound_folder=sound_path)
audio.play_random_music()
audio.set_music_volume(0.025)

if __name__ == "__main__":
    print(f"PHYSICS ENGINE {ENGINE_VER}")
    print("Starting GUI...")
    run_gui(audio=audio)
    print("Killing GUI...")