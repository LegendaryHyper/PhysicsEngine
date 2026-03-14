import dearpygui.dearpygui as dpg
import ctypes
import numpy as np
from engine.analysis.energy import compute_energy_univ_grav
from engine.core.body import Body, BodySystem
from engine.forces.force_events import ForceEvent
import time
from scenarios.orbital_scenario import OrbitalScenario
from scenarios.earth_surface_scenario import EarthSurfaceScenario

def run_gui(audio):
    
    dpg.create_context()
    print(f"Running on DearPyGUI {dpg.get_dearpygui_version()}")
    
    current_state = "MAIN_MENU"
    sim = None
    active_body = None
    halo_tag = None
    
    orbit_data = []
    orbit_series_tags = []
    position_dot_tags = []
    times = []
    energies = []
    
    camera_center = np.array([0.0, 0.0])
    camera_half_range = 2e11
    zoom_sensitivity = 0.1
    halo_size = 12
    max_trail = 2000
    max_history = 2000
    body_render_period = 3
    auto_scale = True
    paused = False

    def toggle_pause():
        nonlocal paused
        paused = not paused
        audio.play_sound("click")
        if paused:
            dpg.set_value("pause_displayer", "Paused")
        else:
            dpg.set_value("pause_displayer", "Playing")
    def set_music_volume(sender, app_data):
        audio.set_music_volume(volume=app_data/2)
    def set_audio_volume(sender, app_data):
        audio.set_sfx_volume(volume=app_data)
    def toggle_auto_scale():
        nonlocal auto_scale
        auto_scale = not auto_scale
        audio.play_sound("click")
    def exit_app():
        audio.play_sound("click")
        time.sleep(0.25)
        dpg.stop_dearpygui()
        
    def create_body():
        try:
            name = dpg.get_value("input_body_name")
            mass = float(dpg.get_value("input_body_mass"))
            radius = float(dpg.get_value("input_body_radius"))
            
            px = float(dpg.get_value("input_body_position_x"))
            py = float(dpg.get_value("input_body_position_y"))
            
            vx = float(dpg.get_value("input_body_velocity_x"))
            vy = float(dpg.get_value("input_body_velocity_y"))

            new_body = Body(name=name, mass=mass, position=[px, py], velocity=[vx, vy], radius=radius)
            sim.body_system.bodies.append(new_body)
            
            orbit_data.append({"x": [], "y": []})
            l_tag = dpg.add_line_series([], [], parent=orbit_y_axis)
            d_tag = dpg.add_scatter_series([], [], parent=orbit_y_axis)
            
            orbit_series_tags.append(l_tag)
            position_dot_tags.append(d_tag)
        except ValueError:
            print("Error: Please enter numerical values!")
        audio.play_sound("click")
    
    def apply_impulse_user():
        try:
            fx = float(dpg.get_value("input_impulse_x"))
            fy = float(dpg.get_value("input_impulse_y"))
            delta_t = float(dpg.get_value("input_impulse_time"))
            sim.force_events.append(ForceEvent(body=active_body, force=np.array([fx, fy]), remaining_time=50*delta_t))
        except ValueError:
            print("Error: Please enter numerical values!")
        audio.play_sound("click")
            
    
    def clear_bodies():
        nonlocal active_body
        sim.body_system.bodies.clear()
        
        for tag in orbit_series_tags:
            if dpg.does_item_exist(tag):
                dpg.delete_item(tag)
        
        for tag in position_dot_tags:
            if dpg.does_item_exist(tag):
                dpg.delete_item(tag)
        
        orbit_data.clear()
        orbit_series_tags.clear()
        position_dot_tags.clear()
        active_body = None
        audio.play_sound("click")
    
    def delete_body():
        nonlocal active_body
        for i, body in enumerate(sim.body_system.bodies):
            if body == active_body:
                if dpg.does_item_exist(orbit_series_tags[i]):
                    dpg.delete_item(orbit_series_tags[i])
                if dpg.does_item_exist(position_dot_tags[i]):
                    dpg.delete_item(position_dot_tags[i])
                orbit_data.pop(i)
                orbit_series_tags.pop(i)
                position_dot_tags.pop(i)
        sim.body_system.bodies.remove(active_body)
        active_body = None
        audio.play_sound("click")
        
    def set_dt(sender, app_data):
        sim.dt = app_data
    
    def switch_state(new_state):
        nonlocal current_state
        current_state = new_state
        for tag in ["main_menu_win", "scenario_win", "sim_screen", "energy_display", "settings_window", "body_info", "body_creation"]:
            if dpg.does_item_exist(tag): dpg.configure_item(tag, show=False)
        
        if new_state == "MAIN_MENU":
            dpg.configure_item("main_menu_win", show=True)
        elif new_state == "SCENARIO_SELECT":
            dpg.configure_item("scenario_win", show=True)
        elif new_state == "SIMULATING":
            dpg.configure_item("sim_screen", show=True)
            dpg.configure_item("energy_display", show=True)
            dpg.configure_item("settings_window", show=True)
            dpg.configure_item("body_info", show=True)
            dpg.configure_item("body_creation", show=True)
        audio.play_sound("click")
    
    def load_scenario(scenario_name):
        nonlocal sim, orbit_data, orbit_series_tags, position_dot_tags, times, energies, camera_half_range, halo_tag
        print("Loading...")
        try:
            new_sim = None
            if scenario_name == "orbital":
                new_sim = OrbitalScenario().create_simulation()
                camera_half_range = 2e11
            elif scenario_name == "earth_surface":
                new_sim = EarthSurfaceScenario().create_simulation()
                camera_half_range = 1e5

            if new_sim is None:
                print("FAIL: create_simulation() returned None!")
                return

            sim = new_sim
            orbit_data = [{"x": [], "y": []} for _ in sim.body_system.bodies]

        except Exception as e:
            print(f"CRASH CAUGHT: {repr(e)}")
            import traceback
            traceback.print_exc()
            return
        
        print("Successfully assigned data")

        if dpg.does_item_exist("orbit_y_axis"):
            dpg.delete_item("orbit_y_axis", children_only=True)
        
        orbit_series_tags.clear()
        position_dot_tags.clear()
        times.clear()
        energies.clear()
        
        for i, _ in enumerate(sim.body_system.bodies):
            l_tag = dpg.add_line_series([], [], parent="orbit_y_axis")
            d_tag = dpg.add_scatter_series([], [], parent="orbit_y_axis")
            
            orbit_series_tags.append(l_tag)
            position_dot_tags.append(d_tag)
        
        halo_tag = dpg.add_scatter_series([], [], parent="orbit_y_axis")
        
        with dpg.theme() as halo_theme:
            with dpg.theme_component(dpg.mvScatterSeries):
                dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, halo_size)
                dpg.add_theme_color(dpg.mvPlotCol_MarkerFill, (0, 0, 0, 0))
                dpg.add_theme_color(dpg.mvPlotCol_MarkerOutline, (255, 255, 0, 255))
        
        dpg.bind_item_theme(halo_tag, halo_theme)
        
        dpg.configure_item("dt_slider", default_value=sim.dt)
        
        switch_state("SIMULATING")
        
        print("Switched state!")
    
    with dpg.window(tag="main_menu_win", label="Physics Engine v1.3", width=400, height=300, pos=(560, 290)):
        dpg.add_text("PHYSICS Engine v1.3")
        dpg.add_button(label="RUN", width=200, callback=lambda: switch_state("SCENARIO_SELECT"))
        dpg.add_button(label="EXIT", width=200, callback=exit_app)
    with dpg.window(tag="scenario_win", label="Select Scenario", show=False, width=400, height=300, pos=(560, 290)):
        dpg.add_button(label="Orbital", callback=lambda: load_scenario("orbital"))
        dpg.add_button(label="Earth Surface", callback=lambda: load_scenario("earth_surface"))
        dpg.add_spacer(height=20)
        dpg.add_button(label="BACK", callback=lambda: switch_state("MAIN_MENU"))
    with dpg.window(tag="sim_screen", label="Earth and Moon", show=False):
        with dpg.plot(label="Orbit", tag="pos_displayer", height=500, width=500, no_mouse_pos=True, no_box_select=True, no_menus=True):
            orbit_x_axis = dpg.add_plot_axis(dpg.mvXAxis, tag="orbit_x_axis")
            orbit_y_axis = dpg.add_plot_axis(dpg.mvYAxis, tag="orbit_y_axis")
            with dpg.draw_layer(tag="hitbox_layer"):
                pass
        dpg.add_button(label="Pause/Resume", callback=toggle_pause)
        dpg.add_button(label="Auto Scale", callback=toggle_auto_scale)
        dpg.add_button(label="Clear Bodies", callback=clear_bodies)
        dpg.add_slider_float(label="dt", tag="dt_slider", min_value = 0.001, max_value=250000, default_value=1, callback=set_dt)
        dpg.add_text(label="Time passed (days): ", tag="time_displayer")
        dpg.add_text(label="Playing", tag="pause_displayer")
        dpg.set_value("pause_displayer", "Playing")
    with dpg.window(tag="energy_display", label="Energy Graph in Time", pos=(520, 0), show=False):
        with dpg.plot(label="Energy", tag="energy_plot", height=250, width=600):
            energy_x_axis = dpg.add_plot_axis(dpg.mvXAxis)
            energy_y_axis = dpg.add_plot_axis(dpg.mvYAxis)
            dpg.add_line_series([], [], tag="energy_series", parent=energy_y_axis)
    with dpg.window(tag="settings_window", label="Settings", width=330, height=150, pos=(1210, 0), show=False):
        dpg.add_text(label="Now playing: ", tag="music_name_displayer")
        dpg.add_slider_float(label="Music volume", min_value=0.0, max_value=1, default_value=0.05, callback=set_music_volume)
        dpg.add_slider_float(label="Audio volume", min_value=0.0, max_value=1, default_value=1, callback=set_audio_volume)
        dpg.add_button(label="Main Menu", tag="main_menu_button", callback=lambda: switch_state("MAIN_MENU"))
        dpg.add_button(label="Exit", tag="exit_button", callback=exit_app)
    with dpg.window(tag="body_info", label="Body Info", show=False, width=450, height=125, pos=(520, 290)):
        dpg.add_text(tag="body_name")
        dpg.add_text(tag="body_mass")
        dpg.add_text(tag="body_radius")
        dpg.add_text(tag="body_position")
        dpg.add_text(tag="body_velocity")
        dpg.add_text(tag="text_create_impulse")
        dpg.set_value("text_create_impulse", "Create Impulse")
        dpg.add_input_text(tag="input_impulse_x", hint="Force (x)")
        dpg.add_input_text(tag="input_impulse_y", hint="Force (y)")
        dpg.add_input_text(tag="input_impulse_time", hint="Impulse Duration (s)")
        dpg.add_button(label="Apply Impulse", tag="apply_impulse_button", callback=apply_impulse_user)
        dpg.add_button(label="Delete Body", tag="delete_body_button", callback=delete_body)
    with dpg.window(tag="body_creation", label="Body Creation", show=False, width=400, height=200, pos=(520, 425)):
        input_name = dpg.add_input_text(tag="input_body_name", hint="Object Name")
        input_mass = dpg.add_input_text(tag="input_body_mass", hint="Object Mass (kg)")
        input_radius = dpg.add_input_text(tag="input_body_radius", hint="Object Radius (m)")
        dpg.add_text("Position (m)")
        input_position_x = dpg.add_input_text(tag="input_body_position_x", hint="x")
        input_position_y = dpg.add_input_text(tag="input_body_position_y", hint="y")
        dpg.add_text("Velocity (m/s)")
        input_velocity_x = dpg.add_input_text(tag="input_body_velocity_x", hint="x")
        input_velocity_y = dpg.add_input_text(tag="input_body_velocity_y", hint="y")
        dpg.add_button(tag="create_body_button", label="Create Body", callback=create_body)
    
    
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    dpg.create_viewport(
        title="Orbital Engine",
        width=screen_width,
        height=screen_height,
        decorated=False
    )

    with dpg.handler_registry():
        is_dragging = False
        last_mouse_pos = None
        
        def mouse_wheel_handler(sender, app_data):
            nonlocal camera_half_range, camera_center, auto_scale
            if current_state == "SIMULATING":
                if dpg.is_item_hovered("pos_displayer"):

                    auto_scale = False
                    
                    scroll = app_data
                    zoom_factor = 1 - scroll * zoom_sensitivity
                    zoom_factor = max(0.1, zoom_factor)
                    
                    mouse_plot = dpg.get_plot_mouse_pos()
                    
                    mx, my = mouse_plot
                    cx, cy = camera_center
                    
                    camera_center[0] = mx + (cx - mx) * zoom_factor
                    camera_center[1] = my + (cy - my) * zoom_factor
                    
                    camera_half_range *= zoom_factor
                    #camera_half_range = max(camera_half_range, 1e7)
        dpg.add_mouse_wheel_handler(callback=mouse_wheel_handler)
        def mouse_click_handler(sender, app_data):
            nonlocal is_dragging, last_mouse_pos, active_body
            if app_data == 0:
                if current_state == "SIMULATING":
                    if dpg.is_item_hovered("pos_displayer"):
                        is_dragging = True
                        last_mouse_pos = dpg.get_mouse_pos()
            elif app_data == 1:
                if current_state == "SIMULATING":
                    selection_radius = camera_half_range * 0.02
                    mx, my = dpg.get_plot_mouse_pos()
                    selected_body = None
                    closest_dist = float("inf")

                    for body in sim.body_system.bodies:
                        x, y = body.position
                        dist = ((x - mx)**2 + (y - my)**2)**0.5
                        
                        if dist < closest_dist:
                            closest_dist = dist
                            selected_body = body
                    if closest_dist < selection_radius:
                        active_body = selected_body
                        
                    else:
                        active_body = None
        def mouse_release_handler(sender, app_data):
            nonlocal is_dragging
            if app_data == 0:
                is_dragging = False
        def mouse_drag_handler(sender, app_data):
            nonlocal camera_center, camera_half_range, auto_scale, is_dragging, last_mouse_pos
            if current_state == "SIMULATING":
                if not auto_scale and is_dragging:
                    current_mouse = dpg.get_mouse_pos()
                    dx = current_mouse[0] - last_mouse_pos[0]
                    dy = current_mouse[1] - last_mouse_pos[1]
                    
                    plot_width = dpg.get_item_rect_size("pos_displayer")[0]
                    plot_height = dpg.get_item_rect_size("pos_displayer")[1]
                    
                    x_scale = (2 * camera_half_range) / plot_width
                    y_scale = (2 * camera_half_range) / plot_height
                    
                    camera_center[0] -= dx * x_scale
                    camera_center[1] += dy * y_scale
                    
                    last_mouse_pos = current_mouse
        
        dpg.add_mouse_click_handler(callback=mouse_click_handler)
        dpg.add_mouse_release_handler(callback=mouse_release_handler)
        dpg.add_mouse_drag_handler(button=0, callback=mouse_drag_handler)
    
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.toggle_viewport_fullscreen()

    while dpg.is_dearpygui_running():
        
        audio.update()
        
        scale = 500/(2 * camera_half_range)
        
        if current_state == "SIMULATING" and sim is not None:
            if not paused:
                sim.step()
            
            if len(energies) > 1:
                min_t = min(times)
                max_t = max(times)
                min_e = min(energies)
                max_e = max(energies)
                
                dpg.set_axis_limits(energy_x_axis, min_t, max_t)
                dpg.set_axis_limits(energy_y_axis, min_e, max_e)
            
            if auto_scale:
                if any(len(b["x"]) > 0 for b in orbit_data):
                    all_x = []
                    all_y = []
                    for b in orbit_data:
                        all_x.extend(b["x"])
                        all_y.extend(b["y"])
                
                    min_x = min(all_x)
                    max_x = max(all_x)
                    min_y = min(all_y)
                    max_y = max(all_y)
                
                    range_x = max_x - min_x
                    range_y = max_y - min_y

                    max_range = max(range_x, range_y)
                
                    if max_range == 0:
                        max_range = 1
                
                    cx = (min_x + max_x)/2
                    cy = (min_y + max_y)/2
                
                    padding_factor = 1.2
                    final_range =  max_range * 0.5 * padding_factor

                    dpg.set_axis_limits(orbit_x_axis, cx - final_range, cx + final_range)
                    dpg.set_axis_limits(orbit_y_axis, cy - final_range, cy + final_range)
            else:
                cx, cy = camera_center
                dpg.set_axis_limits(orbit_x_axis, cx - camera_half_range, cx + camera_half_range)
                dpg.set_axis_limits(orbit_y_axis, cy - camera_half_range, cy + camera_half_range)
                
            times.append(sim.time / 86400)
            energies.append(compute_energy_univ_grav(sim.body_system))

            if len(times) > max_history:
                times.pop(0)
                energies.pop(0)
            
            for i, body in enumerate(sim.body_system.bodies):
                x, y = body.position
                
                if len(times) % body_render_period == 0:
                    orbit_data[i]["x"].append(x)
                    orbit_data[i]["y"].append(y)
                
                    if len(orbit_data[i]["x"]) > max_trail:
                        orbit_data[i]["x"].pop(0)
                        orbit_data[i]["y"].pop(0)
                
                    dpg.set_value(
                        orbit_series_tags[i],
                        [orbit_data[i]["x"], orbit_data[i]["y"]]
                    )
                
                    dpg.set_value(
                        position_dot_tags[i],
                        [[x], [y]]
                    )
                
            dpg.set_value("energy_series", [times, energies])
            dpg.set_value("time_displayer", f"Time passed (days): {round((sim.time/86400), ndigits=1)}")
            if active_body:
                vx, vy = active_body.velocity
                x, y = active_body.position
                dpg.set_value(halo_tag, [[x], [y]])
                
                dpg.set_value("body_name", active_body.name)
                dpg.set_value("body_mass", f"Mass: {active_body.mass}")
                dpg.set_value("body_radius", f"Radius: {active_body.radius}")
                dpg.set_value("body_position", f"Position (x, y): ({x}, {y})")
                dpg.set_value("body_velocity", f"Velocity: {round((vx**2+vy**2)**0.5, 2)} m/s")
                dpg.set_value("text_create_impulse", "Create Impulse")
                dpg.configure_item("input_impulse_x", show=True)
                dpg.configure_item("input_impulse_y", show=True)
                dpg.configure_item("input_impulse_time", show=True)
                dpg.configure_item("apply_impulse_button", show=True)
                dpg.configure_item("delete_body_button", show=True)
            else:
                dpg.set_value(halo_tag, [[], []])
                dpg.set_value("body_name", "No body selected")
                dpg.set_value("body_mass", "")
                dpg.set_value("body_radius", "")
                dpg.set_value("body_position", "")
                dpg.set_value("body_velocity", "")
                dpg.set_value("text_create_impulse", "")
                dpg.configure_item("input_impulse_x", show=False)
                dpg.configure_item("input_impulse_y", show=False)
                dpg.configure_item("input_impulse_time", show=False)
                dpg.configure_item("apply_impulse_button", show=False)
                dpg.configure_item("delete_body_button", show=False)
                
            
            dpg.delete_item("hitbox_layer", children_only=True)
            
            for body in sim.body_system.bodies:
                dpg.draw_circle(
                    center=(body.position[0], body.position[1]),
                    radius=body.radius,
                    color=(155, 155, 0),
                    thickness=1,
                    parent="hitbox_layer"
                )
        dpg.render_dearpygui_frame()
    dpg.destroy_context()