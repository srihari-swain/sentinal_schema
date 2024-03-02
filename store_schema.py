'''
id
"0001"
name
"DIGITAL-Seawood-NaviMumbai"
organization
"reliance-retail"
format
"SMART"
categories
"DIGITAL"
state
"MH"
city
"NaviMumbai"
dist
"Raigarh"

location
Object

layout
Object
createdAt
2024-02-09T08:29:30.125+00:00
updatedAt
2024-02-09T08:29:30.125+00:00
'''

import mongoengine as db
import datetime


class Store(db.Document):
    store_id = db.StringField()
    name = db.StringField()
    organization = db.StringField()
    format = db.StringField()
    category = db.StringField()
    state = db.StringField()
    city = db.StringField()
    district = db.StringField()
    location = db.DictField()
    layout = db.DictField()
    createdAt = db.DateTimeField(default=datetime.datetime.now)
    updatedAt = db.DateTimeField(default=datetime.datetime.utcnow)
