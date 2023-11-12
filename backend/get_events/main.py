import functions_framework

from typing import Optional
from datetime import datetime
from flask import Response
from bson import json_util

from common import *

date_format = "%Y-%m-%d_%H:%M:%S"


# triggered by an http request.
@functions_framework.http
def run_get_events(request):
    request_json = request.json

    building_str = request_json.get("building")
    start_time_str = request_json.get("start_time")
    end_time_str = request_json.get("end_time")
    if not building_str and not start_time_str and not end_time_str:
        return Response(
            "Query should include at least one of the following arguments: building, start_time, end_time",
            mimetype="text/plain",
        )

    start_time = (
        datetime.strptime(start_time_str, date_format) if start_time_str else None
    )
    end_time = datetime.strptime(end_time_str, date_format) if end_time_str else None
    building = building_str if building_str else None

    return Response(
        json_util.dumps(get_events(building, start_time, end_time)),
        mimetype="text/plain",
    )


def get_events(
    building: Optional[str],
    start_time: Optional[datetime],
    end_time: Optional[datetime],
):
    query = {}
    if start_time and end_time:
        query["start_datetime"] = {"$lte": end_time}
        query["end_datetime"] = {"$gte": start_time}
    if building:
        query["building_name"] = building

    return list(events_db.find(query))
