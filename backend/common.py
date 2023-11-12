import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class Event:
    def __init__(
        self,
        event_id,
        name,
        start_datetime,
        end_datetime,
        building_name,
        full_location,
        description,
    ):
        self.event_id = event_id
        self.name = name
        self.full_location = full_location
        if full_location is not None:
            if "," in full_location:
                x = full_location.index(",")
                self.building_name = full_location[0:x]
            else:
                self.building_name = full_location
        else:
            self.building_name = full_location
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.description = description


db_uri = os.getenv("ATLAS_URI")
db_client = MongoClient(db_uri, server_api=ServerApi("1"))
db_cluster = db_client.Madhacks2023Cluster0
events_db = db_cluster.events
