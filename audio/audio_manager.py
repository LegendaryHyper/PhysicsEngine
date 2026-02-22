import pygame
import os
import random

class AudioManager():
    def __init__(self, music_folder, sound_folder):
        pygame.mixer.init()
        self.music_folder = music_folder
        self.last_track = None
        self.current_track = None
        self.tracks = [
            os.path.join(music_folder, f)
            for f in os.listdir(music_folder)
            if f.endswith((".mp3", ".wav", ".ogg"))
        ]
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
        
        self.sounds = {}
        
        for file in os.listdir(sound_folder):
            if file.endswith((".mp3", ".wav", ".ogg")):
                name = os.path.splitext(file)[0]
                path = os.path.join(sound_folder, file)
                self.sounds[name] = pygame.mixer.Sound(path)
    
    def play_random_music(self):
        if not self.tracks:
            print("No music tracks found!")
            return
        
        available = [t for t in self.tracks if t != self.last_track]
        track = random.choice(available) if available else random.choice(self.tracks)
        
        self.last_track = track
        pygame.mixer.music.load(track)
        pygame.mixer.music.play()
    def update(self):
        if not pygame.mixer.music.get_busy():
            self.play_random_music()
    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume)
    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()
    def set_sfx_volume(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(volume)