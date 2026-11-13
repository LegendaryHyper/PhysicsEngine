# Overview
This project is a self-initiated attempt at combining Python and physics by simulating N-body orbital mechanics using various integrators. The project's goal was to also analyze how certain integrators behave in terms of positional and energy conservations.
## General Properties
* The engine is designed with a modular structure with its files, folders, and classes, ensuring that future additions to the code does not require the contributor to deal with what is colloquially called "spaghetti code."
* The engine's UI is designed using DearPyGUI, which lets the user have neat functions with the windows such as moving them around (even though they have default placements for when the application is booted up).
## Utilities
* A scenarios feature that lets future contibutions add certain initial conditions and rulesets to scenarios. As of the current date (v1.5.1b), the engine has two scenarios, with one being a mini-solar system including the Sun, Earth, and Moon with universal gravitation forces in place, and the other being a free fall scenario where objects can be inspected falling with Earth gravity.
* A body inspection (display) window where the positions of the bodies are visualized, along with traces to show the path they recently took. This window also includes:
  * Zooming and panning features through the display window.
  * A "Pause/Resume" button to pause/resume the time.
  * An "Auto Scale" button for the window to automatically pan and zoom your window so that no bodies remain undisplayed outside the window.
  * A "Clear Bodies" button to wipe all bodies.
  * A logarithmic "dt slider" that allows the user to set the time steps used to continue simulating (with a higher dt meaning less accuracy and faster simulation).
  * A "Time Passed" text that displays the total amount of time passed in the simulation (defaults to days for the "Orbital" scenario and seconds for the "Earth Surface" scenario).
  * A "Change Units (t)" button allowing the user to change the units the passed time is displayed in. The available options:
    * Milliseconds
    * Seconds
    * Minutes
    * Hours
    * Days
    * Weeks
    * Months
    * Years
  * A text displaying whether the simulation is paused or playing.
* An "Energy Graph in Time" graph that displays the total mechanical energy of the system as time passes (must remain constant in an ideal simulation). Fluctuations in this graph allows us to map the behavior and inaccuracies of the active integrator.
* A "Body Info" window that displays the name, mass, radius, position, and speed of a body upon the body being right-clicked on the display window. The creation of impulses with user-set force components and time is also accessed under this window.
* A "Body Creation" window that allows the user to create bodies with a user-set name, mass, radius, position (with x and y components), and velocity (with x and y components).
* A "Settings" window that allows the user to set the volume of the music playing and sound effects respectively, "Main Menu" and "Exit" buttons, and an additional "Advanced Settings" node. The node includes:
  * A "Max Trail" text box to set the maximum number of data points stored to draw the trails of the bodies (defaults to 25000 points).
  * A "History Time Window" text box to set how far into the past the time-energy data remain stored in the time-energy graph (defaults to 60 seconds in real-time).
  * A "Body Render Period" box to display how often the bodies' positions and trails are updated in the display window (defaults to once every one frame; positive integers may be entered to change it to once every n frames).
  * A "Set Integrator" dropdown to pick one of the five integrators available in the engine as of the current date (v1.5.1b). The integrators:
    * Explicit Euler (non-symplectic (does not guarantee an overall conservation of energy), functions as a benchmark for the other integrators with the least-optimal capabilities due to significant energy and position drifts).
    * Semi-Implicit Euler (symplectic (guarantees an overall conservation of energy), decent for long-term orbital stability with considerable sinodial oscillations in mechanical energy).
    * Velocity Verlet (symplectic (guarantees an overall conservation of energy), great for long-term orbital stability).
    * Leapfrog (symplectic (guarantees an overall conservation of energy), great for long-term orbital stability).
    * Runge-Kutta 4 (often acronymized as RK4, non-symplectic (does not guarantee an overall conservation of energy), optimal for positional accuracy and more negligible energy drifts in contrast to other non-symplectic integrators such as Explicit Euler).
## File Structure
* The "audio" folder for audial management.
  * "music" and "sound" folders for background musics and sound effects.
  * The "audio_manager.py" file for music/sfx volume management and music changing.
* The "engine" folder for the back-end of the physics simulations.
  * The "analysis" folder containing "energy.py" for the obtainment of mechanical energy.
  * The "core" folder.
    * The "body.py" file, which contains the "Body" class object-oriented body management and the "Body System" class to contain the said bodies.
    * The "simulation.py" file, which contains the "Simulation" class that manages the time steps, force computation, and elastic/non-elastic collisions.
  * The "forces" folder to manage forces.
    * The "collisions.py" file, which manages elastic and non-elastic collisions.
    * The "force_events.py" file, which holds the "ForceEvent" class that holds the active forces.
    * The "forces.py" file, which holds the initially set force classes for Earth surface gravitation and universal gravitation for their respective scenarios and applies forces initiated through this file.
* The "scenarios" folder.
  * The "earth_surface_scenario.py" file that holds the set conditions and rules for the "Earth Surface" scenario.
  * The "orbital_scenario.py" file that holds the set conditions and rules for the "Orbital" scenario.
* The "visualization" folder, which holds the "gui.py" file that manages the front-end of the engine using DearPyGUI.
* The "main.py" file to initiate the application.
## Prerequisites
* NumPy
* DearPyGUI
* PyGame
* Standard libraries (ctypes, os, time).
## Quick Start
1. Clone the repository:
```git clone https://github.com/LegendaryHyper/PhysicsEngine.git
cd PhysicsEngine```
2. Install dependencies:
```pip install numpy dearpygui pygame```
3. Run the engine:
```python main.py```
