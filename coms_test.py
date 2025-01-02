import smbus
import time

# I2C address of the Arduino
I2C_ADDRESS = 0x08

# Function to send data to the Arduino via I2C
def write_to_arduino(data):
    bus = smbus.SMBus(1)  # Use I2C bus 1
    try:
        bus.write_byte(I2C_ADDRESS, data)
        print(f"Data sent to Arduino: {data}")
    except Exception as e:
        print(f"Error writing to Arduino: {e}")
    finally:
        bus.close()

if __name__ == "__main__":
    while True:
        # Example: Send data to turn on both LEDs
        data_on = 0b11  # Binary for 3 (both bits set)
        write_to_arduino(data_on)
        time.sleep(1)

        # Example: Send data to turn off both LEDs
        data_off = 0b00  # Binary for 0 (both bits cleared)
        write_to_arduino(data_off)
        time.sleep(1)