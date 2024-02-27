import mongoengine as db
import datetime

class Video(db.Document):
    store_id = db.ObjectIdField()
    camera_id = db.ObjectIdField() 
    source_url = db.URLField(required=True)
    upload_timestamp = db.DateTimeField(required=True)
    start_time = db.DateTimeField(required=True)
    end_time = db.DateTimeField(required=True)
    createdAt = db.DateTimeField(default=datetime.datetime.now)
    updatedAt = db.DateTimeField(default=datetime.datetime.now)
    
