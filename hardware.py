# https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
import sys
import glob
import serial

def check_os():
    if sys.platform.startswith('win'):
        return ("win")
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        return("linux")
    elif sys.platform.startswith('darwin'):
        return("mac")

def serial_ports():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if check_os()=="win":
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif check_os()=="linux":
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif check_os()=="mac":
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def reload_comport():
    comport_list = []
    for isi in serial_ports():
        comport_list.append(str(isi))
    return comport_list
