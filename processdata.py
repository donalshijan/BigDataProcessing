from datetime import datetime

class VehicleDataProcessor:
    def __init__(self):
        self.vehicle_data = {}

    def process_data(self, data):
        timestamp = datetime.fromisoformat(data["timestamp"])
        total_speed = 0
        speed_count = 0
        
        for vehicle in data["vehicles"]:
            plate = vehicle["plate"]
            position = vehicle["position"]
            if plate in self.vehicle_data:
                prev_position, prev_timestamp = self.vehicle_data[plate]
                speed = (position - prev_position) / ((timestamp - prev_timestamp).total_seconds() / 3600)
                total_speed += speed
                speed_count += 1
            self.vehicle_data[plate] = (position, timestamp)

        if speed_count > 0:
            average_speed = total_speed / speed_count
        else:
            average_speed = 0
        
        vehicle_count = len(self.vehicle_data)
        congestion_level = vehicle_count * average_speed
        
        print(f"Congestion level at intersection: {congestion_level:.2f}")


