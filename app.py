# Created by        : @aviezab
# First Written     : 2024 10 16
import json
from time import sleep
import serial
import dearpygui.dearpygui as dpg
from hardware import reload_comport
from jendela import SensorWindow, AboutWindow, trigger_error, \
    light_brown_window, get_resolution, dark_gray_window

global com_sett
global comport_list
global settings
global ser1
global ser2
global raw_data1
global raw_data2
com_sett = {"port1" : None, "port2" : None}
comport_list = []
comport_list = reload_comport()

####
# RUMUS LINEAR #
####
# x = (y - ymax) . (xmax - xmin) /  (ymax - ymin)
# x = besaran fisika yang dicari
# y = keluaran sensor dalam mA/ mV
# ymax = bacaan sensor dalam mA/ mV max
# ymin = bacaan sensor dalam mA/ mV min
# xmax = besaran fisika maksimal yang bisa dibaca sensor
# xmin = besaran fisika minimal yang bisa dibaca sensor
STATE_FILENAME = "smartboy-settings.json"

def save_state(state):
    with open(STATE_FILENAME, "w") as f:
        json.dump(state, f, indent=4)

def load_state():
    try:
        with open(STATE_FILENAME, "r") as f:
            state = json.load(f)
    except:
        state = {
            "app_name": "Smartboy GUI",
            "settings": {
                "sensor_data" : {
                "1": {"name": "", "type": "current", "min": 0, "max" :0, "minunit" :0, "maxunit": 0, "unit": "", "active": True}, 
                "2": {"name": "", "type": "current", "min": 0, "max" :0, "minunit" :0, "maxunit": 0, "unit": "", "active": True}, 
                "3": {"name": "", "type": "current", "min": 0, "max" :0, "minunit" :0, "maxunit": 0, "unit": "", "active": True}, 
                "4": {"name": "", "type": "current", "min": 0, "max" :0, "minunit" :0, "maxunit": 0, "unit": "", "active": True}, 
                "5": {"name": "", "type": "current", "min": 0, "max" :0, "minunit" :0, "maxunit": 0, "unit": "", "active": True}, 
                "6": {"name": "", "type": "current", "min": 0, "max" :0, "minunit" :0, "maxunit": 0, "unit": "", "active": True}, 
                "7": {"name": "", "type": "current", "min": 0, "max" :0, "minunit" :0, "maxunit": 0, "unit": "", "active": True}, 
                "8": {"name": "", "type": "current", "min": 0, "max" :0, "minunit" :0, "maxunit": 0, "unit": "", "active": True}
                                },
            "interval" : 1
            }
        }
    return state
settings = load_state()

def fetch_serial_data():
    if ser1.is_open and ser2.is_open:
            raw_data1 = ser1.readline().decode('utf-8').strip()
            raw_data2 = ser2.readline().decode('utf-8').strip()
            sleep(float(settings["settings"]["interval"]))

def print_me(sender):
    print(f"Menu Item: {sender}")

################
# Window Utils #
################
def show_comm_setting():
    dpg.show_item("comm_sett_window")

def show_sensor_sett_setting():
    dpg.show_item("sensor_sett_window")

def reload_comm_window(sender, app_data, user_data):
    global comport_list
    comport_list = reload_comport()
    dpg.delete_item("comm_sett_window")
    comm_window(sender=None, app_data=None, user_data={"comport": comport_list})    

def keluar():
    save_state(settings)
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
                labeli = f"Sensor {i} - " + settings["settings"]["sensor_data"][str(i)]["name"]
                SensorWindow(label=labeli, width=240, pos=((i-1)*244, 25), window_id=i, no_close=True)
            ser1 = serial.Serial(com_sett["port1"], 115200, timeout=1)
            dpg.hide_item("comm_sett_window")
    
    if (user_data["range1"] == 5) and (user_data["range2"] == 9):
        if com_sett["port2"] == None:
            trigger_error(user_data={"error_msg": "No Comm Port Selected! Please select first"}, sender=sender)
        else:
            for i in range(user_data["range1"], user_data["range2"]):
                if dpg.does_item_exist(i):
                     dpg.delete_item(i)
                labeli = f"Sensor {i} - " + settings["settings"]["sensor_data"][str(i)]["name"]
                SensorWindow(label=labeli, width=240, pos=((i-5)*244, 395), window_id=i, no_close=True)
            ser2 = serial.Serial(com_sett["port2"], 115200, timeout=1)
            dpg.hide_item("comm_sett_window")

dpg.create_context()


with dpg.font_registry():
    # first argument is the path to the .ttf or .otf file
    default_font = dpg.add_font("BAHNSCHRIFT.TTF", 20)
    f15 = dpg.add_font("BAHNSCHRIFT.TTF", 15)

