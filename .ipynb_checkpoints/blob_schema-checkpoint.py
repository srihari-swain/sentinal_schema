import mongoengine as db

class Blob(db.Document):
    pose_track_ids = db.StringField(required = True)
    frame_number = db.IntField(required=True)
    elapsed_time = db.StringField(required=True)
    time_stamp = db.FloatField(required=True)
    camara_id = db.StringField()
    store_id = db.StringField()
    # pose_bbox = db.ListField(db.ListField(db.IntField()))
    pose_bbox = db.ListField(db.IntField())
    fps = db.FloatField(required=True)
    image_path = db.StringField(required=True)
    trackingid_ref = db.ReferenceField('Tracking_id')

    # @classmethod
    # def get_all(cls):
    #     return Blob.objects
