import urllib.request
import urllib.error
import json
import os
import time
from defcot import *
from decimal import Decimal
import datetime as dt
import socket

ATAK_IP = os.getenv('ATAK_IP', '127.0.0.1')
ATAK_PORT = int(os.getenv('ATAK_PORT', '8087'))
ATAK_PROTO = os.getenv('ATAK_PROTO', 'TCP')
INTERVAL = 60

sessionID = ""
accountRef = "USERNAME"
accountPass = "PASSWORD"
accountID = ""


def Login():
	r = urllib.request.urlopen('http://mobile.trackserver.co.uk/api/api/MobileApp/Login?AccountName='+accountRef+'&AccountPassword='+accountPass+'&SessionID=')
	json_data = r.read()
	parsed_json = (json.loads(json_data))
	global sessionID
	sessionID=parsed_json["SessionID"]
	global accountID
	accountID=parsed_json["AccountID"]


def PullDevices():
	try:
		r = urllib.request.urlopen('http://mobile.trackserver.co.uk/api/api/MobileApp/GetDeviceData?SessionID='+sessionID+'&AccountID='+str(accountID)+'&PullAll=true')
	except urllib.error.HTTPError:
		Login()
		r = urllib.request.urlopen('http://mobile.trackserver.co.uk/api/api/MobileApp/GetDeviceData?SessionID='+sessionID+'&AccountID='+str(accountID)+'&PullAll=true')
	json_data = r.read()
	parsed_json = (json.loads(json_data))
	for device in parsed_json['Devices']:
		speed = Decimal(device["SpeedKPH"])*Decimal(0.2777778) #0.2777778 is 1 kph
		now = dt.datetime.now()
		stale_part = now.minute + 1
		if stale_part > 59:
			stale_part = stale_part - 60
		stale_now = now.replace(minute=stale_part)
		evt = Event(2, "a-h-G-E-V-C", device["Name"], now, now, stale_now, "m-g")
		evt.point = Event.Point(device["Lat"], device["Lon"], 0, 10, 10)
		evt.detail = Event.Detail()
		evt.detail.track = Event.Detail.Track(device["Heading"], speed)
		evt.detail.status = Event.Detail.Status(device["BatteryLevel"])
		if str(device["MotionStatus"]) == "1":
			remark_string = "Device Moving: true"
		else:
			remark_string = "Device Moving: false"
		remark_string += "\nLast Comm: "+str(device["LastCommTime"])+"\nLast GPS Fix: "+str(device["LastGPSFix"])
		evt.detail.remark = Event.Detail.Remark(remark_string)
		SendTakMessage(evt)
		time.sleep(5)


def flush(socket):
	socket.settimeout(0.5)
	while True:
		try:
			socket.recv(2048)
			pass
		except:
			break
	socket.settimeout(5)

def pushTCP(ip_address, port, cot_xml):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("connect to server\n")
	sock.connect((ip_address, port))
	print("flush connection\n")
	flush(sock)
	final_xml=('<?xml version="1.0" standalone="yes"?>'+ET.tostring(cot_xml, encoding="unicode")).encode('utf-8')
	print(final_xml)
	print("send data\n")
	bytes_send = sock.send(final_xml)
	print(str(bytes_send) + " bytes of CoT-message length " + str(len(final_xml)) + " sent to " + ATAK_IP + " on port " + str(ATAK_PORT))
	time.sleep(1)
	print("read the response\n")
	print(sock.recv(2048))
	sock.close()
	return bytes_send


def SendTakMessage(params):
	cot = params.generate_cot()
	sent = pushTCP(ATAK_IP, ATAK_PORT, cot)


while True:	
	PullDevices()
	time.sleep(INTERVAL)
