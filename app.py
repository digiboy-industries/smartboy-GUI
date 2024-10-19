# Created by        : @aviezab
# First Written     : 2024 10 16
import dearpygui.dearpygui as dpg
from math import sin
from hardware import reload_comport
from jendela import SensorWindow, trigger_error, light_brown_window, get_resolution \
    , dark_gray_window

global com_sett
global comport_list
global sensor_names
com_sett = {"port1" : None, "port2" : None}
comport_list = []
comport_list = reload_comport()
sensor_names = {}

def print_me(sender):
    print(f"Menu Item: {sender}")

################
# Window Utils #
################
def show_comm_setting():
    dpg.show_item("comm_sett_window")

def reload_comm_window(sender, app_data, user_data):
    global comport_list
    comport_list = reload_comport()
    dpg.delete_item("comm_sett_window")
    comm_window(sender=None, app_data=None, user_data={"comport": comport_list})    

def keluar():
    dpg.destroy_context()
    exit()

def get_combo_item(sender, app_data, user_data):
    # app_data contains the selected value
    selected_value = app_data
    if user_data["status"] == 1:
        com_sett["port1"] = str(selected_value)
    if user_data["status"] == 2:
        com_sett["port2"] = str(selected_value)
    return str(selected_value)

def spawn_4windows(sender, app_data, user_data):
    if (user_data["range1"] == 1) and (user_data["range2"] == 5):
        if com_sett["port1"] == None:
            trigger_error(user_data={"error_msg": "No Comm Port Selected! Please select first"}, sender=sender)
        else:
            for i in range(user_data["range1"], user_data["range2"]):
                if dpg.does_item_exist(i):
                     dpg.delete_item(i)
                SensorWindow(label=f"Sensor {i}", width=240, pos=((i-1)*244, 25), window_id=i, no_close=True)
            dpg.hide_item("comm_sett_window")
    
    if (user_data["range1"] == 5) and (user_data["range2"] == 9):
        if com_sett["port2"] == None:
            trigger_error(user_data={"error_msg": "No Comm Port Selected! Please select first"}, sender=sender)
        else:
            for i in range(user_data["range1"], user_data["range2"]):
                if dpg.does_item_exist(i):
                     dpg.delete_item(i)
                SensorWindow(label=f"Sensor {i}", width=240, pos=((i-5)*244, 395), window_id=i, no_close=True)
            dpg.hide_item("comm_sett_window")

dpg.create_context()


with dpg.font_registry():
    # first argument is the path to the .ttf or .otf file
    default_font = dpg.add_font("BAHNSCHRIFT.TTF", 20)
    f15 = dpg.add_font("BAHNSCHRIFT.TTF", 15)


with dpg.viewport_menu_bar():
    with dpg.menu(label="File"):
        dpg.add_menu_item(label="Save", callback=print_me)
        dpg.add_menu_item(label="Exit", callback=keluar)
    with dpg.menu(label="Settings"):
        dpg.add_menu_item(label="Comm Port Setting", callback=show_comm_setting, check=False)
        dpg.add_menu_item(label="Sensor Setting & Calibration", callback=print_me)

# Comm Port Setting Window
def comm_window(sender, app_data, user_data):
    with dpg.window(label="Communication Port Setting", width=250, tag="comm_sett_window", pos=(400,300)):
        dpg.bind_item_theme(dpg.last_item(), light_brown_window())
        dpg.bind_item_font(dpg.last_item(), f15)
        dpg.add_button(label="Reload Port List", callback=reload_comm_window)
        dpg.add_text("Modul 1 Comm Port: ")
        dpg.add_combo(user_data["comport"], tag=101, callback=get_combo_item, user_data={"status" : 1})
        dpg.add_button(label="Execute", callback=spawn_4windows, user_data={"range1":1, "range2":5})
        dpg.add_text("Modul 2 Comm Port: ")
        dpg.add_combo(user_data["comport"], tag=102, callback=get_combo_item, user_data={"status" : 2})
        dpg.add_button(label="Execute", callback=spawn_4windows, user_data={"range1":5, "range2":9})

def sensor_sett_window(sender, app_data, user_data):
    with dpg.window(label="Sensor Setting & Calibration", width=400, tag="sensor_sett_window", pos=(300, 300)):
        dpg.bind_item_theme(dpg.last_item(), light_brown_window())
        dpg.bind_item_font(dpg.last_item(), f15)        
        with dpg.group(horizontal=True):
            dpg.add_text("Sensor 1 Name    :")
            dpg.add_input_text(label="", tag="sens1", width=200)            
        with dpg.group(horizontal=True):
            dpg.add_text("Sensor 1 min value:")
            dpg.add_input_text(label="", tag="sens1_min", width=200)
        with dpg.group(horizontal=True):            
            dpg.add_text("Sensor 1 max value:")
            dpg.add_input_text(label="", tag="sens1_max", width=200)
        with dpg.group(horizontal=True):
            dpg.add_text("Sensor 1 input type:")
            dpg.add_combo(["voltage", "current"], tag="sens1_type", width=200)
        with dpg.group(horizontal=True):
            dpg.add_text("Sensor 1 min unit")







# dpg.set_viewport_small_icon("path/to/small_icon.ico")
# dpg.set_viewport_large_icon("path/to/large_icon.ico")

comm_window(sender=None, app_data=None, user_data={"comport": comport_list})
sensor_sett_window(sender=None, app_data=None, user_data=None)
# Hide Popup Windows
dpg.hide_item("comm_sett_window")

dpg.create_viewport(title='Smartboy GUI', width=1024, height=768, resizable=False)
#put viewport to the center of screen
dpg.set_viewport_pos([get_resolution()[0]/4, get_resolution()[1]/8])
dpg.setup_dearpygui()
dpg.show_viewport()
#dpg.show_item_registry()



# below replaces, start_dearpygui()
while dpg.is_dearpygui_running():
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()
    # print("this will run every frame")
    # print(dpg.get_viewport_pos())
    dpg.render_dearpygui_frame()

dpg.destroy_context()