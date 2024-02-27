import mongoengine as db

class Tracking_id(db.Document):
    pose_track_ids = db.StringField(required = True)
    person_class = db.StringField(required = True)
    age = db.IntField()
    gender = db.StringField()
    upper_body_clothes = db.StringField()
    lower_body_clothes = db.StringField()
    blob_refs = db.ListField(db.ReferenceField('Blob'))
    store_id = db.ReferenceField("Store")
    group = db.ListField(db.StringField())
