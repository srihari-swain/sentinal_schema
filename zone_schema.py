import mongoengine as db
import datetime
class Zone(db.Document):
    id = db.StringField(primary_key=True)
    name = db.StringField(required=True)
    
    store = db.ObjectIdField()
    
    createdAt = db.DateTimeField(default=datetime.datetime.now)
    updatedAt = db.DateTimeField(default=datetime.datetime.utcnow)
    
    colourHex = db.StringField(required=True)
