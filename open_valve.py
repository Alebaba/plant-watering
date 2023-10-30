import sys
import serial
import time

arduino_port = '/dev/ttyACM0'
baud_rate = 9600
timeout = 1

arduino = serial.Serial(arduino_port, baud_rate, timeout=timeout)

time.sleep(2)

def activate_valve(duration):
    command = 'v' + str(duration)
    print("Valve on for " + str(duration) + " milliseconds")
    arduino.write(command.encode())

if len(sys.argv) > 1:
    valve_active_time = int(sys.argv[1]) * 1000
    activate_valve(valve_active_time)

arduino.close()
