from pathlib import Path
import json

def load_settings():
    """Load saved settings, if not exist create default settings.json"""
    # Reading JSON content from a file
 
    # change later
    settings_file = Path.cwd() / 'settings.json'
    if settings_file.is_file():
        # file exists
        with open(settings_file, 'r') as f:
            data = json.load(f)
            return data
    else:
        #Write default settings to json file
        default_settings = {
            "window_height" : 600,
            "window_width" : 800,
            "picture_height" : 400,
            "picture_width" : 300,
            "gui_preview_x" : 100,
            "gui_preview_y" : 100,
            "beam_pin" : 10,
            "pic_taken_led" : 8,
            "pictures_directory" : '/home/pi/Documents/Lots',
            "bounce_time" : 200,
            "picture_delay" : 200 ,#IN MILISECONDS
            "camera_shutter_speed" : 20000,
            "smart_plug_ip":"192.168.0.39"
        }
        # Writing JSON content to a file using the dump method
        print("here")
        with open(settings_file, 'w') as f:
            json.dump(default_settings, f, sort_keys=True,indent=4)
    return default_settings

def save_settings(settings_dict):
    settings_file = Path("./settings.py")
    if settings_file.is_file():
        # file exists
        with open(settings_file, 'w') as f:
            json.dump(settings_dict, f, sort_keys=True)