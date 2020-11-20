from datetime import datetime
from pathlib import Path
import os
from picamera import PiCamera #Import camera lib

from modules.settings import load_settings
settings = load_settings()


class Camera:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.shutter_speed = settings['camera_shutter_speed']
        self.last_picture = ""

    def debug_image(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        file_name = "debug" + ' ' + timestamp + '.jpg'
        full_path = settings['debug_directory'] + "/" + file_name
        self.camera.capture(str(full_path))
        self.last_picture = full_path

    def capture_image(self,lotname):
        """Captures an image from the camera with a timestamp """
        timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        file_name = lotname + ' ' + timestamp + '.jpg'
        full_path = settings['pictures_directory'] + "/" + lotname + "/" + file_name
        self.camera.capture(str(full_path))
        self.last_picture = full_path

    def get_last_n_pics(self,lotname,n=5):
        """ returns the lastest picture in the current lot folder """
        p = Path(settings['pictures_directory'] + "/" + lotname).glob('**/*')
        files = [x for x in p if x.is_file()]
        last_pics = files.sort(key = os.path.getctime)
        return last_pics[:n]