#!/usr/bin/python3
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from picamera import PiCamera #Import camera lib
from time import sleep,time   # Import the sleep function from the time module
import os
from pathlib import Path
from guizero import App, Text, TextBox, PushButton, Slider, Picture,MenuBar, Box, Window
from tkinter import filedialog
from datetime import datetime
import errno






lotname = None
camera = PiCamera()
camera.shutter_speed = 20000

#CONSTANTS
WINDOW_HEIGHT = 600

WINDOW_WIDTH =800
PICTURE_HEIGHT = 400
PICTURE_WIDTH = 300
GUI_PREVIEW_X = 100
GUI_PREVIEW_Y = 100
BEAM_PIN = 10
PIC_TAKEN_LED = 8
PICTURES_DIRECTORY = (Path('/home/pi/Documents'))
BOUNCE_TIME = 200
PICTURE_DELAY = 200 #IN MILISECONDS


#GPIO SETUP
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
GPIO.setup(PIC_TAKEN_LED , GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)
GPIO.setup(BEAM_PIN, GPIO.IN,pull_up_down=GPIO.PUD_UP )   # Set pin 8 to be an output pin and set initial value to low (off)
# pull_up_down=GPIO.PUD_UP #use this if not using 10k resistor

#regular vars
start_time = None
end_time=None

def edit_function():
    print("Edit option")
    
def new_lot():
    print("new lot")
    global lotname, title
    lotname = app.question("New Lot Number", "What is the lot number?")
    
    if lotname is not None and len(lotname) > 0 :
        try:
            print(lotname)
            GPIO.remove_event_detect(40)
            pictures_path = PICTURES_DIRECTORY  / lotname
            #lot already exists check
            pictures_path.mkdir(parents=True, exist_ok=False)
            #init camera
            camera.start_preview()
            sleep(2)#sleep to let camera's sensors adjust
            
            #draw ui
            title.destroy()
            title = Text(box, text=f"Lot: {lotname}", size=14, font="Arial", grid=[1,0])
            
            #set up beam
            GPIO.add_event_detect(BEAM_PIN, GPIO.BOTH, callback=beam_break_cb)
        except :
            app.error("Lot Exists","The Lot Already Exists")
    else:
        app.error("No lotname","You must enter a lot name")
    
def open_lot():
    global lotname
    file_path = filedialog.askdirectory(initialdir = "/home/pi/Documents",title = "Select Lot")
    print(Path(file_path).stem)
    lotname = Path(file_path).stem
    if lotname is not None and len(lotname) > 0:
        print(len(lotname))
        #fix when nothing is selevted you get a blank folder error
        GPIO.remove_event_detect(40)
        #init camera
        camera.start_preview(fullscreen=False,window=(GUI_PREVIEW_X ,GUI_PREVIEW_Y ,PICTURE_WIDTH,PICTURE_HEIGHT))
        sleep(2)#sleep to let camera's sensors adjust
        
        #if nothing has been opened yet
        #if title is not None:
        #    title.destroy()
        title = Text(box, text=f"Lot: {lotname}", size=14, font="Arial", grid=[1,0])

        #set up cbs
        #cb = ButtonHandler(BEAM_PIN, beam_break_cb, edge='rising', bouncetime=BOUNCE_TIME)
        #cb.start()
        GPIO.add_event_detect(BEAM_PIN, GPIO.BOTH, callback=beam_break_cb)



def capture_image():
    """Captures an image from the camera with a timestamp """
    global lotname
    timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    file_name = lotname + ' ' + timestamp + '.jpg'
    full_path = (PICTURES_DIRECTORY  / lotname).resolve()
    camera.capture(str(full_path) + "/" + str(file_name))

def beam_break_cb(chan):
    """Callback called when the beam is broken """
    #print(chan,"beam broken")
    #I think here I will need some sort of delay for when the next pic should get taken
    current_time = time()
    end_time = current_time + PICTURE_DELAY

    print(start_time)
    #if enough time has't elapsed, don't tke a picture
    if (current_time < end_time):
        print("too soon")
    else:
        if GPIO.input(chan):
            print('Input was HIGH')
        else:
            print('Input was LOW')
            capture_image()
            show_picture()    

def get_last_pic() -> Path:
    """ returns the lastest picture in the current lot folder """
    p = (PICTURES_DIRECTORY / lotname).glob('**/*')
    files = [x for x in p if x.is_file()]
    latest = max(files , key = os.path.getctime)
    return latest
    
def show_picture():
    global box
    path = str(get_last_pic())
    picture = Picture(box, image=path, grid=[1,2],width=PICTURE_WIDTH,height=PICTURE_HEIGHT)

app = App(title="Hello world", width=WINDOW_WIDTH, height=WINDOW_HEIGHT)


menubar = MenuBar(app,
                  toplevel=["File", "Edit"],
                  options=[
                      [ ["New Lot", new_lot], ["Open Lot", open_lot] ],
                      [ ["Edit Lot Name", edit_function], ["Edit option 2", edit_function] ]
                  ])

box = Box(app,layout="grid")
title = Text(box, text=f"", size=14, font="Arial", grid=[1,0])
app.display()