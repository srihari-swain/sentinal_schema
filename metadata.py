import mongoengine as db

class Tracking_id(db.Document):
    pose_track_ids = db.StringField(required = True)
    person_class = db.StringField(required = True)
    # person_class =  db.ListField(db.StringField(), required=True)
    # pose_track_ids = db.ListField(db.StringField())
    age = db.IntField()
    gender = db.StringField()
    upper_body_clothes = db.StringField()
    lower_body_clothes = db.StringField()
    blob_refs = db.ListField(db.ReferenceField('Blob'))

    @classmethod
    def get_all(cls):
        return Tracking_id.objects
