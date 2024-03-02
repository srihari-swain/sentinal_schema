import mongoengine as db

class Cameras(db.Document):
    # store_id = db.ReferenceField("Stores") 
    store_id = db.ReferenceField("Store")
    camera_id = db.StringField(required=True)  
    blob = db.ObjectIdField()
    zones = db.ListField()
    analysis_timestamp = db.DateTimeField()
    created_at = db.DateTimeField()
    update_at = db.DateTimeField(default=created_at)