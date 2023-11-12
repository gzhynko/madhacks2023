import functions_framework
import json

from typing import Optional
from datetime import datetime

from common import *


# triggered by an http request.
@functions_framework.http
def run_get_events(request):
    request_args = request.args

    building_str = request_args["building"]
    time_str = request_args["time"]
    if not building and not time:
        return "Query should include at least one of the following arguments: building, time"

    time = datetime.strptime(time_str, date_format) if time_str else None
    building = building_str if building_str else None

    return json.dumps(get_events(time, building))


def get_events(building: Optional[str], time: Optional[datetime.datetime]) -> [Event]:
    query = []
    if time:
        query.append({""})
