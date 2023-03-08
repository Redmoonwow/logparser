import websocket
import json
import numpy
import pandas
import re
import datetime
import io
import splatool_global as g

# ギミッククラス
import TOP_P5
import splatool_util

# config

# テストモード
fg_test_mode = True


fg_PT_setup_done = False
fg_gimmkck_open_fd = False
dammy_combatants_fd = 0
test_combatants_filename = ""
combatants_fd_name = ""

JOBLIST = {
	"00":"",
	"01":"",
	"02":"",
	"03":"",
	"04":"",
	"05":"",
	"06":"",
	"07":"",
	"08":"",
	"09":"",
	"0A":"",
	"0B":"",
	"0C":"",
	"0D":"",
	"0E":"",
	"0F":"",
	"10":"",
	"11":"",
	"12":"",
	"13":"PLD",
	"14":"MNK",
	"15":"WAR",
	"16":"DRG",
	"17":"BRD",
	"18":"WHM",
	"19":"BLM",
	"1A":"",
	"1B":"SMN",
	"1C":"SCH",
	"1D":"",
	"1E":"NIN",
	"1F":"MCH",
	"20":"DRK",
	"21":"AST",
	"22":"SAM",
	"23":"RDM",
	"24":"BLU",
	"25":"GNB",
	"26":"DNC",
	"27":"RPR",
	"28":"SGE"
}
JOBPRIO = {
	"DRK":0,
	"WAR":1,
	"GNB":2,
	"PLD":3,
	"WHM":4,
	"AST":5,
	"SCH":6,
	"SGE":7,
	"DRG":8,
	"MNK":9,
	"SAM":10,
	"RPR":11,
	"NIN":12,
	"BRD":13,
	"MCH":14,
	"DNC":15,
	"SMN":16,
	"BLM":17,
	"RDM":18,
	"":98,
	"BLU":99
}

MARKERLIST = {
	0:"Hexagon 1",
	1:"Hexagon 2",
	2:"Hexagon 3",
	3:"Hexagon 4",
	4:"Hexagon 5",
	5:"Chain 1",
	6:"Chain 2",
	7:"Chain 3",
	8:"Ignore 1",
	9:"Ignore 2",
	10:"Square",
	11:"Circle",
	12:"Plus",
	13:"Triangle"
}


Gimmick_class_00 = TOP_P5.top_p5()

def dump_function(message_dict):
	if (False == g.fg_combat):
		return
	if (0 == Gimmick_class_00.state_sigma):
		return
	#if (splatool_util.log_chk_combatant_entity_03(message_dict,"","15724")):
		#print(message_dict["rawLine"])


def Gimmick_branch(message_dict):
	global Gimmick_class_00
	dump_function(message_dict)
	#TOP P5
	if(splatool_util.log_chk_00(message_dict,"ガガ……ガガガガ……この力は、いったい……！？")):
		Gimmick_class_00.start(g.g.PT_array)
		return
	if(Gimmick_class_00.is_start == True):
		Gimmick_class_00.update_df(g.g.PT_array)
		Gimmick_class_00.log_chk(message_dict)
	return

def Gimmick_init():
	global Gimmick_class_00
	#TOP P5
	Gimmick_class_00.init()
	return

def func_InCombat(message_dict):
	#print(message_dict)
	"""
	if bool(message_dict["inGameCombat"]) != g.fg_combat:
		g.fg_combat = message_dict["inGameCombat"]
		if True == message_dict["inGameCombat"]:
			print("-----戦闘開始-----")
		else:
			print("-----戦闘終了-----")
	"""
	return

def func_ChangePrimaryPlayer(message_dict):
	g.MY_PC.loc[0,"ID"]	= format(message_dict["charID"],"X")
	g.MY_PC.loc[0,"name"]	= message_dict["charName"]
	json_fd = open("E:\\works\\1.projects\\svn\\logparser\\logparser\\json\\" + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime(r"%Y%m%d%H%M%S%f") + "_ChangePrimaryPlayer_data.json","w",encoding="utf-8")
	json_fd.write(json.dumps(message_dict, indent=4))
	json_fd.close()
	return

def func_ChangeZone(message_dict):
	global fg_PT_setup_done
	g.ZoneID = message_dict["g.ZoneID"]
	json_fd = open("E:\\works\\1.projects\\svn\\logparser\\logparser\\json\\" + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime(r"%Y%m%d%H%M%S%f") + "_" + message_dict["zoneName"] + "_ChangeZone_data.json","w",encoding="utf-8")
	json_fd.write(json.dumps(message_dict, indent=4))
	json_fd.close()
	fg_PT_setup_done = False
	return

