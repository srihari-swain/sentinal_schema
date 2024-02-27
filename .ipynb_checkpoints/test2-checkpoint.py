import ast
import mongoengine as db
import pandas as pd
from blob_schema import Blob
from metadata import Tracking_id
from bson import ObjectId
import re

# Read the instance file

def connect_to_mongo():
    # Update the MongoDB connection URI with your actual MongoDB server details
    mongo_url = 'mongodb+srv://srihari:KtOlAeBIx68LyQYb@disha.btaddfx.mongodb.net/reliance-digital-test?authMechanism=DEFAULT&authSource=admin&readPreference=nearest&retryWrites=true'
    
    db.connect(host=mongo_url)


def dummy_data():
    try:
        connect_to_mongo()
        print("Database connection successful..")

        

        data = pd.read_csv('output_file.csv')
        data = data.head(10)
        tracking_id_dict = {}
        for index,row in data[2:-1].iterrows():
            pose = row['pose_bbox']
            pose_bbox = [list(map(int, re.findall(r'\d+', item))) for item in pose.split(')\n') if item]
                # print(pose)
        # pose_bbox = (row['pose_bbox'])
        
            frame_no =int( row['frame_number'])
        # print(type(frame_no) )
        # print(frame_no)   
            elaps_time = row['elapsed_time']
        # print(elaps_time)
        # print(type(elaps_time))
            labels = list(row['label'])
            labels = [element for element in labels if element.isdigit()]
        # print("label_type",type(labels))
        # print(labels)
            fps = row['fps']
            time_stamp = float(frame_no/fps)
            # print(time_stamp)
        # print(type(fps))
            image_path = row['image_path']
        # print(image_path)
        # print(type(image_path))
        # pose_track_ids =row['pose_track_ids'].replace(" ", ",")
        # pose_track_ids = [int(x) for x in pose_track_ids.split()]
            pose_track_id = list(row['pose_track_ids'])
            pose_track_id = [element for element in pose_track_id if element.isdigit()]
            print(pose_track_id)

            # print(pose_track_id)
            # print(labels)
        

           
                
                # print(pose_track_id[i])
                # print(labels[i])
            # print(pose_track_id)

        # # Iterate over each row in the DataFrame
        # for index, row in data.iterrows():
        #     try:
        #         # Convert string representation of lists to actual lists
        #         pose_bbox = ast.literal_eval(row['pose_bbox'])

        #         # Handle NaN values for pose_track_ids
        #         pose_track_ids_str = row['pose_track_ids']
        #         pose_track_ids_str = preprocess_pose_track_ids(pose_track_ids_str)
        #         pose_track_ids = ast.literal_eval(pose_track_ids_str) if not pd.isna(pose_track_ids_str) else []

        #         # Handle NaN values for label
        #         label_str = row['label']
        #         label = ast.literal_eval(label_str) if not pd.isna(label_str) else []

        #         # Create metadata document for the current row
        #         metadata_doc = Metadata(
        #             pose_track_ids=pose_track_ids
        #         )
        #         metadata_doc.save()
        #         print("metadata saved")

                # Create a blob document for each pose track in the current frame
            #     for i, track_id in enumerate(pose_track_ids):
            #         blob_doc = Blob(
            #             frame_number=row['frame_number'],
            #             elapsed_time=row['elapsed_time'],
            #             label=label[i] if i < len(label) else None,
            #             pose_bbox=pose_bbox[i],
            #             fps=row['fps'],
            #             image_path=row['image_path'],
            #             metadata_ref=metadata_doc,
            #             pose_track_id=track_id
            #         )
            #         blob_doc.save()
            #         print("blob data saved")
            # except Exception as e_row:
            #     print(f"An error occurred for row {index + 1}: {e_row}")
            #     print(f"Row content: {row}")
            # matching_blob_ids = []
        
            for index,value in enumerate(pose_track_id):

                blob = Blob(
                    pose_track_ids = value,
                    frame_number=frame_no,
                    elapsed_time=elaps_time,
                    time_stamp = time_stamp,
                    # label=labels,#TODO (transer this label to track_id cl)
                    pose_bbox=pose_bbox[index],
                    fps=fps,
                    image_path = image_path,
                    # trackingid_ref = tracking_id
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

                # Update the blob_refs of the tracking_id
                tracking_id_dict[value].blob_refs.append(blob.id)
                tracking_id_dict[value].save()
                
                # blob = Blob(
                #     pose_track_ids = value,
                #     frame_number=frame_no,
                #     elapsed_time=elaps_time,
                #     time_stamp = time_stamp,
                #     # label=labels,#TODO (transer this label to track_id cl)
                #     pose_bbox=pose_bbox[index],
                #     fps=fps,
                #     image_path = image_path,
                #     # trackingid_ref = tracking_id
                # ).save()
                # print("blob data saved")

#                 matching_blobs = Blob.objects(pose_track_ids=value)

#                 print(matching_blobs)


#                 tracking_id.blob_refs.extend(matching_blobs)
#                 tracking_id.save()

#                 blob.trackingid_ref = tracking_id
#                 blob.save()
                

                   

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    dummy_data()
