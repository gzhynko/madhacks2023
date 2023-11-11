import os
import base64
import functions_framework

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class Event:
    def __init__(
        self, event_id: int, name: str, datetime: str, location: str, description: str
    ):
        self.event_id = event_id
        self.name = name
        self.datetime = datetime
        self.location = location
        self.description = description


db_uri = os.getenv("ATLAS_URI")
db_client = MongoClient(db_uri, server_api=ServerApi("1"))
db_cluster = db_client.Madhacks2023Cluster0
events_db = db_cluster.events


# triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def run_scrape_events(cloud_event):
    message = base64.b64decode(cloud_event.data["message"]["data"]).decode()
    if message == "scrape events":
        print("running scrape events")
        event_data = scrape_event_data()
        publish_to_db(event_data)


def scrape_event_data() -> [Event]:
    return [Event(0, "test event", "", "", "")]


def publish_to_db(event_data: [Event]):
    # clear all events in the db
    events_db.delete_many({})

    # convert the event data from array of classes to array of dictionaries (required by insert_many)
    doc = []
    for e in event_data:
        doc.append(e.__dict__)

    events_db.insert_many(doc)
