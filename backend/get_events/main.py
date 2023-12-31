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
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return Response("", 204, headers)

    # Set CORS headers for the main request
    headers = {"Access-Control-Allow-Origin": "*"}

    request_json = request.json

    building_str = request_json.get("building")
    start_time_str = request_json.get("start_time")
    end_time_str = request_json.get("end_time")
    if not building_str and not start_time_str and not end_time_str:
        return Response(
            "Query should include at least one of the following arguments: building, start_time, end_time",
            200,
            headers,
            "text/plain",
        )

    start_time = (
        datetime.strptime(start_time_str, date_format) if start_time_str else None
    )
    end_time = datetime.strptime(end_time_str, date_format) if end_time_str else None
    building = building_str if building_str else None

    return Response(
        json_util.dumps(get_events(building, start_time, end_time)),
        200,
        headers,
        "application/json",
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

    query_results = events_db.find(query)

    frontend_data = []
    for result in query_results:
        frontend_data.append(
            {
                "name": result.get("name"),
                "start_datetime": result.get("start_datetime"),
                "end_datetime": result.get("end_datetime"),
                "building_name": result.get("building_name"),
                "full_location": result.get("full_location"),
                "description": result.get("description"),
            }
        )

    return frontend_data
