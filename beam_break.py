import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module
from picamera import PiCamera #Import camera lib
from datetime import datetime
from pathlib import Path
import os

class Breaker:
    
    
    def __init__(self,lot_name):
        self.lot_name = lot_name
        self.beam_pin = 40
        self.pic_taken_led = 8
        
        #lot_name='072219TEST'
        self.pictures_path = (Path('/home/pi/Documents') / lot_name)
        self.pictures_path.mkdir(parents=True, exist_ok=True)
        
        #GPIO SETUP
        GPIO.setwarnings(False)    # Ignore warning for now
        GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
        GPIO.setup(self.pic_taken_led, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)
        GPIO.setup(self.beam_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # Set pin 8 to be an output pin and set initial value to low (off)
        GPIO.add_event_detect(self.beam_pin, GPIO.FALLING, callback=self.beam_break_cb, bouncetime=300)
        
        #init camera
        self.camera = PiCamera()
        self.camera.start_preview()
        sleep(2)#sleep to let camera's sensors adjust
       
    @staticmethod
    def test(meh):
        print(meh)
    
    def capture_image(self):
        """Captures an image from the camera with a timestamp """
        timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        file_name = self.lot_name + ' ' + timestamp + '.jpg'
        full_path = (self.pictures_path / file_name).resolve()
        #print()
        self.camera.capture(str(full_path))
        #capture_image()
        
    def beam_break_cb(self,chan):
        """Callback called when the beam is broken """
        #global beam_broken
        #beam_broken = not beam_broken
        #GPIO.output(pic_taken_led,GPIO.HIGH if beam_broken else GPIO.LOW)
        print("beam broken")
        Breaker.capture_image(self)

    def get_last_pic(self) -> Path:
        """ returns the lastest picture in the current lot folder """
        p = Path(self.pictures_path).glob('**/*')
        files = [x for x in p if x.is_file()]
        latest = max(files , key = os.path.getctime)
        return latest
        
