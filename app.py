# بِسْمِ ٱللَّٰهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ
# Created by        : @aviezab
# First Written     : 2024 10 16
import json
from time import sleep
import threading
import serial
import dearpygui.dearpygui as dpg
from hardware import reload_comport
from jendela import RPM_SensorWindow,SensorWindow, AboutWindow, trigger_error, \
    light_brown_window, get_resolution, dark_gray_window, \
    dark_purple, dark_green
from basisdata import save_to_db

settings = None
v_execute1 = False
v_execute2 = False
com_sett = {"port1" : None, "port2" : None}
comport_list = []
comport_list = reload_comport()
comm_deployed = False
null_literal = "S1=0.00mA;0.00mV;S2=0.00mA;0.00mV;S3=0.00mA;0.00mV;S4=0.00mA;0.00mV;"
raw_data1 = None
raw_data2 = None
nyala = True
sensor_graph = \
{ "1": {"x": [], "y":[]}, "2": {"x": [], "y":[]}, "3": {"x": [], "y":[]}, "4": {"x": [], "y":[]}, 
"5": {"x": [], "y":[]}, "6": {"x": [], "y":[]}, "7": {"x": [], "y":[]}, "8":{"x": [], "y":[]} }

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
                "interval" : 1,
                "sensor_data" : {
                "1": {"name": "", "type": "current", "min": 0, "max" :0, "minunit" :0, "maxunit": 0, "unit": "", "active": True}, 
                "2": {"name": "", "type": "current", "min": 0, "max" :0, "minunit" :0, "maxunit": 0, "unit": "", "active": True}, 
                "3": {"name": "", "type": "current", "min": 0, "max" :0, "minunit" :0, "maxunit": 0, "unit": "", "active": True}, 
                "4": {"name": "", "type": "current", "min": 0, "max" :0, "minunit" :0, "maxunit": 0, "unit": "", "active": True}, 
                "5": {"name": "", "type": "current", "min": 0, "max" :0, "minunit" :0, "maxunit": 0, "unit": "", "active": True}, 
                "6": {"name": "", "type": "current", "min": 0, "max" :0, "minunit" :0, "maxunit": 0, "unit": "", "active": True}, 
                "7": {"name": "", "type": "current", "min": 0, "max" :0, "minunit" :0, "maxunit": 0, "unit": "", "active": True}, 
                "8": {"name": "", "type": "current", "min": 0, "max" :0, "minunit" :0, "maxunit": 0, "unit": "", "active": True}
                                }
            }
        }
    return state
settings = load_state()

def apf(y, xmin, xmax, ymin, ymax):
    # h =  xmin + ((y - ymin)*(xmax-xmin) / (ymax - ymin))
    try:
        y = float(y)
        ymin = float(ymin)
        ymax = float(ymax)
        xmin = float(xmin)
        xmax = float(xmax)
        pertama = y - ymin
        kedua = xmax - xmin
        ketiga = ymax - ymin
        keempat = pertama * kedua
        kelima = keempat / ketiga
        hasil = xmin + (kelima)
        hasil = round(hasil, 3)
        return hasil
    except ZeroDivisionError:
        return 0
    except Exception as e:
        print(e)

def fetch_serial_data():
    global v_execute1
    global v_execute2
    global raw_data1
    global raw_data2
    global ser1
    global ser2
    global nyala
    nyala = True
    while (nyala):
        try:
            if v_execute1 and v_execute2:
                # print("R1R2")
                if ser1.is_open and ser2.is_open:
                    raw_data1 = ser1.readline().decode('utf-8').strip()
                    raw_data2 = ser2.readline().decode('utf-8').strip()
                    ser1.flushInput()
                    ser2.flushInput()
                    # print(raw_data1)
                    # print(raw_data2)
            if v_execute1:
                # print("R1")
                if ser1.is_open:
                    raw_data1 = ser1.readline().decode('utf-8').strip()
                    # print(raw_data1)
                    ser1.flushInput()
            if v_execute2:
                # print("R2")
                if ser2.is_open:
                    raw_data2 = ser2.readline().decode('utf-8').strip()
                    # print(raw_data2)
                    ser2.flushInput()
            sleep(float(settings["settings"]["interval"]))
        except Exception as e:
            print(e)

