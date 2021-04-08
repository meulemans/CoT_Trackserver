import datetime as dt
import json
import urllib.error
import urllib.request
from decimal import Decimal

import CoT_Trackserver


def login() -> tuple:
    r = urllib.request.urlopen(
        'http://mobile.trackserver.co.uk/api/api/MobileApp/Login?AccountName=' + CoT_Trackserver.constants.accountRef + '&AccountPassword=' + CoT_Trackserver.constants.accountPass + '&SessionID=')
    json_data = r.read()
    parsed_json = (json.loads(json_data))
    sessionID = parsed_json["SessionID"]
    accountID = parsed_json["AccountID"]
    return sessionID, accountID


def json_to_cot(device, stale) -> CoT_Trackserver.Event:
    speed = Decimal(device["SpeedKPH"]) * Decimal(0.2777778)  # 0.2777778 is 1 kph
    time = dt.datetime.now(dt.timezone.utc)

    evt = CoT_Trackserver.Event(2, "a-h-G-E-V-C", device["Name"], time, time, time + dt.timedelta(seconds=stale),
                            "m-g")
    evt.point = CoT_Trackserver.Event.Point(device["Lat"], device["Lon"], 0, 10, 10)
    evt.detail = CoT_Trackserver.Event.Detail()
    evt.detail.uid = CoT_Trackserver.Event.Detail.Uid()
    evt.detail.uid.attributes = {"Droid": device["Name"]}
    evt.detail.track = CoT_Trackserver.Event.Detail.Track(device["Heading"], speed)
    evt.detail.status = CoT_Trackserver.Event.Detail.Status(device["BatteryLevel"])
    if str(device["MotionStatus"]) == "1":
        remark_string = "Device Moving: true"
    else:
        remark_string = "Device Moving: false"
    remark_string += " Last Comm: " + str(device["LastCommTime"]) + " Last GPS Fix: " + str(
        device["LastGPSFix"])
    evt.detail.remark = CoT_Trackserver.Event.Detail.Remark(remark_string)
    return evt


def hello_event() -> CoT_Trackserver.Event:
    time = dt.datetime.now(dt.timezone.utc)
    name = 'CoT_Trackserver'
    callsign = 'CoT_Trackserver'

    event = CoT_Trackserver.Event(2.0, 'a-n-G-E-S', name, time, time, time + dt.timedelta(hours=1), 'h-g-i-g-o')
    event.point = CoT_Trackserver.Event.Point(9999999.0, 9999999.0, 9999999.0, 9999999.0, 9999999.0)
    event.detail = CoT_Trackserver.Event.Detail()
    event.detail.contact = CoT_Trackserver.Event.Detail.Contact(callsign)
    event.detail.uid = CoT_Trackserver.Event.Detail.Uid()
    event.detail.uid.attributes = {"Droid": name}

    return event
