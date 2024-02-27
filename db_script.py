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
from cameras_schema import Cameras #TODO 
import re
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
import random
import datetime
from faker import Faker
fake = Faker()
import secrets



def connect_to_mongo():
    mongo_url = os.environ.get('MONGO_APP_URL')
    db.connect(host=mongo_url)
    print(mongo_url)


df2 = pd.read_csv('16_1-2_processed_updated-2.csv')

df2 = pd.read_csv('16_1-2_processed_updated-2.csv')
df2.drop("elapsed_time", axis=1, inplace=True)
timestamp_str = pd.Timestamp('2024-02-25 22:15:01.359274').strftime('%Y-%m-%d %H:%M:%S.%f')
print(timestamp_str)
print(type(timestamp_str))
# df2['time_stamp'] = timestamp_str


all_ids = []

for index, row in df2.iterrows():
    zone_value = row["1_zone"]
    if not pd.isna(zone_value):
        zone_dict = ast.literal_eval(zone_value)
        
        current_ids = zone_dict.get("current_ids", [])
        
        all_ids.extend(current_ids)

zone1_ids = list(set(all_ids))
for index, row in df2.iterrows():
    zone_value = row["2_zone"]
    if not pd.isna(zone_value):
        zone_dict = ast.literal_eval(zone_value)
        
        current_ids = zone_dict.get("current_ids", [])
        
        all_ids.extend(current_ids)

zone2_ids = list(set(all_ids))
for index, row in df2.iterrows():
    zone_value = row["3_ground"]
    if not pd.isna(zone_value):
        zone_dict = ast.literal_eval(zone_value)
        
        current_ids = zone_dict.get("current_ids", [])
        
        all_ids.extend(current_ids)

ground_ids = list(set(all_ids))
for index, row in df2.iterrows():
    zone_value = row["4_department"]
    if not pd.isna(zone_value):
        zone_dict = ast.literal_eval(zone_value)
        
        current_ids = zone_dict.get("current_ids", [])
        
        all_ids.extend(current_ids)

department_ids = list(set(all_ids))

zone_id_mapping = {
    "ground": ground_ids,
    "department": department_ids,
    "zone1": zone1_ids,
    "zone2": zone2_ids
}

def assign_zone_id(pose_track_id, zone_id_mapping):
    zone_id_assigned = None
    for zone_id, zone_ids_list in zone_id_mapping.items():
        if any(track_id in zone_ids_list for track_id in pose_track_id):
            zone_id_assigned = zone_id
            print("zone id assigned",zone_id_assigned)
            break
    return zone_id_assigned


def fill_tracking_ids(num_records):
    for _ in range(num_records):
        pose_track_ids = random.choice(list(set(all_ids)))  
        person_class = random.choice(['Costumer', 'Employee'])
        gender = random.choice(['Male', 'Female'])
        age = random.randint(18, 70),
        upper_body_clothes = random.choice(['Red', 'Blue', 'Green', 'Yellow'])
        lower_body_clothes = random.choice(['Black', 'White', 'Gray'])
        blob_refs = []  
        store_id = None  
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
    tracking_id_dict = {}
    

    for index,row in df2[2:-1].iterrows():
        pose = row['pose_bbox']
        pose_bbox = [list(map(int, re.findall(r'\d+', item))) for item in pose.split(')\n') if item]
        frame_no =int( row['frame_number'])
        labels = list(row['label'])
        labels = [element for element in labels if element.isdigit()]
        fps = row['fps']
        # time_stamp = row['time_stamp']
        image_path = row['image_path']
        pose_track_id = list(row['pose_track_ids'])
        pose_track_id = [element for element in pose_track_id if element.isdigit()]
        zone_id = [assign_zone_id(pose_track_id, zone_id_mapping) for element in pose_track_id if element.isdigit()]

        
    
        for index,value in enumerate(pose_track_id):

            blob = Blob(
                frame_number=frame_no,
                # time_stamp=time_stamp,
                pose_bbox=pose_bbox[index],
                fps=fps,
                image_path = image_path,
                zone_id = zone_id
            ).save()
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
            "blob": ObjectId(),  # Assuming you have blob IDs in your database
            "zones": {"zone1": "zone1", "zone2": "zone2"},
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
            "blob": ObjectId(),  # Assuming you have blob IDs in your database
            "zones": {"zone3": "ground", "zone4": "department"},
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
        camera = Cameras(
            store_id=ObjectId(),
            camera_id=camera_data["camera_id"],
            blob=camera_data["blob"],
            zones=camera_data["zones"],
            analysis_timestamp=camera_data["analysis_timestamp"],
            neo_object=camera_data["neo_object"],
            created_at=camera_data["created_at"],
            update_at=camera_data.get("update_at", camera_data["created_at"])
        )
        camera.save()
        print("camara data saved")

    print("Dummy data populated successfully.")




def generate_dummy_zones():
    store_ids = ["store1", "store2", "store3"]
    colour_hex_codes = ["#FF5733", "#33FF57", "#5733FF", "#FFFF33", "#33FFFF", "#FF33FF"]
    dummy_zones = [{
            'id': "zone0001",
            'name': "zone1",
            'store': ObjectId(),
            'colourHex': secrets.choice(colour_hex_codes)
        },
        {
            'id': "zone0002",
            'name': "zone2",
            'store': ObjectId(),
            'colourHex': secrets.choice(colour_hex_codes)
        },
        {
            'id': "zone0003",
            'name': "ground",
            'store': ObjectId(),
            'colourHex': secrets.choice(colour_hex_codes)
        },
        {
            'id': "zone0004",
            'name': "department",
            'store': ObjectId(),
            'colourHex': secrets.choice(colour_hex_codes)
        }]
    
    
    return dummy_zones

def save_dummy_zones(dummy_zones):
    for zone_data in dummy_zones:
        zone = Zone(**zone_data)
        zone.save()
        print("zone data saved")

def populate_videos(num_records):
    store_ids = ["store1", "store2", "store3"]
    for _ in range(num_records):
        # Generate dummy values for each field
        store_id = ObjectId()  # Replace with actual store IDs
        camera_id = ObjectId() # Replace with actual camera IDs
        source_url = fake.url()
        upload_timestamp = datetime.datetime.now()
        start_time = datetime.datetime.now()
        end_time = datetime.datetime.now()
        
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
        print("video daata saved")



def main():
    try:
        connect_to_mongo()
        print("Database connection successful..")
        
        n = 10
        dummy_data()
        dummy_zones = generate_dummy_zones()
        save_dummy_zones(dummy_zones)
        # fill_tracking_ids(n)
        populate_camera_data()
        
        populate_videos(n)

        print(f"{n} dummy records inserted into the Tracking_id collection.")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()