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
import sys

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
    global lines
    if lines[0] == 0 and lines[1]==0:
         print("Both lines off")
         write_to_arduino(0b00)
    if lines[0] == 1 and lines[1]==1:
         print("Both lines on")
         write_to_arduino(0b11)
    if lines[0] == 1 and lines[1]==0:
         print("Central line on")
         write_to_arduino(0b10)
    if lines[0] == 0 and lines[1]==1:
         print("Other line on")
         write_to_arduino(0b01)

app = Flask(__name__)
socketio = SocketIO(app)
print(type(socketio))

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

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    lines = [0,0]
    updateState()

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    global lines
    lines = [0,0]
    updateState()


if __name__ == '__main__':  #ensure this is is run as the main program
    ip = get_ip()
    print("Server Running on: ", ip)
    socketio.run(app, debug=True, host=ip, port=5000)