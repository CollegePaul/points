"""
Creates a web page (will automatically get device adress)
PI - GPIO 2 - SDA   then on my nano I have A4
     GPIO 3 - SCL                          A5



"""



from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from smbus2 import SMBus
import time
import socket

# I2C address of the Arduino
I2C_ADDRESS = 0x08

lines = [0,0]  # central, other - both set to off

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def write_to_arduino(data):
    with SMBus(1) as bus:  # Use I2C bus 1
        try:
            bus.write_byte(I2C_ADDRESS, data)
            print(f"Data sent to Arduino: {data}")
        except Exception as e:
            print(f"Error writing to Arduino: {e}")

def updateState():
    x, y = lines
    val =  bin(x * 2 + y)  
    write_to_arduino(val)
    print("WRITING STATE: ", val)


app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('map.html')

@socketio.on('button_pressed')
def handle_button_press(data): 
    print(f"Button pressed: {data}")  # Receive and print the button's value
    emit('response', {'message': f"Button {data} pressed!"})

    # update button values
    if lines[data-1] == 0:    # button 1 is data-1  hence 0 index in line
        lines[data-1] = 1
    else:
        lines[data-1] = 0

    updateState()


if __name__ == '__main__':  #ensure this is is run as the main program
    ip = get_ip()
    print("Server Running on: ", ip)
    socketio.run(app, debug=True, host=ip, port=5000)