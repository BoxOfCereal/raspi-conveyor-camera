import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from guizero import App, Text, TextBox, PushButton, Slider, Picture

def say_my_name():
    welcome_message.value = my_name.value
    
def change_text_size(slider_value):
    welcome_message.size = slider_value



BEAM_PIN = 10

#GPIO SETUP
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
# Set pin 10 to be an output pin and set initial value to low (off)
GPIO.setup(BEAM_PIN, GPIO.IN,pull_up_down=GPIO.PUD_UP )
# pull_up_down=GPIO.PUD_UP #use this if not using 10k resistor

def break_cb(e):
    print(e,"broken")

GPIO.add_event_detect(BEAM_PIN, GPIO.FALLING, callback=break_cb)

app = App(title="Hello world", width=640, height=480)
my_name = TextBox(app)

app.display()