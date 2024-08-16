import random
import time
from datetime import datetime
import threading

from processdata import VehicleDataProcessor

processor = VehicleDataProcessor()
# Global list to store active vehicles
active_vehicles = []
# Create a lock for thread-safe access
vehicles_lock = threading.Lock()
# Vehicle class definition (assuming it's defined elsewhere in your code)
class Vehicle:
    def __init__(self, plate, initial_position, speed):
        self.plate = plate
        self.position = initial_position
        self.active = True

    def move(self):
        if self.active:
            self.position = round(random.uniform(self.position, 110), 2)
            if self.position > 100:  # Vehicle exits the sensor range
                self.active = False

# Function to initialize new vehicles
def initialize_vehicles(num_vehicles):
    vehicles = []
    for _ in range(num_vehicles):
        plate = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        initial_position = round(random.uniform(0, 50), 2)
        vehicles.append(Vehicle(plate, initial_position))
    return vehicles

# Function to generate fake data from sensor
def generate_fake_data(sensor_id, time_interval=1):
    global active_vehicles
    timestamp = datetime.utcnow().isoformat()
    
    # Update positions of existing active vehicles
    with vehicles_lock:
        for vehicle in active_vehicles[:]:  # Iterate over a copy to avoid modification issues
            vehicle.move()
            if not vehicle.active:
                active_vehicles.remove(vehicle)

    # Collect data for active vehicles
    active_vehicle_data = []
    for vehicle in active_vehicles:
        active_vehicle_data.append({
            "plate": vehicle.plate,
            "position": round(vehicle.position, 2)
        })

    return {
        "sensor_id": sensor_id,
        "timestamp": timestamp,
        "vehicles": active_vehicle_data
    }

# Thread function to continuously initialize new vehicles
def vehicle_initializer_thread():
    global active_vehicles
    while True:
        num_new_vehicles = random.randint(1, 5)
        new_vehicles = initialize_vehicles(num_new_vehicles)
        with vehicles_lock:
            active_vehicles.extend(new_vehicles) # Add new vehicles to the active list
        time.sleep(random.uniform(1, 3))

# Thread function to simulate data generation
def data_generator_thread():
    while True:
        data = generate_fake_data("sensor_1")
        print(data)
        processor.process_data(data)
        time.sleep(1)  # Simulate time passing

# Start the threads
initializer_thread = threading.Thread(target=vehicle_initializer_thread)
generator_thread = threading.Thread(target=data_generator_thread)

initializer_thread.start()
generator_thread.start()

initializer_thread.join()
generator_thread.join()
