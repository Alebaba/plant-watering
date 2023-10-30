import math
import serial

class WaterBucket:
    def __init__(self, initial_water_amount, bucket_area, valve_area):
        self.water_amount = initial_water_amount # Water amount in liters
        self.bucket_area = bucket_area # Area in m^2
        self.valve_area = valve_area # Area in m^2

        try:
            self.serial_connection = serial.Serial('dev/ttyACM0', 9600, timeout=1)
        except serial.SerialException as e:
            print(f"Error: {e}")

    def __del__(self):
        if self.serial_connection:
            self.serial_connection.close()

    def calculate_drain_time(self, liters) -> int:
        g = 9.81
        V_initial = self.water_amount * 1e-3
        H_initial = V_initial / self.bucket_area
        V_after_drained = V_initial - liters * 1e-3

        # Eulers method to calculate approximate time
        t = 0
        dt = 1e-3
        V = V_initial
        H = H_initial
        while V > V_after_drained:
            # Calculate flow rate using Toricelli's law
            flow_rate = self.valve_area * math.sqrt(2 * g * H) 
            dV = flow_rate * dt
            V = max(V - dV, 0)
            H = V / self.bucket_area
            t += dt
        
        return int(t * 1000)

    def open_valve(self, liters) -> bool:
        if liters > self.water_amount:
            print("Drained amount is higher than water amount in bucket")
            return False
        
        valve_active_time = self.calculate_drain_time(liters)
        
        print(f"Valve on for {valve_active_time} milliseconds")
        command = f'v{valve_active_time}'
        try:
            self.serial_connection.write(command.encode())
        except serial.SerialException as e:
            print(f"Error writing to serial port: {e}")
            return False
        
        self.water_amount = max(self.water_amount - liters, 0)

        return True