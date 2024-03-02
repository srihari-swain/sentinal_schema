import mongoengine as db

class Blob(db.Document):
    track_ids = db.StringField(required = True)
    person_class = db.StringField(required = True)
    age = db.IntField()
    gender = db.StringField()
    upper_body_clothes = db.StringField()
    lower_body_clothes = db.StringField()
    store_id = db.ReferenceField("Store")
    group = db.ListField(db.StringField())
    camera = db.ListField(db.ReferenceField("Camera"))
    starting_time = db.StringField()
    ending_time = db.StringField()
    metadata_refs = db.ListField(db.ReferenceField('Metadata'))
    
    
    ## TODO: add stating time and ending time of the id in the store
# process feather file and push the metadata 
   # at the end , push the blob _collection
# trackid update 
    