import os
import ast
import mongoengine as db
import pandas as pd
from blob_schema import Blob
from tracking_id_schema import Tracking_id
from bson import ObjectId
#from store_schema import Store
from zone_schema import Zone
from video_schema import Video
from cameras_schema import Camera #TODO 
import re
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
import random
import datetime
from faker import Faker
fake = Faker()
# Read the instance file

def connect_to_mongo():
    mongo_url = os.environ.get('MONGO_APP_URL')
    db.connect(host=mongo_url)
    print(mongo_url)


def generate_dummy_data(num_records):
    for _ in range(num_records):
        # Generate dummy values for each field
        pose_track_ids = ''.join(random.choices('0123456789', k=10))  # Generate a random 10-digit string
        person_class = random.choice(['Class A', 'Class B', 'Class C'])
        age = random.randint(18, 70)  # Random age between 18 and 70
        gender = random.choice(['Male', 'Female'])
        upper_body_clothes = random.choice(['Red', 'Blue', 'Green', 'Yellow'])
        lower_body_clothes = random.choice(['Black', 'White', 'Gray'])
        blob_refs = []  # Initialize as an empty list
        store_id = None  # Initialize as None
        group = random.choices(['Group 1', 'Group 2', 'Group 3'], k=random.randint(1, 3))  # Random list of groups

        # Create a Tracking_id document and save it to the collection
        tracking_id = Tracking_id(
            pose_track_ids=pose_track_ids,
            person_class=person_class,
            age=age,
            gender=gender,
            upper_body_clothes=upper_body_clothes,
            lower_body_clothes=lower_body_clothes,
            blob_refs=blob_refs,
            store_id=store_id,
            group=group
        )
        tracking_id.save()


def dummy_data():
    data = pd.read_feather('13_3-1processed.feather')
    data = data.head(10)
    tracking_id_dict = {}
    '''
    frame_number = db.IntField(required=True)
    time_stamp = db.FloatField(required=True)
    camera_id = db.StringField(required=True)
    pose_bbox = db.ListField(db.IntField())
    fps = db.FloatField(required=True)
    image_path = db.StringField(required=True)
    trackingid_ref = db.ReferenceField('Tracking_id')
    zone_id = db.ReferenceField('Zone')

    '''

    for index,row in data[2:-1].iterrows():
        pose = row['pose_bbox']
        pose_bbox = [list(map(int, re.findall(r'\d+', item))) for item in pose.split(')\n') if item]
        frame_no =int( row['frame_number'])
        elaps_time = row['elapsed_time']
        labels = list(row['label'])
        labels = [element for element in labels if element.isdigit()]
        fps = row['fps']
        time_stamp = row['time_stamp']
        image_path = row['image_path']
        pose_track_id = list(row['pose_track_ids'])
        pose_track_id = [element for element in pose_track_id if element.isdigit()]
        print(pose_track_id)

        
    
        for index,value in enumerate(pose_track_id):

            blob = Blob(
                pose_track_ids = value,
                frame_number=frame_no,
                elapsed_time=elaps_time,
                time_stamp = time_stamp,
                pose_bbox=pose_bbox[index],
                fps=fps,
                image_path = image_path,
            ).save()
            track_id = Tracking_id(

            )
            print("blob data saved")
            if value not in tracking_id_dict:
                tracking_id = Tracking_id(
                    pose_track_ids=value,
                    person_class=labels[index],
                    age=45,
                    gender='male',
                    upper_body_clothes='green',
                    lower_body_clothes='white',
                ).save()
                tracking_id_dict[value] = tracking_id
                print("trackingid data saved")
            blob.trackingid_ref = tracking_id_dict[value]
            blob.save()
            tracking_id_dict[value].blob_refs.append(blob.id)
            tracking_id_dict[value].save()
                

def populate_camera_data():
    dummy_cameras = [
        {
            "store_id": "store_id_1",
            "camera_id": "camera_001",
            "blob": "blob_id_1",  # Assuming you have blob IDs in your database
            "zones": {"zone1": "description1", "zone2": "description2"},
            "analysis_timestamp": datetime.datetime.utcnow(),
            "neo_object": [
                {"id": 1, "coordinates": {"x": 19.09, "y": 25.55}},
                {"id": 2, "coordinates": {"x": 21.35, "y": 28.75}},
            ],
            "created_at": datetime.datetime.utcnow(),
            "update_at": datetime.datetime.utcnow()
        },
        {
            "store_id": "store_id_2",
            "camera_id": "camera_002",
            "blob": "blob_id_2",  # Assuming you have blob IDs in your database
            "zones": {"zone3": "description3", "zone4": "description4"},
            "analysis_timestamp": datetime.datetime.utcnow(),
            "neo_object": [
                {"id": 3, "coordinates": {"x": 15.20, "y": 30.10}},
                {"id": 4, "coordinates": {"x": 18.75, "y": 22.90}},
            ],
            "created_at": datetime.datetime.utcnow(),
            "update_at": datetime.datetime.utcnow()
        },
    ]

    for camera_data in dummy_cameras:
        camera = Camera(
            store_id=camera_data["store_id"],
            camera_id=camera_data["camera_id"],
            blob=camera_data["blob"],
            zones=camera_data["zones"],
            analysis_timestamp=camera_data["analysis_timestamp"],
            neo_object=camera_data["neo_object"],
            created_at=camera_data["created_at"],
            update_at=camera_data.get("update_at", camera_data["created_at"])
        )
        camera.save()

    print("Dummy data populated successfully.")




def generate_dummy_zones(num_zones):
    dummy_zones = []
    for i in range(num_zones):
        zone_id = f"zone_{i+1}"
        name = f"Zone {i+1}"
        store_id = "your_store_id" 
        colour_hex = f"#{random.randint(0, 0xFFFFFF):06x}" 
        
        zone_data = {
            'id': zone_id,
            'name': name,
            'store': store_id,
            'colourHex': colour_hex
        }
        dummy_zones.append(zone_data)

    return dummy_zones

def save_dummy_zones(dummy_zones):
    for zone_data in dummy_zones:
        zone = Zone(**zone_data)
        zone.save()

def populate_videos(num_records):
    for _ in range(num_records):
        # Generate dummy values for each field
        store_id = 'some_store_id'  # Replace with actual store IDs
        camera_id = 'some_camera_id'  # Replace with actual camera IDs
        source_url = fake.url()
        upload_timestamp = fake.date_time_this_year()
        start_time = fake.date_time_this_year()
        end_time = fake.date_time_this_year()
        
        # Create a new Video document with the generated data
        video = Video(
            store_id=store_id,
            camera_id=camera_id,
            source_url=source_url,
            upload_timestamp=upload_timestamp,
            start_time=start_time,
            end_time=end_time
        )
        video.save()



def main():
    try:
        connect_to_mongo()
        print("Database connection successful..")
        
        n = 10

        generate_dummy_data(n)
        populate_camera_data()
        dummy_zones = generate_dummy_zones(n)
        save_dummy_zones(dummy_zones)
        populate_videos(n)

        print(f"{n} dummy records inserted into the Tracking_id collection.")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()