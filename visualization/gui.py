import dearpygui.dearpygui as dpg
import ctypes
import numpy as np
from engine.analysis.energy import compute_energy_univ_grav

def run_gui(sim, audio):
    
    dpg.create_context()

    orbit_data = []

    for _ in sim.body_system.bodies:
        orbit_data.append({
            "x": [],
            "y": []
        })
    
    times = []
    energies = []
    
    camera_center = np.array([0.0, 0.0])
    camera_half_range = 2e11
    zoom_sensitivity = 0.1
    
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
    
    
    with dpg.window(tag="sim_screen", label="Earth and Moon"):
        with dpg.plot(label="Orbit", tag="pos_displayer", height=500, width=500, no_mouse_pos=True, no_box_select=True, no_menus=True):
            orbit_x_axis = dpg.add_plot_axis(dpg.mvXAxis)
            orbit_y_axis = dpg.add_plot_axis(dpg.mvYAxis)
            #dpg.add_line_series([], [], tag="orbit_series", parent=orbit_y_axis)

            orbit_series_tags = []
            position_dot_tags = []
            
            for i, body in enumerate(sim.body_system.bodies):
                line_tag = f"orbit_series_{i}"
                dot_tag = f"orbit_dot_{i}"

                orbit_series_tags.append(line_tag)
                position_dot_tags.append(dot_tag)
                
                dpg.add_line_series([], [], tag=line_tag, parent=orbit_y_axis)
                dpg.add_scatter_series([], [], tag=dot_tag, parent=orbit_y_axis)
        dpg.add_button(label="Pause/Resume", callback=toggle_pause)
        dpg.add_button(label="Auto Scale", callback=toggle_auto_scale)
        dpg.add_text(label="Time passed (days): ", tag="time_displayer")
        dpg.add_text(label="Playing", tag="pause_displayer")
    with dpg.window(tag="energy_display", label="Energy Graph in Time", pos=(520, 0)):
        with dpg.plot(label="Energy", tag="energy_plot", height=250, width=600):
            energy_x_axis = dpg.add_plot_axis(dpg.mvXAxis)
            energy_y_axis = dpg.add_plot_axis(dpg.mvYAxis)
            dpg.add_line_series([], [], tag="energy_series", parent=energy_y_axis)
    with dpg.window(tag="audio_displayer", label="Audio Displayer", width=330, height=100, pos=(1210, 0)):
        dpg.add_text(label="Now playing: ", tag="music_name_displayer")
        dpg.add_slider_float(label="Music volume", min_value=0.0, max_value=1, default_value=0.05, callback=set_music_volume)
        dpg.add_slider_float(label="Audio volume", min_value=0.0, max_value=1, default_value=1, callback=set_audio_volume)

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
            if not dpg.is_item_hovered("pos_displayer"):
                return
            
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
            camera_half_range = max(camera_half_range, 1e7)
        dpg.add_mouse_wheel_handler(callback=mouse_wheel_handler)
        def mouse_click_handler(sender, app_data):
            nonlocal is_dragging, last_mouse_pos
            if app_data == 0:
                if dpg.is_item_hovered("pos_displayer"):
                    is_dragging = True
                    last_mouse_pos = dpg.get_mouse_pos()
        def mouse_release_handler(sender, app_data):
            nonlocal is_dragging
            if app_data == 0:
                is_dragging = False
        def mouse_drag_handler(sender, app_data):
            nonlocal camera_center, camera_half_range, auto_scale, is_dragging, last_mouse_pos
            
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

        for i, body in enumerate(sim.body_system.bodies):
            x, y = body.position
            
            orbit_data[i]["x"].append(x)
            orbit_data[i]["y"].append(y)
            
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

        dpg.render_dearpygui_frame()

    dpg.destroy_context()