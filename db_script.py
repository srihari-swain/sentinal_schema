import os
import json
import mongoengine as db
import pandas as pd
from blob_schema import Blob
from metadata_schema import Metadata
from store_schema import Store
from zone_schema import Zone
from video_schema import Video
import re
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
import random
import datetime
from faker import Faker
fake = Faker()
import secrets

"""
This script will do following things:
1. aggregate the store metadata based on selected time period and pull the data
2. apply the create blob document method on the extrected data
    i. This function will select the best confidance label, age, gneder, upper body and lower body
    ii. create multiple blob document for all the track ids with filted info
    iii. Push the data blob collection

"""

    
def connect_to_mongo():
    mongo_url = "mongodb+srv://neo-rajkishore:NeoRajkishore12345@disha.btaddfx.mongodb.net/reliance-digital-test-2?retryWrites=true&w=majority"
    db.connect(host=mongo_url)
    
def merge_dicts(x, y):
    merged_dict = x.copy()
    merged_dict.update(y)
    return merged_dict


    
def fill_data():
    
    segmentation_json = "/home/pranjal/project/sentinel-core/results/cctv-seg-15_min_13_16/instances_default.json"
    df = pd.read_feather("/home/aryan/project/sentinel-core/results/processed_zone.feather")

    with open(segmentation_json, "r") as f:
        seg_json = json.load(f)
        
    annotations_df = pd.DataFrame(seg_json['annotations'])
    categories_df = pd.DataFrame(seg_json["categories"])

    for rows,value in categories_df.iterrows():
        annotations_df.loc[annotations_df['category_id']==value['id'],"zones"] = value["name"]
    
    store_test = Store(
        store_id="001",
        name = "DIGITAL-Seawood-NaviMumbai",
        organization = "reliance-retail",
        format = "SMART",
        category = "DIGITAL",
        state = "MH",
        city = "NaviMumbai",
        district = "Raigarh",
        location={"longitude": 19.020174, "latitude": 73.017255},
        layout = {"zones":["Z-0000","Z-0001","Z-0002","Z-0003"]},
        createdAt = datetime.datetime.now(),
        updatedAt = datetime.datetime.now()
        )
    try:
        store_test.save()  
        print("store data saved")
    except Exception as e:
        print(f"Store Data not saved: {e}")
      
    
    
    storeall = Store.objects.first()
    colour_hex_codes = ["#FF5733", "#33FF57", "#5733FF", "#FFFF33"]
    dummy_zones = [{
            'zone_id': "Z-0000",
            'name': "zone_1",
            'store': storeall,
            'colourHex': secrets.choice(colour_hex_codes)
        },
        {
            'zone_id': "Z-0001",
            'name': "zone_2",
            'store': storeall,
            'colourHex': secrets.choice(colour_hex_codes)
        },
        {
            'zone_id': "Z-0002",
            'name': "mobile_1",
            'store': storeall,
            'colourHex': secrets.choice(colour_hex_codes)
        },
        {
            'zone_id': "Z-0003",
            'name': "mobile_2",
            'store': storeall,
            'colourHex': secrets.choice(colour_hex_codes)
        }]
    for zone_data in dummy_zones:
        zone = Zone(**zone_data) # ** is for unpacking the dictionary
        try:
            zone.save() 
            print("zone data saved")
        except Exception as e:
            print(f"zone Data not saved: {e}")
    
    
    
    metadata_dict = []
    df['combined_zones'] = df.apply(lambda row: merge_dicts(row['customer_zone'],row['employees_zone']),axis=1)
    
    for key, row in df.iterrows():
        if row is not None:
            for index,x in enumerate(row["pose_track_ids"]):
                zone_id_list = []
                zone_list = []
                zones = row["combined_zones"]
                try:
                    for key,val in zones.items():
                        if val is not None:
                            for i in val:
                                if x==i:
                                    zone_list.append(key)
                    for val in zone_list:
                        zone = Zone.objects.filter(name=val).first()
                        if zone:
                            zone_id_list.append(zone.zone_id)
                            
                    metadata = {
                        "frame_number": int(row["frame_number"]),
                        "pose_track_id": int(x),
                        "person_class": int(row["labels"][index]),
                        "time_stamp": str(row["time_stamp"]),
                        "pose_bbox": row["pose_bboxes"][index],
                        "fps": int(row["fps"]),
                        "age": int(random.randint(18,70)),
                        "gender": random.choice(["Male","Female"]),
                        "upper_body_clothes": random.choice(["Black","Green"]),
                        "lower_body_clothes": random.choice(["while","Black"]),
                        "zone_id":   zone_id_list,
                        "pose_segmentation_mask": row["segmentation_masks"][index].tolist(),
                        "confidence": float(row["confidences"][index])
                    }
                    metadata_dict.append(metadata)
                except Exception as e:
                    print(f"Error processing row {key}:{e}")

    for meta in metadata_dict:
        metadata_test = Metadata(**meta)
        try:
            metadata_test.save() 
        except Exception as e:
            print(f"Meta Data not saved: {e}")
    print("Meta data saved")
    
    
    pose_track_id_list = []
    labels_list = []
    confidence_list = []
    for index,row in df.iterrows():
        if row is not None:
            for key,track_id in enumerate(row["pose_track_ids"]):
                pose_track_id_list.append(track_id)
                labels_list.append(row["labels"][key])
                confidence_list.append(row["confidences"][key])
    test_df = pd.DataFrame({'track_ids':pose_track_id_list,'labels':labels_list,'confidences':confidence_list})
    idx = test_df.groupby("track_ids")["confidences"].idxmax()
    result_df = test_df.loc[idx]
    
    
    
    
    
def main():
    try:
        connect_to_mongo()
        print("Database connection successful..")
        
        fill_data()
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
                    
        