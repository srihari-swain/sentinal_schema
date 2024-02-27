import mongoengine as db

class Cameras(db.Document):
    # store_id = db.ReferenceField("Stores") 
    store_id = db.ObjectIdField()

    camera_id = db.StringField(required=True)  
    blob = db.ObjectIdField()
    zones = db.DictField()
    analysis_timestamp = db.DateTimeField()
    neo_object = db.ListField(db.DictField())
    created_at = db.DateTimeField()
    update_at = db.DateTimeField(default=created_at)