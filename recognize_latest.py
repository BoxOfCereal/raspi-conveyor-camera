#!/usr/bin/python3
import traceback
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from picamera import PiCamera  # Import camera lib
from time import sleep, time   # Import the sleep function from the time module
import os
import json
from pathlib import Path
from guizero import App, Text, TextBox, PushButton, Slider, Picture, MenuBar, Box, Window
from tkinter import filedialog
from datetime import datetime
import errno
import sys
import asyncio
import logging
from functools import partial

from modules.settings import load_settings, save_settings
from modules.io import init_gpio
from modules.camera_funcs import setup_camera, capture_image, get_last_pic
from modules.plug import turn_off_plug, turn_on_plug


logging.basicConfig(filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')

lotname = None

settings = load_settings()
init_gpio()
camera = setup_camera()


def destroy_kids(widget):
    for e in widget.children:
        e.destroy()

def shutdown_cleanup():
    print("running cleanup")
    # asyncio.run(turn_off_plug())
    turn_off_plug()
    app.destroy()


def settings_window_handler():
    """Function to handle settings window"""
    settings_window.show(wait=true)


def calibration():
    pass


def new_lot():
    print("new lot")
    global lotname,title_text
    lotname = app.question("New Lot Number", "What is the lot number?")

    if lotname is not None and len(lotname) > 0:
        try:

            print(lotname)
            GPIO.remove_event_detect(40)
            pictures_path = Path(settings['pictures_directory']) / lotname

            # lot already exists check
            pictures_path.mkdir(parents=True, exist_ok=False)

            # init cameras
            logging.debug("Starting Camera Preview")
            camera.start_preview()
            sleep(2)
            # capture_image(lotname,camera)

            # starting conveyor
            # asyncio.run(turn_on_plug())
            turn_on_plug()

            # simulate

            sim = partial(simulation, lotname, camera)
            app.after(3000, sim)
            app.after(6000, sim)
            app.after(8000, sim)
            app.after(12000, sim)

            # set up beam
            # GPIO.add_event_detect(settings['beam_pin'], GPIO.BOTH, callback=beam_break_cb)

            #update UI
            destroy_kids(title_box)
            title_text = Text(title_box, text=f"Lot: {lotname}", size=20, font="Arial")

        except:
            print(traceback.format_exc())

    else:
        app.error("No lotname", "You must enter a lot name")


def open_lot():
    global lotname, title
    file_path = filedialog.askdirectory(
        initialdir="/home/pi/Documents", title="Select Lot")
    print(Path(file_path).stem)
    lotname = Path(file_path).stem
    if lotname is not None and len(lotname) > 0:
        print(len(lotname))
        # fix when nothing is selevted you get a blank folder error
        GPIO.remove_event_detect(40)
        # init camera
        camera.start_preview(fullscreen=False,
                             window=(settings['gui_preview_x'],
                                     settings['gui_preview_y'],
                                     settings['picture_width'],
                                     settings['picture_height']))
        sleep(2)  # sleep to let camera's sensors adjust

        title = Text(
            main_box, text=f"Lot: {lotname}", size=14, font="Arial", grid=[1, 0])

        GPIO.add_event_detect(
            settings['beam_pin'], GPIO.BOTH, callback=beam_break_cb)


def edit_lot():
    pass


def beam_break_cb(chan):
    """Callback called when the beam is broken """
    #print(chan,"beam broken")
    # I think here I will need some sort of delay for when the next pic should get taken

    if GPIO.input(chan):
        print('Input was HIGH')
    else:
        print('Input was LOW')
        capture_image(lotname, camera)
        show_picture()


def beam_break_cb_simulation(lot, cam):
    print('Input was LOW')
    capture_image(lot, cam)
    show_picture()


def simulation(lot, cam):
    turn_off_plug()
    beam_break_cb_simulation(lot, cam)
    turn_on_plug()


def show_picture():
    global content_box
    path = str(get_last_pic(lotname))
    destroy_kids(content_box)
    picture = Picture(content_box, image=path, grid=[
                      0, 1, 4, 1], width=settings['picture_width'], height=settings['picture_height'])


def view_pictures():
    pass


def create_settings_window():

    def close_window():
        window.hide()

    window = Window(app, title="Setings", layout="grid")
    # name_label = Text(app, text="Name", grid=[0,0], align="left")")
    i = 0
    for key, value in settings.items():
        Text(window, text="f{key}", grid=[i, 0], align="left")
        TextBox(window, text="f{value}", grid=[i, 1], align="left")
        i = i + 1
    PushButton(window, text="Save", command=close_window, grid=[i, 0])
    PushButton(window, text="Cancel", command=save_settings, grid=[i, 1])

    window.hide()

    #cancel_button = PushButton(window, text="Cancel", command=close_window)
    return window


# create app
app = App(title="Conveyor Image Capture",
          width=settings['window_width'], height=settings['window_height'])
app.when_closed = shutdown_cleanup

settings_window = create_settings_window

calibration_window = Window(app, title="Calibration")
calibration_window.hide()

view_pictures_window = Window(app, title="Pictures")
view_pictures_window.hide()

# init the menu bar
menubar = MenuBar(app,
                  toplevel=["File", "Edit", ],
                  options=[
                      [["New Lot", new_lot], ["Open Lot", open_lot], [
                          "Edit Lot Name", edit_lot], ["View Pictures", view_pictures]],
                      [["Change Settings", settings_window_handler],
                          ["Calibration", calibration]],
                  ])
#chnge font later
# print(type(menubar._get_tk_config("font")))

title_box = Box(app, width="fill", align="top", border=True)
title_text = Text(title_box, text="Creat a new lot or open one",size=20, font="Arial")

buttons_box = Box(app, width="fill", align="bottom", border=True)
Text(buttons_box, text="CONVEYOR CONTROLS",size=20, font="Arial")
stop_conveyor_button = PushButton(buttons_box, text="Stop Conveyor",
                                  command=turn_off_plug, align="left", width="fill", height="fill", pady=20)
stop_conveyor_button.text_size= 20
start_conveyor_button = PushButton(buttons_box, text="Start Conveyor",
                                   command=turn_on_plug, align="left", width="fill", height="fill", pady=20)
start_conveyor_button.text_size= 20


options_box = Box(app, height="fill", align="right", border=True)
Text(options_box, text="options")

content_box = Box(app, align="top", width="fill", border=True)
Text(content_box, text="content")

# form_box = Box(content_box, layout="grid",
#                width="fill", align="left", border=True)
# Text(form_box, grid=[0, 0], text="form", align="right")
# Text(form_box, grid=[0, 1], text="label", align="left")
# TextBox(form_box, grid=[1, 1], text="data", width="fill")


app.display()
