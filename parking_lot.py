import random
import json
# import boto3

# Parking Lot method with map_to_json and decrease_capacity methods
class ParkingLot:
    def __init__(self, lot_size, spot_size=96):
        self.lot_size = lot_size
        self.spot_size = spot_size
        self.total_capacity = lot_size // spot_size
        self.parking_lot = [None] * self.total_capacity
        self.parking_map = {}

    def map_to_json(self):
        mapping = {str(i + 1): str(car.license_plate) if car else None for i, car in enumerate(self.parking_lot)}
        return json.dumps(mapping, indent=1)
        
    # this method decreases the total_capacity by 1 - when a car enters parking lot total_capacity decreases by 1
    def decrease_capacity(self):
        self.total_capacity -= 1

# Car class with magic and park methods
class Car:
    def __init__(self, license_plate):
        self.license_plate = license_plate

    def magic(self):
        return str(self.license_plate)
    
    # this method parks a car and decreases car capacity from total_capacity by 1
    def park(self, parking_lot):
        for spot in range(len(parking_lot.parking_lot)):
            if parking_lot.parking_lot[spot] is None:
                parking_lot.parking_lot[spot] = self
                parking_lot.decrease_capacity()
                return f"Car with license plate {self.license_plate} parked successfully in spot {spot + 1}"
        return f"Car with license plate {self.license_plate} could not park in any spot"

# this method uploads the file to S3, given bucket name and object_name
def upload_to_s3(file_path, bucket_name, object_name):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, object_name)

def main():
    parking_lot_size = 200
    spot_size = 96  
    parking_lot = ParkingLot(parking_lot_size, spot_size)
    
    # reading number of cars and car numbers as input
    num_cars = int(input("Enter the number of cars: "))
    # input car numbers 
    cars = [Car(input(f"Enter license plate for car {i + 1}: ")) for i in range(num_cars)]

    for car in cars:
        status = car.park(parking_lot)
        print(status)

    json_data = parking_lot.map_to_json()
    with open("parking_map.json", "w") as json_file:
        json_file.write(json_data)

    s3_bucket_name = "your-s3-bucket-name"
    s3_object_name = "parking_map.json"
    upload_to_s3("parking_map.json", s3_bucket_name, s3_object_name)

if __name__ == "__main__":
    main()
