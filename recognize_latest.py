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
from modules.camera_funcs import Camera
from modules.plug import turn_off_plug, turn_on_plug

STATE = {
    "LOTNAME": None
}


settings = load_settings()
init_gpio()
camera = Camera()

Path(settings['debug_directory']).mkdir(parents=True, exist_ok=True)

logging.basicConfig(filename=settings["debug_directory"] + 'app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')


def destroy_kids(widgets):
    for widget in widgets:
        for e in widget.children:
            print(e)
            e.destroy()


def take_picture_handler():
    camera.capture_image(STATE["LOTNAME"])
    show_picture(camera.last_picture)


def shutdown_cleanup():
    print("running cleanup")
    # asyncio.run(turn_off_plug())
    turn_off_plug()
    app.destroy()


def settings_window_handler():
    """Function to handle settings window"""
    settings_window.show(wait=True)


def new_lot():
    print("new lot")
    STATE["LOTNAME"] = app.question(
        "New Lot Number", "What is the lot number?")
    lotname = STATE["LOTNAME"]

    if lotname is not None and len(lotname) > 0:
        try:

            print(lotname)
            GPIO.remove_event_detect(40)
            pictures_path = Path(settings['pictures_directory']) / lotname

            # lot already exists check
            pictures_path.mkdir(parents=True, exist_ok=False)

            # init cameras
            logging.debug("Starting Camera Preview")
            camera.camera.start_preview()
            sleep(2)
            # capture_image(lotname ,camera)

            # starting conveyor
            # asyncio.run(turn_on_plug())
            turn_on_plug()

            # simulate

            sim = partial(simulation, lotname)
            app.after(3000, sim)
            app.after(6000, sim)
            app.after(8000, sim)
            app.after(12000, sim)

            # set up beam
            # GPIO.add_event_detect(settings['beam_pin'], GPIO.BOTH, callback=beam_break_cb)

            # update UI
            destroy_kids([title_box, options_box])
            destroy_kids([options_box])
            title_text = Text(
                title_box, text=f"Lot: {lotname}", size=20, font="Arial")
            take_picture_button = PushButton(
                options_box, text="Take Picture", align="left", width="fill", height="fill", pady=20)
            take_picture_button.text_size = 20

            take_picture_button.when_clicked = take_picture_handler

        except:
            print(traceback.format_exc())

    else:
        app.error("No lotname", "You must enter a lot name")


def open_lot():
    pictures_dir = settings["pictures_directory"]
    file_path = filedialog.askdirectory(
        initialdir=pictures_dir, title="Select Lot")
    print(Path(file_path).stem)
    STATE["LOTNAME"] = Path(file_path).stem
    lotname = STATE["LOTNAME"]

    if lotname is not None and len(lotname) > 0:
        print(len(lotname))
        # fix when nothing is selevted you get a blank folder error
        GPIO.remove_event_detect(40)
        # init camera
        camera.camera.start_preview(fullscreen=False,
                                    window=(settings['gui_preview_x'],
                                            settings['gui_preview_y'],
                                            settings['picture_width'],
                                            settings['picture_height']))
        sleep(2)  # sleep to let camera's sensors adjust

        # update UI
        destroy_kids([title_box, options_box])
        destroy_kids([options_box])
        title_text = Text(
            title_box, text=f"Lot: {lotname}", size=20, font="Arial")
        take_picture_button = PushButton(
            options_box, text="Take Picture", align="left", width="fill", height="fill", pady=20)
        take_picture_button.text_size = 20

        take_picture_button.when_clicked = take_picture_handler

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
        camera.capture_image(STATE["LOTNAME"])
        show_picture()


def beam_break_cb_simulation(lot):
    print('Input was LOW')
    camera.capture_image(lot)
    show_picture(camera.last_picture)


def simulation(lot):
    turn_off_plug()
    beam_break_cb_simulation(lot)
    turn_on_plug()


