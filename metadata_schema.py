import mongoengine as db
"""
module_dict= {
    pose_track_id : db.IntField()
    person_class : db.IntField()
    pose_bbox = db.ListField(db.FloatField())
    pose_segmentation_mask = db.ListField(db.FloatField())
    confidence = db.FloatField()
    age = db.IntField()
    gender = db.StringField()
    zone_id = db.ListField(db.StringField())
}
    
    
feature_dict= {
    upper_body_clothes = db.StringField()
    lower_body_clothes = db.StringField()
}

"""

    

class Metadata(db.Document):
    name = db.StringField()
    frame_number = db.IntField()
    camera = db.ObjectIdField()
    time_stamp = db.StringField()
    fps = db.IntField()
    module = db.DictField()
    feature = db.DictField()
    
    
    
    
    
    

# TODO: add pose segmentation mask, confidence, age, gender, upperbody clothes, lowerbody clothes