def parse_sensor_data(data_a, data_b):
    sensor_data = {}
    # Parse Data A
    if data_a and "XR=" in data_a:
        segments = data_a.split(";")
        for segment in segments:
            if segment.startswith("XR"):
                rpm_data = segment.split("=")[1]
                rpm_data = rpm_data.replace("rpm", "")
                sensor_data["XRPM"] = {}
                sensor_data["XRPM"]["rpm"] = int(rpm_data)
            elif "S" in segment:
                sensor_id, values = segment.split("=")
                sensor_data[sensor_id] = {}
                current_value = values.replace("mA", "")
                sensor_data[sensor_id]["current"] = current_value
            elif "mV" in segment:
                voltage_value = segment.replace("mV", "")
                sensor_data[sensor_id]["voltage"] = float(voltage_value)

    # Parse Data B
    if data_b:
        segments = data_b.split(";")
        sensor_offset = 5  # Start at S5 for data_b
        for segment in segments:
            if "S" in segment:
                _, values = segment.split("=")
                sensor_data[f"S{sensor_offset}"] = {}
                current_value = values.replace("mA", "")
                sensor_data[f"S{sensor_offset}"]['current'] = current_value
            elif "mV" in segment:
                voltage_value = segment.replace('mV', '')
                sensor_data[f"S{sensor_offset}"]['voltage'] = float(voltage_value)
                sensor_offset += 1
    # if("S1" and "S2" and "S3" and "S4" in sensor_data):
    return sensor_data
    # else:
        # return ""
                   
def print_me(sender):
    print(f"Menu Item: {sender}")

################
# Window Utils #
################
def show_comm_setting():
    global comm_deployed
    if comm_deployed: reload_comm_window(sender=None, app_data=None, user_data=None)
    else: comm_window(sender=None, app_data=None, user_data={"comport": comport_list})

def show_sensor_sett_setting():
    sensor_sett_window(sender=None, app_data=None, user_data=None)

def show_interval_setting():
    interval_sett_window(sender=None, app_data=None, user_data=None)

def reload_comm_window(sender, app_data, user_data):
    global comport_list
    comport_list = reload_comport()
    dpg.delete_item("comm_sett_window")
    comm_window(sender=None, app_data=None, user_data={"comport": comport_list})    

def delete_window(sender, app_data, user_data):
    dpg.delete_item(sender)

def keluar():
    dpg.stop_dearpygui()
    save_state(settings)
    dpg.destroy_context()
    exit()

def get_combo_item(sender, app_data, user_data):
    # app_data contains the selected value
    global com_sett
    selected_value = app_data
    if user_data["status"] == 1:
        com_sett["port1"] = str(selected_value)
    if user_data["status"] == 2:
        com_sett["port2"] = str(selected_value)
    return str(selected_value)

def spawn_4windows(sender, app_data, user_data):
    global ser1
    global ser2
    global v_execute1
    global v_execute2
    global com_sett
    if (user_data["range1"] == 1) and (user_data["range2"] == 5):
        if com_sett["port1"] == None:
            trigger_error(user_data={"error_msg": "No Comm Port Selected! Please select first"}, sender=sender)
        else:
            sername = com_sett["port1"]
            try:
                ser1 = serial.Serial(sername, 115200, timeout=1)
                v_execute1 = True
                RPM_SensorWindow(label="RPM Sensor", width=200, pos=(650, 300), window_id="rpm_window", no_close=False,
                                 font=default_font)
                for i in range(user_data["range1"], user_data["range2"]):
                    if dpg.does_item_exist(i):
                        dpg.delete_item(i)
                    labeli = f"Sensor {i} - " + settings["settings"]["sensor_data"][str(i)]["name"]
                    SensorWindow(label=labeli, width=240, pos=((i-1)*244, 25), window_id=i, no_close=True)
            except serial.SerialException as e:
                pesan = "Comm Port " + sername + " already used!"
                trigger_error(user_data={"error_msg": pesan}, sender=sender)
            if v_execute2 == True: dpg.delete_item("comm_sett_window")

    
    if (user_data["range1"] == 5) and (user_data["range2"] == 9):
        if com_sett["port2"] == None:
            trigger_error(user_data={"error_msg": "No Comm Port Selected! Please select first"}, sender=sender)
        else:
            sername = com_sett["port2"]
            try:
                ser2 = serial.Serial(sername, 115200, timeout=1)
                v_execute2 = True
                for i in range(user_data["range1"], user_data["range2"]):
                    if dpg.does_item_exist(i):
                        dpg.delete_item(i)
                    labeli = f"Sensor {i} - " + settings["settings"]["sensor_data"][str(i)]["name"]
                    SensorWindow(label=labeli, width=240, pos=((i-5)*244, 395), window_id=i, no_close=True)
            except serial.SerialException as e:
                pesan = "Comm Port " + sername + " already used!"
                trigger_error(user_data={"error_msg": pesan}, sender=sender)
            if v_execute1 == True: dpg.delete_item("comm_sett_window")
    return

