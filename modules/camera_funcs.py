from datetime import datetime
from pathlib import Path
import os
from picamera import PiCamera #Import camera lib

from modules.settings import load_settings
settings = load_settings()

def setup_camera():
    camera = PiCamera()
    camera.shutter_speed = settings['camera_shutter_speed']
    return camera

def capture_image(lotname,camera):
    """Captures an image from the camera with a timestamp """
    timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    file_name = lotname + ' ' + timestamp + '.jpg'
    full_path = settings['pictures_directory'] + "/" + lotname
    camera.capture(str(full_path) + "/" + str(file_name))

def get_last_pic(lotname) -> Path:
    """ returns the lastest picture in the current lot folder """
    p = (settings['pictures_directory'] / lotname).glob('**/*')
    files = [x for x in p if x.is_file()]
    latest = max(files , key = os.path.getctime)
    return latest