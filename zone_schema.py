import mongoengine as db
import datetime
class Zone(db.Document):
    zone_id = db.StringField()
    name = db.StringField()
    
    store = db.ReferenceField('Store')
    
    createdAt = db.DateTimeField(default=datetime.datetime.now)
    updatedAt = db.DateTimeField(default=datetime.datetime.utcnow)
    
    colourHex = db.StringField()