def show_picture(path):
    global content_box
    destroy_kids([content_box])
    picture = Picture(content_box, image=path, grid=[
                      0, 1, 4, 1], width=settings['picture_width'], height=settings['picture_height'])


def view_pictures():
    pass

# # Program to demonstrate conditional operator 
# a, b = 10, 20
  
# # Copy value of a in min if a < b else copy b 
# min = a if a < b else b 

def serialize(lst):
    dic = {}
    for i in range(0,len(lst),2):
        key = lst[i].value
        value = int(lst[i+1].value) if lst[i+1].value.isdigit() else lst[i+1].value
        dic[key] = value 
    return dic

def save_btn_handler():
    lst = settings_box.children
    # settings_dict = {lst[i].value: lst[i + 1].value for i in range(0, len(lst), 2)}
    settings_dict = serialize(lst)
    print(settings_dict)
    save_settings(settings_dict)


def cancel_btn_handler():
    settings_window.hide()


# create app
app = App(title="Conveyor Image Capture",
          width=settings['window_width'], height=settings['window_height'])
app.when_closed = shutdown_cleanup

# settings window
settings_window = Window(app, title="Settings",
                         width=settings['window_width'], height=settings['window_height'])
settings_window.hide()

# create ui
settings_box = Box(settings_window, layout="grid")
i = 0
for key, value in settings.items():
    txt = Text(settings_box, text=f"{key}", grid=[0, i], align="left", size=16)
    txtBox = TextBox(settings_box, text=f"{value}", grid=[
                     1, i], align="left", width=30)
    txtBox.text_size = 16
    i = i + 1

save_btn = PushButton(settings_window, text="Save",
                      align="left", width="fill", height="fill", pady=20)
save_btn.when_clicked = save_btn_handler
save_btn.text_size = 20
cancel_btn = PushButton(settings_window, text="Cancel",
                        align="left", width="fill", height="fill", pady=20)
cancel_btn.when_clicked = cancel_btn_handler
cancel_btn.text_size = 20


view_pictures_window = Window(app, title="Pictures")
view_pictures_window.hide()

# init the menu bar
menubar = MenuBar(app,
                  toplevel=["Lots", "Edit"],
                  options=[
                      [["New Lot", new_lot], ["Open Lot", open_lot], [
                          "Edit Lot Name", edit_lot], ["View Pictures", view_pictures]],
                      [["Change Settings", settings_window_handler]],
                  ])
# chnge font later
# print(type(menubar._get_tk_config("font")))


# main window
title_box = Box(app, width="fill", align="top", border=True)
title_text = Text(
    title_box, text="Creat a new lot or open one", size=20, font="Arial")

buttons_box = Box(app, width="fill", align="bottom", border=True)
Text(buttons_box, text="CONVEYOR CONTROLS", size=20, font="Arial")
stop_conveyor_button = PushButton(buttons_box, text="Stop Conveyor",
                                  command=turn_off_plug, align="left", width="fill", height="fill", pady=20)
stop_conveyor_button.text_size = 20
start_conveyor_button = PushButton(buttons_box, text="Start Conveyor",
                                   command=turn_on_plug, align="left", width="fill", height="fill", pady=20)
start_conveyor_button.text_size = 20


options_box = Box(app, height="fill", align="right", border=True)
Text(options_box, text="Camera Functions")
take_picture_button = PushButton(options_box, text="Take Picture",
                                 command=camera.debug_image, align="left", width="fill", height="fill", pady=20)
take_picture_button.text_size = 20

content_box = Box(app, align="top", width="fill", border=True)
Text(content_box, text="content")

# form_box = Box(content_box, layout="grid",
#                width="fill", align="left", border=True)
# Text(form_box, grid=[0, 0], text="form", align="right")
# Text(form_box, grid=[0, 1], text="label", align="left")
# TextBox(form_box, grid=[1, 1], text="data", width="fill")


app.display()