def append_for_graphs():
    # Output for this example from parse_sensor_data():
    # {'S5': {'current': -2.5, 'voltage': 400.0}, 'S6': {'current': -2.5, 'voltage': 0.0}, 
    # 'S7': {'current': -2.5, 'voltage': 6.25}, 'S8': {'current': -3.75, 'voltage': 22.5} }
    global sensor_graph
    global settings
    global v_execute1
    global v_execute2
    global nyala
    y, ymin, ymax, xmin, xmax, h = 0, 0, 0, 0, 0, 0
    sltime = float(settings["settings"]["interval"])
    while(nyala):
        sens_dict = {}
        try:
            temp = parse_sensor_data(raw_data1, raw_data2)
            # print(temp)
            for i in range(1, 9):
                sensor_key = f"S{i}"
                if "XRPM" in temp:
                    dpg.set_value("rpm_windowrpm_val", str(temp["XRPM"]["rpm"]))
                    sens_dict["XRPM"] = int(temp["XRPM"]["rpm"])
                if sensor_key in temp:
                    # sensor_window.update_label(parsed_data[sensor_key])
                    sens_dict[sensor_key] = {}
                    sens_dict[sensor_key]["voltage"] = float(temp[sensor_key]["voltage"])
                    sens_dict[sensor_key]["current"] = float(temp[sensor_key]["current"])
                    if settings["settings"]["sensor_data"][str(i)]["type"] == "voltage":
                        y = temp[sensor_key]["voltage"]
                    elif settings["settings"]["sensor_data"][str(i)]["type"] == "current":
                        y = temp[sensor_key]["current"]
                    y = float(y)
                    ymin = settings["settings"]["sensor_data"][str(i)]["min"]
                    ymax = settings["settings"]["sensor_data"][str(i)]["max"]
                    xmax = settings["settings"]["sensor_data"][str(i)]["maxunit"]
                    xmin = settings["settings"]["sensor_data"][str(i)]["minunit"]
                    h = apf(y, xmin, xmax, ymin, ymax) # h is result
                    if (y>0):
                        h = h
                    elif(y<0 and y<ymin):
                        h = 0
                    else: 
                        h = round(h, 3)
                    nam = settings["settings"]["sensor_data"][str(i)]["name"]
                    un = settings["settings"]["sensor_data"][str(i)]["unit"]
                    sens_dict[sensor_key]["name"] = nam
                    sens_dict[sensor_key]["value"] = h
                    sens_dict[sensor_key]["unit"] = un
                    sensor_graph[str(i)]["y"].append(h)
                    sensor_graph[str(i)]["x"].append(len(sensor_graph[str(i)]["y"]))
                    l_name = "plot" + str(i)
                    b_name = "btn" + str(i)
                    b_lbl = str(h) + un
                    dpg.configure_item(l_name, x=sensor_graph[str(i)]["x"], y=sensor_graph[str(i)]["y"])
                    # Force axis rescale to refresh the graph
                    dpg.fit_axis_data(l_name+"x")
                    dpg.fit_axis_data(l_name+"y")
                    dpg.set_item_label(b_name, b_lbl)
                else:
                    pass
                    # sensor_window.update_label("No Data")
            # print(sens_dict)
            statsave = save_to_db(sens_dict)
            sleep(sltime)
        except Exception as e:
            print(e)
            sleep(sltime)
            pass
        
