import mongoengine as db


class Blob(db.Document):
    frame_number = db.IntField(required=True,primary_key=True)
    # time_stamp = db.StringField(required=True)
    time_stamp = db.StringField()
    camera_id = db.ReferenceField("Camera")
    pose_bbox = db.ListField(db.IntField())
    fps = db.FloatField(required=True)
    image_path = db.StringField(required=True)
    trackingid_ref = db.ReferenceField('Tracking_id')
    zone_id = db.ReferenceField('Zone')