def func_ChangeMap(message_dict):
	#print(message_dict)
	# ZoneIDだけでいい
	return

def func_PartyChanged(message_dict):
	i = 0
	for data in message_dict["party"]:
		g.PT_array.loc[i,"ID"] = data["id"]
		g.PT_array.loc[i,"name"] = data["name"]
		g.PT_array.loc[i,"JOB"] = JOBLIST[format(data["job"],"X")]
		g.PT_array.loc[i,"PRIO"] = JOBPRIO[g.PT_array["JOB"][i]]
		i += 1
	json_fd = open("E:\\works\\1.projects\\svn\\logparser\\logparser\\json\\" + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime(r"%Y%m%d%H%M%S%f") + "_PartyChanged_data.json","w",encoding="utf-8")
	json_fd.write(json.dumps(message_dict, indent=4))
	json_fd.close()
	return

def func_LogLine(message_dict):
	global fg_gimmkck_open_fd
	global gimmick_fd
	global fg_PT_setup_done
	global MARKERLIST
	linedata = message_dict["line"]
	if (	(249 <= int(linedata[0]))	and \
			(260 > int(linedata[0]))	):
		return
	match int(linedata[0]):
		case 40:
			return
		case 1:
			return
		case 2:
			return
		case 4:
			return
		case 21:
			return
		case 22:
			return
		case 24:
			return
		case 25:
			return
		case 28:
			return
		case 31:
			return
		case 36:
			return
		case 37:
			return
		case 12:
			return
		case 11:
			func_set_PTarray()
			return
		case 260:
			if ((int(linedata[3]) != g.fg_combat) and (fg_PT_setup_done == True)):
				g.fg_combat = int(linedata[3])
				if 1 == int(linedata[3]):
					gimmick_fd = open("E:\\works\\1.projects\\svn\\logparser\\logparser\\gimmick_file\\" + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y%m%d%H%M%S") + "_gimmick_data.log","w",encoding="utf-8")
					fg_gimmkck_open_fd = True
					gimmick_fd.write("---------------戦闘開始---------------\n")
					print("-----戦闘開始-----")
				else:
					gimmick_fd.write("---------------戦闘終了---------------\n")
					gimmick_fd.close()
					fg_gimmkck_open_fd = False
					Gimmick_init()
					print("-----戦闘終了-----")
			return
		case 38:
			if((True == g.PT_array[g.PT_array["ID"] == linedata[2]].empty) or (fg_PT_setup_done == False)):
				return
			else:
				ok = 1
			#print(str(message_dict["rawLine"]).replace("\n",""))
			g.PT_array.loc[g.PT_array["ID"] == linedata[2],"x"] = linedata[11]
			g.PT_array.loc[g.PT_array["ID"] == linedata[2],"y"] = linedata[12]
			g.PT_array.loc[g.PT_array["ID"] == linedata[2],"z"] = linedata[13]
			return
		case 39:
			if((True == g.PT_array[g.PT_array["ID"] == linedata[2]].empty) or (fg_PT_setup_done == False)):
				return
			else:
				ok = 1
			#print(str(message_dict["rawLine"]).replace("\n",""))
			g.PT_array.loc[g.PT_array["ID"] == linedata[2],"x"] = linedata[10]
			g.PT_array.loc[g.PT_array["ID"] == linedata[2],"y"] = linedata[11]
			g.PT_array.loc[g.PT_array["ID"] == linedata[2],"z"] = linedata[12]
			return
		case 0:
			chatID = linedata[2]
			chatauther = linedata[3]
			chatdata = linedata[4]
			if ("Hojoring" in chatdata):
				return
			if ("Sonar" in chatauther):
				return
			if ("0044" not in chatID):
				return
			#print(message_dict["rawLine"])
		case 20:
			#### 味方から発生してるバフはスキルバフなので除外する
			if(False == g.PT_array[g.PT_array["ID"] == linedata[2]].empty):
				return
			else:
				ok = 1
		case 26:
			#### 味方から発生してるバフはスキルバフなので除外する
			if(False == g.PT_array[g.PT_array["ID"] == linedata[5]].empty):
				return
			else:
				ok = 1
		case 30:
			#### 味方から発生してるバフはスキルバフなので除外する
			if(False == g.PT_array[g.PT_array["ID"] == linedata[5]].empty):
				return
			else:
				ok = 1
		case 29:
			# ターゲットマーカー操作
			if((True == g.PT_array[g.PT_array["ID"] == linedata[4]].empty) or (fg_PT_setup_done == False)):
				return
			else:
				ok = 1

			g.PT_array.loc[g.PT_array["ID"] == linedata[4],"HEADMARKER"] = [MARKERLIST[int(linedata[3])]]

	func_dammy_getCombatants(message_dict)


		
	#### ここにたどり着くログはギミック処理分岐でつかうためギミック処理分岐にまわす

	Gimmick_branch(message_dict)
	#print(str(message_dict["rawLine"]).replace("\n",""))
	if (fg_gimmkck_open_fd != False):
		gimmick_fd.write(str(message_dict["rawLine"]))
	
	return

def func_set_PTarray():
	global fg_PT_setup_done
	g.PT_array.loc[g.PT_array["ID"] == str(g.MY_PC.loc[0,"ID"]),"MINE"] = 1
	g.PT_array = g.PT_array.sort_values("PRIO")
	g.PT_array = g.PT_array.reset_index(drop=True)
	g.PT_array.loc[0,"NUMKEY"] = "num5"
	g.PT_array.loc[1,"NUMKEY"] = "num6"
	g.PT_array.loc[2,"NUMKEY"] = "num7"
	g.PT_array.loc[3,"NUMKEY"] = "num8"
	g.PT_array.loc[4,"NUMKEY"] = "num2"
	g.PT_array.loc[5,"NUMKEY"] = "num3"
	g.PT_array.loc[6,"NUMKEY"] = "num1"
	g.PT_array.loc[7,"NUMKEY"] = "num4"
	fg_PT_setup_done = True

def func_getCombatants(message_dict):
	global combatants_fd_name
	if ("" == combatants_fd_name):
		combatants_fd_name = "E:\\works\\1.projects\\svn\\logparser\\logparser\\combatants\\" + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime(r"%Y%m%d") + "_specificCombatants.csv"
	combatants_fd = open(combatants_fd_name,"a")
	g.combatants_df = pandas.DataFrame.from_dict(message_dict["combatants"])
	nowtime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime(r"%Y%m%d%H%M%S%f")
	for buf in message_dict["combatants"]:
		buf_str = str(buf).replace("{","")
		buf_str = str(buf_str).replace("}","")
		buf_str = str(buf_str).replace(" ","")
		buf_str = re.sub("\,(.*?)(:)",",",buf_str)
		buf_str = str(buf_str).replace("'","")
		buf_str = nowtime + "," + buf_str
		buf_str = str(buf_str).replace("ID:","")
		buf_str = str(buf_str).replace(" ","")
		combatants_fd.write(buf_str + "\n")
	combatants_fd.close()
	return

def func_dammy_getCombatants(message_dict):
	global test_combatants_filename
	global fg_test_mode
	global dammy_combatants_fd
	once = False
	if (False == fg_test_mode):
		return
	


	# 時間確認
	# logline
	logline_time = str(message_dict["line"][1])
	logline_time = logline_time.replace("+09:00","")
	logline_time = logline_time.replace("-","")
	logline_time = logline_time.replace(":","")
	logline_time = logline_time.replace(".","")
	logline_time = logline_time.replace("T","")
	logline_time = logline_time[:20]
	pre_seek_pos = dammy_combatants_fd.tell()
	data = str(dammy_combatants_fd.readline())
	if( "" == data):
		return
	data_time = data.split(",")[0]
	if (int(logline_time) < int(data_time)):
		dammy_combatants_fd.seek(pre_seek_pos)
		return
	data = data.replace("\n","")
	while True:
		combatants_df_line = pandas.read_csv(io.StringIO(data), header=None)
		combatants_df_line = combatants_df_line.set_axis(['time','ID', 'OwnerID', 'Type', 'ModelStatus', 'TargetID', 'IsTargetable','Job', 'Name', 'CurrentHP', 'MaxHP', 'PosX', 'PosY', 'PosZ', 'Heading','BNpcID', 'CurrentMP', 'MaxMP', 'Level', 'BNpcNameID', 'WorldID','CurrentWorldID', 'TransformationId', 'WeaponId', 'PartyType','WorldName'],axis=1)
	
		if(False == once):
			combatants_df_tmp = combatants_df_line
			once = True
		else:
			combatants_df_tmp = pandas.concat([combatants_df_tmp,combatants_df_line], join='inner')
		
		pre_seek_pos = dammy_combatants_fd.tell()
		data = str(dammy_combatants_fd.readline())
		if( "" == data):
			break

		if( data.split(",")[0] != data_time):
			dammy_combatants_fd.seek(pre_seek_pos)
			break

	g.combatants_df = combatants_df_tmp
	return

def main():
	#websocket.enableTrace(True)
	ws_cliant = websocket.WebSocket()
	ws_cliant.connect("ws://127.0.0.1:10501/ws",)
	ws_cliant.send('{"call":"subscribe","events":["ChangePrimaryPlayer"]}')
	ws_cliant.send('{"call":"subscribe","events":["ChangeZone"]}')
	ws_cliant.send('{"call":"subscribe","events":["ChangeMap"]}')
	ws_cliant.send('{"call":"subscribe","events":["PartyChanged"]}')
	ws_cliant.send('{"call":"subscribe","events":["LogLine"]}')
	ws_cliant.send('{"call":"subscribe","events":["InCombat"]}')
	ws_cliant.send('{"call":"subscribe","events":["OnlineStatusChanged"]}')
	ws_cliant.send('{"call":"getCombatants","ids":[],"props":["CurrentWorldID","WorldID","WorldName","BNpcID","BNpcNameID","PartyType","ID","OwnerID","Type","type","Job","Level","Name","CurrentHP","MaxHP","CurrentMP","MaxMP","PosX","PosY","PosZ","Heading","TargetID","ModelStatus","IsTargetable","TransformationId","WeaponId"],"rseq":"specificCombatants"}')
	#ws_cliant.send('{"call":"subscribe","events":["GameVersion"]}')
	#ws_cliant.send('{"rseq":"getLanguage","call":"getLanguage"}')
	#ws_cliant.send('{"rseq":"getVersion","call":"getVersion"}')
	ws_cliant.send('{"rseq":"allCombatants","props":["CurrentWorldID","WorldID","WorldName","BNpcID","BNpcNameID","PartyType","ID","OwnerID","Type","type","Job","Level","Name","CurrentHP","MaxHP","CurrentMP","MaxMP","PosX","PosY","PosZ","Heading","TargetID","ModelStatus","IsTargetable","TransformationId","WeaponId"],"call":"getCombatants"}')
	
	while True:
		data:dict = json.loads(ws_cliant.recv())
		if "combatants" in data.keys():
			func_getCombatants(data)
			ws_cliant.send('{"call":"getCombatants","ids":[],"props":["CurrentWorldID","WorldID","WorldName","BNpcID","BNpcNameID","PartyType","ID","OwnerID","Type","type","Job","Level","Name","CurrentHP","MaxHP","CurrentMP","MaxMP","PosX","PosY","PosZ","Heading","TargetID","ModelStatus","IsTargetable","TransformationId","WeaponId"],"rseq":"specificCombatants"}')
			continue #nop
		#print(data)
		match data["type"]:
			case "ChangePrimaryPlayer":
				func_ChangePrimaryPlayer(data)
			case "ChangeZone":
				func_ChangeZone(data)
			#case "ChangeMap":
			#	func_ChangeMap(data)
			case "PartyChanged":
				func_PartyChanged(data)
			case "LogLine":
				func_LogLine(data)
			case "InCombat":
				func_InCombat(data)
#			case "OnlineStatusChanged":
#				func_OnlineStatusChanged(data)
#			case "getCombatants":
#				func_getCombatants(data)

def damy_main():
	global fg_test_mode
	global test_combatants_filename
	global dammy_combatants_fd
	splatool_util.set_test()
	test_combatants_filename = "E:\\works\\1.projects\\svn\\logparser\\logparser\\combatants\\20230308_specificCombatants.csv"
	dammy_combatants_fd = open(test_combatants_filename,"r")
	log_p = open(r"E:\\logs\\Network_26801_20230308.log",encoding = "utf-8")
	pchg_data = open(r"E:\\works\\1.projects\\svn\\logparser\\logparser\\json\\20230308124533517425_ChangePrimaryPlayer_data.json")
	PTchg_data = open(r"E:\\works\\98.tmp\\20230301095402_PartyChanged_data.json")
	func_ChangePrimaryPlayer(json.load(pchg_data))
	func_PartyChanged(json.load(PTchg_data))
	for log_rawdata in log_p:
		log_array = log_rawdata.split("|")
		log_dict = { "rawLine":log_rawdata,"line":log_array }
		func_LogLine(log_dict)

if __name__ == "__main__":
	if (True == fg_test_mode):
		damy_main()
	else:
		main()

