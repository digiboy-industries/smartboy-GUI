import dearpygui.dearpygui as dpg
import random
from PIL import ImageGrab

class SensorWindow:
    def __init__(self, label, width, pos, window_id, **kwargs):
        self.label = label
        self.width = width
        self.pos = pos
        self.window_id = window_id
        self.font = kwargs.get("font", None)
        self.no_close = kwargs.get("no_close", False)
        self.height = kwargs.get("height", 300)
        # Data for plotting as class properties
        self.sindatax = []
        self.sindatay = []
        self.generate_data()

        # Create the window
        self.create_window()

    def generate_data(self):
        """Generate data for plotting."""
        for i in range(0, 500):
            self.sindatax.append(i / 1000)
            self.sindatay.append(random.randrange(0, 10, 1))

    def create_window(self):
        """Create the window and plot inside it."""
        with dpg.window(label=self.label, width=self.width, pos=self.pos, id=self.window_id, no_close=self.no_close,
                        height=self.height):
            if self.font: dpg.bind_font(self.font)
            btn = dpg.add_button(label="", callback=self.get_window_position)
            dpg.set_item_label(btn, "Button 57")
            dpg.set_item_width(btn, self.width-15)

            # Create the plot as part of the class
            self.create_plot()

    def create_plot(self):
        """Create the plot inside the window."""
        with dpg.plot(label="Line Series", height=self.height-90, width=self.width-15):
            # Optionally create legend
            dpg.add_plot_legend()
            # Create x and y axes
            dpg.add_plot_axis(dpg.mvXAxis, label="x")
            dpg.add_plot_axis(dpg.mvYAxis, label="y", tag=f"y_axis_{self.window_id}")

            # Add the line series using the class properties
            dpg.add_line_series(self.sindatax, self.sindatay, parent=f"y_axis_{self.window_id}")
    
    def get_window_position(self, sender, app_data, user_data):
        """Callback function to get and print the window position."""
        window_pos = dpg.get_item_pos(self.window_id)
        print(f"Window {self.window_id} Position: {window_pos}")


class ErrorMessageBox:
    def __init__(self, message="An error occurred!"):
        self.message = message
        self.window_id = dpg.generate_uuid()  # Generate a unique ID for the error window
        self.pos = (376, 300)

    def show(self):
        """Displays the error message in a popup window."""
        with dpg.window(label="Error", modal=True, no_title_bar=True, id=self.window_id, pos=self.pos):
            dpg.add_text(self.message)
            dpg.add_button(label="Close", callback=self.close)

    def close(self, sender, app_data=None, user_data=None):
        """Closes the error window."""
        dpg.delete_item(self.window_id)

import dearpygui.dearpygui as dpg
import datetime

class AboutWindow:
    def __init__(self):
        """Initialize the About window but don't show it yet."""
        self.window_tag = "about_window"

    def show(self):
        """Creates and shows the About window."""
        with dpg.window(label="About", width=500, height=300, tag=self.window_tag, pos=(250, 200), no_resize=True, no_collapse=True):
            dpg.add_text("Tangerang Selatan, Indonesia", pos=(280, 25))  # Location and flag at top right
            dpg.add_spacer(height=12)
            with dpg.group(horizontal=False):  # Main content area
                # Frame to show text
                with dpg.child_window(height=150, border=True):
                    dpg.add_text("""Smartboy GUI is graphical interface application to aqcuire data from the industrial sensors.
This program is able to record up to 8 sensors simultaneously and record it to a database.
Author dedicated this programm to his sons: Musa and Eisa."""
                                 , wrap=450)
                    
            
            # Dynamic date and time label
            dpg.add_text(self.get_current_datetime(), tag="date_time_label")  # Below the main text
            
            # Hyperlink to digiboy.com
            dpg.add_text("Visit: ")
            dpg.add_text("https://digiboy.com", color=(50, 188, 255), bullet=True)  # Center bottom link
            dpg.add_text("author: aviezab © 2024")
            
            # OK Button
            dpg.add_button(label="OK", pos=(200, 250), width=250, callback=self.close)

    def close(self, sender, app_data, user_data):
        """Close the About window."""
        dpg.delete_item(self.window_tag)

    def update_datetime_label(self):
        """Updates the datetime label in the About window."""
        dpg.set_value("date_time_label", self.get_current_datetime())

    def get_current_datetime(self):
        """Gets the current date and time as a string."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def dark_gray_window():
    """Creates a custom theme for the window background and text color."""
    # Create a new theme for the window
    with dpg.theme() as window_theme:
        with dpg.theme_component(dpg.mvAll):
            # Set window background color
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (50, 50, 50, 255))  # Dark gray
    return window_theme
            
def light_brown_window():
    """Creates a custom theme for the window background and text color."""
    # Create a new theme for the window
    with dpg.theme() as window_theme:
        with dpg.theme_component(dpg.mvAll):
            # Set window background color
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (181, 101, 29, 255)) # Light brown
    return window_theme

def get_resolution():
    img = ImageGrab.grab()
    return img.size[0], img.size[1]

def trigger_error(sender=None, app_data=None, user_data=None):
    error_box = ErrorMessageBox(f"Error: {user_data['error_msg']}")
    error_box.show()