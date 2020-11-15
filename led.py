import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # Set pin 8 to be an output pin and set initial value to low (off)

beam_broken = False
print("test")

def beam_break_cb(ev=None):
    #global beam_broken
    #beam_broken = not beam_broken
    #GPIO.output(8,GPIO.HIGH if beam_broken else GPIO.LOW)
    print("beam broken")
    
GPIO.add_event_detect(12,GPIO.FALLING,callback=beam_break_cb,bouncetime=300)
    

while True: # Run forever
 sleep(1) # Sleep for 1 second
 #print("sleep")
