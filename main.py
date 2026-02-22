import numpy as np
import matplotlib.pyplot as plt
import os

from engine.core.body import BodySystem, Body
from engine.core.simulation import Simulation
from engine.forces.forces import MutualGravity
from engine.integrators.semi_implicit_euler import SemiImplicitEuler
from engine.integrators.explicit_euler import ExplicitEuler
from audio.audio_manager import AudioManager
from visualization.gui import run_gui

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

music_path = os.path.join(BASE_DIR, "audio", "music")
sound_path = os.path.join(BASE_DIR, "audio", "sound")

earth = Body(6e24, [0.0, 0.0], [0.0, 29780.0])
moon = Body(7.347673e22, [384000000.0, 0.0], [0.0, 30802.0])
sun = Body(1.9891e30, [-150000000000.0, 0.0], [0.0, 0.0])

system = BodySystem([earth, moon, sun])
audio = AudioManager(music_folder=music_path, sound_folder=sound_path)
gravity = MutualGravity()
integrator = SemiImplicitEuler()

sim_dt = 1440

sim = Simulation(system, [gravity], integrator, dt=sim_dt)

audio.play_random_music()
audio.set_music_volume(0.05)

print("Starting GUI...")
run_gui(sim, audio)
print("Killing GUI...")