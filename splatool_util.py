import pandas
import datetime
import pyautogui
import urllib.parse
import json
import requests
import math
import numpy as np

fg_test = False

def set_test():
	global fg_test
	fg_test = True


def calc_2point_pos(center_x,center_y,a_x,a_y,b_x,b_y):
	#角度計算開始
	vec1=[a_x-center_x,a_y-center_y]
	vec2=[b_x-center_x,b_y-center_y]
	absvec1=np.linalg.norm(vec1)
	absvec2=np.linalg.norm(vec2)
	inner=np.inner(vec1,vec2)
	cross=np.cross(vec1,vec2)
	cos_theta=inner/(absvec1*absvec2)
	theta=math.degrees(math.acos(cos_theta))
	return float(round(theta,2))

"""
def calc_2point_pos(center_x,center_y,a_x,a_y,b_x,b_y):
	a = np.array([center_x, center_y])
	b = np.array([b_x, b_y])
	vec = b - a
	a = np.rad2deg(np.arctan2(vec[0], vec[1]))
	return float(round(a,2))
"""

# log parse functions
def log_chk_00(message_dict,chk_message):
	linedata = message_dict["line"]
	if (linedata[0] == "00"):
		if (linedata[4] == chk_message):
			return True

	return False

def log_chk_get_buff_26(message_dict,buffID):
	linedata = message_dict["line"]
	if (linedata[0] == "26"):
		if (linedata[2] == buffID):
			return True

	return False

	return False

def log_chk_combatant_entity_03(message_dict,npcnameid,npcid):
	linedata = message_dict["line"]
	if (linedata[0] == "03"):
		a = 1
		if ("" != npcnameid):
			if (linedata[9] == npcnameid):
				return True
		if ("" != npcid):
			if (linedata[10] == npcid):
				return True
	return False

# splatoon Control Function

#d = {'elements': 'eyJOYW1lIjoidGVzdCIsInR5cGUiOjMsInJlZlkiOjI3LjAsInJhZGl1cyI6NTAuMCwiY29sb3IiOjE2Nzc3MjE4NTUsInJlZkFjdG9yTlBDTmFtZUlEIjo3Njk1LCJyZWZBY3RvckNvbXBhcmlzb25UeXBlIjo2LCJpbmNsdWRlUm90YXRpb24iOnRydWUsIm9ubHlWaXNpYmxlIjp0cnVlLCJBZGRpdGlvbmFsUm90YXRpb24iOjEuMzA4OTk2OX0=',"namespace":"extope"}
"""
d = {"namespace":"extope"}
jsondata = '%7b%22Name%22%3a%22ELEMENTS%22%2c%22type%22%3a1%2c%22radius%22%3a1.69%2c%22refActorNPCID%22%3a0%2c%22refActorComparisonType%22%3a4%2c%22includeRotation%22%3atrue%7d'
tp = urllib.parse.unquote(jsondata)
tp = json.loads(tp)
jsondata = json.dumps(tp)
#d = {'raw': '%7b%22Name%22%3a%22omj%22%2c%22type%22%3a3%2c%22refY%22%3a27.0%2c%22radius%22%3a50.0%2c%22color%22%3a1677721855%2c%22refActorNPCID%22%3a7695%2c%22refActorComparisonType%22%3a4%2c%22includeRotation%22%3atrue%2c%22onlyVisible%22%3atrue%2c%22AdditionalRotation%22%3a1.3089969%7d',"namespace":"extope"}
#tp = urllib.parse.urlencode(d)
#a = urllib.parse.unquote(d["raw"])
#c = json.loads(a)
#c["refActorNPCID"] = 0
#c = json.dumps(a)
#d["raw"] = urllib.parse.quote(c)
#d = {"destroy":"extope"}
d_qs = urllib.parse.urlencode(d)
requests.post("http://127.0.0.1:47774?" + d_qs,data=jsondata)

#jsondata = { "version": 1, "id": 123456, "type": "ExecuteCommand", "payload": { "command": "/mk attack1 <1>" } }
#requests.post("http://localhost:51323/",data= json.dumps(jsondata))


d = {"destroy":"extope"}
d_qs = urllib.parse.urlencode(d)
requests.post("http://127.0.0.1:47774?" + d_qs)
"""
# telesto Control Function
def chatprint(string):
	global fg_test
	if (False == fg_test):
		jsondata = { "version": 1, "id": 666666, "type": "PrintMessage", "payload": { "message": string } }
		requests.post("http://localhost:51323/",data= json.dumps(jsondata))
	print(string)

def ExecuteCommand(string):
	if (False == fg_test):
		jsondata = { "version": 1, "id": 123456, "type": "ExecuteCommand", "payload": { "command": string } }
		requests.post("http://localhost:51323/",data= json.dumps(jsondata))