with dpg.viewport_menu_bar():
    with dpg.menu(label="File"):
        dpg.add_menu_item(label="About", callback=lambda: about_window.show())
        dpg.add_menu_item(label="Exit", callback=keluar)
    with dpg.menu(label="Settings"):
        dpg.add_menu_item(label="Comm Port Setting", callback=show_comm_setting, check=False)
        dpg.add_menu_item(label="Sensor Setting & Calibration", callback=show_sensor_sett_setting)

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

def load_sensor_settings(sender, app_data, user_data):
    sensor_number = str(dpg.get_value("sensor_selector"))  # Get selected sensor number
    # Load current sensor data into the input fields
    dpg.set_value("sens_type", settings["settings"]["sensor_data"][sensor_number]["type"])
    dpg.set_value("sens_name", settings["settings"]["sensor_data"][sensor_number]["name"])
    dpg.set_value("sens_min", settings["settings"]["sensor_data"][sensor_number]["min"])
    dpg.set_value("sens_max", settings["settings"]["sensor_data"][sensor_number]["max"])
    dpg.set_value("sens_min_unit", settings["settings"]["sensor_data"][sensor_number]["minunit"])
    dpg.set_value("sens_max_unit", settings["settings"]["sensor_data"][sensor_number]["maxunit"])
    dpg.set_value("sens_unit",settings["settings"]["sensor_data"][sensor_number]["unit"])
    
def save_sensor_settings(sender, app_data, user_data):
    sensor_number = str(dpg.get_value("sensor_selector"))  # Get selected sensor number
    # Save the sensor data dictionary with the new values
    settings["settings"]["sensor_data"][sensor_number]["type"] = dpg.get_value("sens_type")
    settings["settings"]["sensor_data"][sensor_number]["name"] = dpg.get_value("sens_name")
    settings["settings"]["sensor_data"][sensor_number]["min"] = dpg.get_value("sens_min")
    settings["settings"]["sensor_data"][sensor_number]["max"] = dpg.get_value("sens_max")
    settings["settings"]["sensor_data"][sensor_number]["minunit"] = dpg.get_value("sens_min_unit")
    settings["settings"]["sensor_data"][sensor_number]["maxunit"] = dpg.get_value("sens_max_unit")
    settings["settings"]["sensor_data"][sensor_number]["unit"] = dpg.get_value("sens_unit")

# Sesor Settings Window
def sensor_sett_window(sender, app_data, user_data):
    with dpg.window(label="Sensor Setting & Calibration", width=400, tag="sensor_sett_window", pos=(300, 300)):
        dpg.bind_item_theme(dpg.last_item(), light_brown_window())
        dpg.bind_item_font(dpg.last_item(), f15)        
        dpg.add_combo(["1", "2", "3", "4", "5", "6", "7", "8"], label="Select Sensor",\
            tag="sensor_selector", default_value="", callback=load_sensor_settings)
        dpg.add_separator()
        with dpg.group(horizontal=True):
            dpg.add_text("Sensor Name       :")
            dpg.add_input_text(label="", tag="sens_name", width=200)            
        with dpg.group(horizontal=True):
            dpg.add_text("Sensor input type :")
            dpg.add_combo(["voltage", "current"], tag="sens_type", width=200)
        with dpg.group(horizontal=True):
            dpg.add_text("Sensor min value  :")
            dpg.add_input_float(label="", tag="sens_min", width=200)
        with dpg.group(horizontal=True):            
            dpg.add_text("Sensor max value  :")
            dpg.add_input_float(label="", tag="sens_max", width=200)
        with dpg.group(horizontal=True):
            dpg.add_text("Sensor min unit   :")
            dpg.add_input_float(label="", tag="sens_min_unit", width=200)
        with dpg.group(horizontal=True):
            dpg.add_text("Sensor max unit   :")
            dpg.add_input_float(label="", tag="sens_max_unit", width=200)
        with dpg.group(horizontal=True):
            dpg.add_text("Sensor unit       :")
            dpg.add_input_text(label="", tag="sens_unit", width=200)
        with dpg.group(horizontal=True):
            dpg.add_separator()
            dpg.add_spacer(width=300)
            dpg.add_button(label="Save", tag="btn_save_sensor", callback=save_sensor_settings)

# dpg.set_viewport_small_icon("path/to/small_icon.ico")
# dpg.set_viewport_large_icon("path/to/large_icon.ico")
about_window = AboutWindow()
comm_window(sender=None, app_data=None, user_data={"comport": comport_list})
sensor_sett_window(sender=None, app_data=None, user_data=None)
# Hide Popup Windows
dpg.hide_item("comm_sett_window")
dpg.create_viewport(title='Smartboy GUI', width=1024, height=768, resizable=False)
#put viewport to the center of screen
dpg.set_viewport_pos([get_resolution()[0]/4, get_resolution()[1]/8])
dpg.setup_dearpygui()
dpg.show_viewport()




# below replaces, start_dearpygui()
while dpg.is_dearpygui_running():
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()

    dpg.render_dearpygui_frame()

save_state(settings)
dpg.destroy_context()