# Create GUI Context
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
        dpg.add_menu_item(label="Interval Time Setting", callback=show_interval_setting)

# Comm Port Setting Window
def comm_window(sender, app_data, user_data):
    global comm_deployed
    comm_deployed = True
    with dpg.window(label="Communication Port Setting", width=250, 
                    tag="comm_sett_window", pos=(400,300), on_close=delete_window):
        dpg.bind_item_theme(dpg.last_item(), light_brown_window())
        dpg.bind_item_font(dpg.last_item(), f15)
        dpg.add_button(label="Reload Port List", callback=reload_comm_window)
        dpg.add_text("Modul 1 Comm Port: ")
        dpg.add_combo(user_data["comport"], tag="combo_com1", callback=get_combo_item, user_data={"status" : 1})
        dpg.add_button(label="Execute", callback=spawn_4windows, user_data={"range1":1, "range2":5})
        dpg.add_text("Modul 2 Comm Port: ")
        dpg.add_combo(user_data["comport"], tag="combo_com2", callback=get_combo_item, user_data={"status" : 2})
        dpg.add_button(label="Execute", callback=spawn_4windows, user_data={"range1":5, "range2":9})
        if com_sett["port1"] is not None: dpg.set_value("combo_com1", com_sett["port1"])
        if com_sett["port2"] is not None: dpg.set_value("combo_com2", com_sett["port2"])

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
    with dpg.window(label="Sensor Setting & Calibration", width=400, 
                    tag="sensor_sett_window", pos=(300, 300), on_close=delete_window):
        dpg.bind_item_theme(dpg.last_item(), dark_purple())
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
        dpg.add_spacer()
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=150)
            dpg.add_button(label="Save", tag="btn_save_sensor", callback=save_sensor_settings)

def interval_save(sender, app_data, user_data):
    if dpg.get_value("tinterval") < 0.005:
        settings["settings"]["interval"] = 0.005
        dpg.set_value("tinterval", 0.005)
    else:
        settings["settings"]["interval"] = dpg.get_value("tinterval")

# Interval Acq Setting Window
def interval_sett_window(sender, app_data, user_data):
    with dpg.window(label="Interval Acquisition Setting", width=400, 
                    tag="interval_sett_window", pos=(300, 300), on_close=delete_window):
        dpg.bind_item_theme(dpg.last_item(), dark_green())
        dpg.bind_item_font(dpg.last_item(), f15)                    
        dpg.add_spacer(height=10)
        with dpg.group(horizontal=True):            
            dpg.add_text("Time interval (s) :")
            dpg.add_input_float(label="", tag="tinterval", width=200)
            dpg.set_value("tinterval", settings["settings"]["interval"])
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=150)
            dpg.add_button(label="Save", tag="btn_save_inter", callback=interval_save)

# dpg.set_viewport_small_icon("path/to/small_icon.ico")
# dpg.set_viewport_large_icon("path/to/large_icon.ico")
about_window = AboutWindow()

dpg.create_viewport(title='Smartboy GUI', width=1024, height=768, resizable=False)
# put viewport to the center of screen
dpg.set_viewport_pos([get_resolution()[0]/4, get_resolution()[1]/8])
dpg.setup_dearpygui()
dpg.show_viewport()

# Serial monitoring multi-threading
serial_thread = threading.Thread(target=fetch_serial_data)
serial_thread.start()
graph_thread = threading.Thread(target=append_for_graphs)
graph_thread.start()

# below replaces, start_dearpygui()
while dpg.is_dearpygui_running():
    # global raw_data1
    # global raw_data2
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()
    dpg.render_dearpygui_frame()

save_state(settings)
try:
    if v_execute1: ser1.close()
    if v_execute2: ser2.close()
except:
    pass
v_execute1 = False
v_execute2 = False
nyala = False
serial_thread.join()
graph_thread.join()
dpg.destroy_context()