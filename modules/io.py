import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from modules.settings import load_settings
settings = load_settings()

def init_gpio():
#GPIO SETUP
    GPIO.setwarnings(False)    # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
    GPIO.setup(settings['pic_taken_led'] , GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)
    GPIO.setup(settings['beam_pin'], GPIO.IN,pull_up_down=GPIO.PUD_UP )   # Set pin 8 to be an output pin and set initial value to low (off)
    # pull_up_down=GPIO.PUD_UP #use this if not using 10k resistor
    print("gpio setup")