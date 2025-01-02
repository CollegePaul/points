from smbus2 import SMBus
import time

# I2C address of the Arduino
I2C_ADDRESS = 0x08

def write_to_arduino(data):
    with SMBus(1) as bus:  # Use I2C bus 1
        try:
            bus.write_byte(I2C_ADDRESS, data)
            print(f"Data sent to Arduino: {data}")
        except Exception as e:
            print(f"Error writing to Arduino: {e}")

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