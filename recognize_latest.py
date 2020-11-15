#!/usr/bin/python3
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from picamera import PiCamera #Import camera lib
from time import sleep,time   # Import the sleep function from the time module
import os
import json
from pathlib import Path
from guizero import App, Text, TextBox, PushButton, Slider, Picture,MenuBar, Box, Window
from tkinter import filedialog
from datetime import datetime
import errno
import sys

from modules.settings import load_settings, save_settings


#load settings




def settings_window_handler():
    """Function to handle settings window"""
    settings_window.show(wait=true)

def calibration():
    pass


settings = load_settings()
lotname = None
camera = PiCamera()
camera.shutter_speed = settings['camera_shutter_speed']


#GPIO SETUP
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
GPIO.setup(settings['pic_taken_led'] , GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)
GPIO.setup(settings['beam_pin'], GPIO.IN,pull_up_down=GPIO.PUD_UP )   # Set pin 8 to be an output pin and set initial value to low (off)
# pull_up_down=GPIO.PUD_UP #use this if not using 10k resistor


def new_lot():
    print("new lot")
    global lotname, title
    lotname = app.question("New Lot Number", "What is the lot number?")
    
    if lotname is not None and len(lotname) > 0 :
        try:
            
            print(lotname)
            GPIO.remove_event_detect(40)
            pictures_path = Path(settings['pictures_directory'])  / lotname
            #lot already exists check
            pictures_path.mkdir(parents=True, exist_ok=False)
            #init cameras
            print("starting preview")
            camera.start_preview()
            sleep(2)
            camera.stop_preview()
            
            #draw ui
            title.destroy()
            title = Text(box, text=f"Lot: {lotname}", size=14, font="Arial", grid=[1,0])
            
            #set up beam
            GPIO.add_event_detect(settings['beam_pin'], GPIO.BOTH, callback=beam_break_cb)
        except :
            # app.error("Lot Exists","The Lot Already Exists")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    else:
        app.error("No lotname","You must enter a lot name")
    
def open_lot():
    global lotname, title
    file_path = filedialog.askdirectory(initialdir = "/home/pi/Documents",title = "Select Lot")
    print(Path(file_path).stem)
    lotname = Path(file_path).stem
    if lotname is not None and len(lotname) > 0:
        print(len(lotname))
        #fix when nothing is selevted you get a blank folder error
        GPIO.remove_event_detect(40)
        #init camera
        camera.start_preview(fullscreen=False,
            window=(settings['gui_preview_x'] ,
                    settings['gui_preview_y'] ,
                    settings['picture_width'],
                    settings['picture_height']))
        sleep(2)#sleep to let camera's sensors adjust
        
        
        title = Text(box, text=f"Lot: {lotname}", size=14, font="Arial", grid=[1,0])

        GPIO.add_event_detect(settings['beam_pin'], GPIO.BOTH, callback=beam_break_cb)

def edit_lot():
    pass

def capture_image():
    """Captures an image from the camera with a timestamp """
    global lotname
    timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    file_name = lotname + ' ' + timestamp + '.jpg'
    full_path = (settings['pictures_directory']  / lotname).resolve()
    camera.capture(str(full_path) + "/" + str(file_name))

def beam_break_cb(chan):
    """Callback called when the beam is broken """
    #print(chan,"beam broken")
    #I think here I will need some sort of delay for when the next pic should get taken
    current_time = time()
    end_time = current_time + settings['picture_delay']

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
    p = (settings['pictures_directory'] / lotname).glob('**/*')
    files = [x for x in p if x.is_file()]
    latest = max(files , key = os.path.getctime)
    return latest
    
def show_picture():
    global box
    path = str(get_last_pic())
    picture = Picture(box, image=path, grid=[1,2],width=settings['picture_width'],height=settings['picture_height'])

def view_pictures():
    pass


def create_settings_window():

    def close_window():
        window.hide()

    window = Window(app, title="Setings",layout="grid")
    #name_label = Text(app, text="Name", grid=[0,0], align="left")")
    i = 0
    for key, value in settings.items():
        Text(window, text="f{key}",grid=[i,0], align="left")
        TextBox(window,text="f{value}",grid=[i,1], align="left")
        i = i + 1
    PushButton(window, text="Save", command=close_window,grid=[i,0])
    PushButton(window, text="Cancel", command=save_settings,grid=[i,1])

    window.hide()

    #cancel_button = PushButton(window, text="Cancel", command=close_window)
    return window

#create app
app = App(title="Hello world", width=settings['window_width'], height=settings['window_height'])

settings_window = create_settings_window


calibration_window = Window(app, title="Calibration")
calibration_window.hide()

view_pictures_window = Window(app, title="Pictures")
view_pictures_window.hide()

#load settings
settings = load_settings()
print(settings)

#init the menu bar
menubar = MenuBar(app,
                  toplevel=["File", "Edit",],
                  options=[
                      [ ["New Lot", new_lot], ["Open Lot", open_lot], ["Edit Lot Name", edit_lot],["View Pictures", view_pictures ] ],
                      [ ["Change Settings", settings_window_handler], ["Calibration", calibration ] ],
                  ])

box = Box(app,layout="grid")
title = Text(box, text=f"", size=14, font="Arial", grid=[1,0])
#display app.
app.display()

