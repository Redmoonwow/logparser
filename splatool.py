import websocket
import json
import numpy
import pandas
import re
import datetime
import io
import splatool_global as g
import tarfile
import shutil
import os
import glob


# ギミッククラス
import TOP_P5
import splatool_util

# config

# テストモード
fg_test_mode = False
INIT_state = 0
primary_pc_set_done = False
fg_gimmkck_open_fd = False
dammy_combatants_fd = 0
test_combatants_filename = ""
dammy_combatants_df = ""
wipeout_cnt = 1
log_fd = 0
write_buf = ""
req_write = True

ChangePrimaryPlayer_data=""
ChangeZone_data=""
PartyChanged_data=""
InCombat_data=""

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

def updataPT_array():
	if(g.combatants_df.empty):
		return
	for index, row in g.PT_array.iterrows():
		if((True == g.combatants_df[g.combatants_df["ID"] == int(row["ID"],16)].empty)):
			continue
		df = g.combatants_df[g.combatants_df["ID"] == int(row["ID"],16)]
		df = df.reset_index(drop=True)
		g.PT_array.loc[index,"x"] = df["PosX"][0]
		g.PT_array.loc[index,"y"] = df["PosY"][0]
		g.PT_array.loc[index,"z"] = df["PosZ"][0]
	return

def dump_function(message_dict):
	if (0 == g.fg_combat):
		return
	if (0 == Gimmick_class_00.state_sigma):
		return

def Gimmick_branch(message_dict):
	global Gimmick_class_00
	
	#TOP P5
	if(splatool_util.log_chk_00(message_dict,"実装……共闘者の存在…… 戦闘行為におけるロール分担の有用性を検証します……。")):
		splatool_util.chatprint("#### TOP_P2 start")
		return
	if(splatool_util.log_chk_00(message_dict,"ガガガ……ハードウェア、耐久限界を超越…… そうだとしても……強く……もっと強く……！")):
		splatool_util.chatprint("#### TOP_P4 start")
		return
	if(splatool_util.log_chk_00(message_dict,"ガガ……ガガガガ……この力は、いったい……！？")):
		splatool_util.chatprint("#### TOP_P5 start")
		Gimmick_class_00.start(g.PT_array)
		return
	if(Gimmick_class_00.is_start == True):
		Gimmick_class_00.update_df(g.PT_array)
		Gimmick_class_00.log_chk(message_dict)
	return

def Gimmick_init():
	global Gimmick_class_00
	#TOP P5
	Gimmick_class_00.init()
	return

def func_InCombat(message_dict):
	global log_fd
	global wipeout_cnt
	global ChangeZone_data
	global PartyChanged_data
	global ChangePrimaryPlayer_data
	global write_buf
	if ((int(message_dict["inGameCombat"]) != g.fg_combat)):
				g.fg_combat = int(message_dict["inGameCombat"])
				if 1 == int(message_dict["inGameCombat"]):
					if(False ==  fg_test_mode):
						log_fd = open("E:\\works\\1.projects\\svn\\logparser\\logparser\\gimmick_file\\" + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y%m%d%H%M%S") + " try_" + str(g.ZoneID) + "_" + str(wipeout_cnt) +"_gimmick_data.log","w",encoding="utf-8")
						wipeout_cnt += 1
						write_buf = write_buf + ChangePrimaryPlayer_data + "\n"
						write_buf = write_buf + ChangeZone_data + "\n"
						if("" != PartyChanged_data):
							log_fd.write(PartyChanged_data + "\n")
					splatool_util.chatprint("-----戦闘開始-----")
				else:
					if(False ==  fg_test_mode):
						if(len(write_buf) != 0):
							log_fd.write(write_buf)
						write_buf = ""
						log_fd.close()
					Gimmick_init()
					splatool_util.chatprint("-----戦闘終了-----")
	return

def func_ChangePrimaryPlayer(message_dict):
	global primary_pc_set_done
	g.MY_PC.loc[0,"ID"]	= format(message_dict["charID"],"X")
	g.MY_PC.loc[0,"name"]	= message_dict["charName"]
	primary_pc_set_done = True
	return

def func_ChangeZone(message_dict):
	global INIT_state
	global wipeout_cnt
	g.ZoneID = message_dict["zoneID"]
	wipeout_cnt = 1
	return	

def func_ChangeMap(message_dict):
	#print(message_dict)
	# ZoneIDだけでいい
	return

def func_PartyChanged(message_dict):
	global INIT_state
	global primary_pc_set_done
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
	if (True == primary_pc_set_done):
		func_set_PTarray()
	INIT_state = 1
	splatool_util.chatprint("-----PT RESTART-----")
	return

def func_LogLine(message_dict):
	global fg_gimmkck_open_fd
	global MARKERLIST
	global wipeout_cnt
	global req_write
	linedata = message_dict["line"]
	if ((249 <= int(linedata[0]))	and	(260 >= int(linedata[0]))):
		req_write = False
		return
	if (int(linedata[0]) in [1,2,4,21,22,24,25,28,31,36,37,12,11,38,39]):
		req_write = False
		return
	if(00 == int(linedata[0])):
		chatID = linedata[2]
		chatauther = linedata[3]
		chatdata = linedata[4]
		if ("Hojoring" in chatdata):
			req_write = False
			return
		if ("Sonar" in chatauther):
			req_write = False
			return
		if ("0044" not in chatID):
			req_write = False
			return
	if (int(linedata[0]) in [20]):
		#### 味方から発生してるバフはスキルバフなので除外する
		if(False == g.PT_array[g.PT_array["ID"] == linedata[2]].empty):
			req_write = False
			return
		else:
			ok = 1
	if (int(linedata[0]) in [26,30]):
		#### 味方から発生してるバフはスキルバフなので除外する
		if(False == g.PT_array[g.PT_array["ID"] == linedata[5]].empty):
			req_write = False
			return
		else:
			ok = 1
	if(29 == int(linedata[0])):
		# ターゲットマーカー操作
		g.PT_array.loc[g.PT_array["ID"] == linedata[4],"HEADMARKER"] = [MARKERLIST[int(linedata[3])]]

		
	#### ここにたどり着くログはギミック処理分岐でつかうためギミック処理分岐にまわす
	#if(False ==  fg_test_mode):
	#	print(str(message_dict["rawLine"]).replace("\n",""))

	if(g.fg_combat == 1):
		Gimmick_branch(message_dict)
	
	return

def func_set_PTarray():
	global INIT_state
	g.PT_array.loc[g.PT_array["ID"] == str(g.MY_PC.loc[0,"ID"]),"MINE"] = 1
	g.PT_array = g.PT_array.sort_values("PRIO")
	g.PT_array = g.PT_array.reset_index(drop=True)
	g.PT_array.loc[0,"NUMKEY"] = "5"
	g.PT_array.loc[1,"NUMKEY"] = "6"
	g.PT_array.loc[2,"NUMKEY"] = "7"
	g.PT_array.loc[3,"NUMKEY"] = "8"
	g.PT_array.loc[4,"NUMKEY"] = "2"
	g.PT_array.loc[5,"NUMKEY"] = "3"
	g.PT_array.loc[6,"NUMKEY"] = "1"
	g.PT_array.loc[7,"NUMKEY"] = "4"
	INIT_state += 1

def main():
	global ChangePrimaryPlayer_data
	global ChangeZone_data
	global PartyChanged_data
	global InCombat_data
	global log_fd
	global write_buf
	global req_write
	global fg_test_mode
	global INIT_state
	once = False
	dsp_cnt = 0
	if (False == fg_test_mode):
		#websocket.enableTrace(True)
		ws_cliant = websocket.WebSocket()
		ws_cliant.connect("ws://127.0.0.1:10501/ws",)
		ws_cliant.send('{"call":"subscribe","events":["ChangePrimaryPlayer"]}')
		ws_cliant.send('{"call":"subscribe","events":["ChangeZone"]}')
		#ws_cliant.send('{"call":"subscribe","events":["ChangeMap"]}')
		ws_cliant.send('{"call":"subscribe","events":["PartyChanged"]}')
		ws_cliant.send('{"call":"subscribe","events":["LogLine"]}')
		ws_cliant.send('{"call":"subscribe","events":["InCombat"]}')
		#ws_cliant.send('{"call":"subscribe","events":["OnlineStatusChanged"]}')
		#ws_cliant.send('{"call":"getCombatants","ids":[],"props":["CurrentWorldID","WorldID","WorldName","BNpcID","BNpcNameID","PartyType","ID","OwnerID","Type","type","Job","Level","Name","CurrentHP","MaxHP","CurrentMP","MaxMP","PosX","PosY","PosZ","Heading","TargetID","ModelStatus","IsTargetable","TransformationId","WeaponId"],"rseq":"specificCombatants"}')
		#ws_cliant.send('{"rseq":"allCombatants","props":["CurrentWorldID","WorldID","WorldName","BNpcID","BNpcNameID","PartyType","ID","OwnerID","Type","type","Job","Level","Name","CurrentHP","MaxHP","CurrentMP","MaxMP","PosX","PosY","PosZ","Heading","TargetID","ModelStatus","IsTargetable","TransformationId","WeaponId"],"call":"getCombatants"}')
		#ws_cliant.send('{"rseq":"allCombatants","props":["BNpcID","BNpcNameID","ID","Type","Name","PosX","PosY","PosZ","TransformationId","WeaponId"],"call":"getCombatants"}')
	else:
		if (False == once):
			splatool_util.set_test()
			fg_test_mode = True
			log_p = open(r"E:\works\\1.projects\\svn\\logparser\\logparser\\gimmick_file\\20230315224623 try_1122_2_gimmick_data.log",encoding = "utf-8")
			once = True

	while True:
		if (False == fg_test_mode):
			rawdata = ws_cliant.recv()
		else:
			rawdata = log_p.readline()
			if (rawdata == ""):
				return
			
		# PTセットアップ確認
		if (3 > INIT_state):
			if((1 <= INIT_state) and (True == primary_pc_set_done)):
				func_set_PTarray()
			else:
				if(0 == dsp_cnt):
					splatool_util.chaterror("[ERROR] func_set_PTarray()")
					dsp_cnt = 200
				else:
					dsp_cnt -= 1
			if(2 <= INIT_state):
				dsp_cnt = 0
				df_bool = int(g.PT_array["MINE"].sum())
				if(1 < df_bool):
					if(0 == dsp_cnt):
						splatool_util.chaterror("[ERROR] MINE is not unique")
						dsp_cnt = 200
					else:
						dsp_cnt -= 1
				else:
					INIT_state += 1
			if(3 <= INIT_state):
				splatool_util.chatprint("[INFO ] PT set done")
		else:
			df_bool = int(g.PT_array["MINE"].sum())
			if(1 < df_bool):
				splatool_util.chaterror("[ERROR] MINE is not unique RE_INIT START")
				INIT_state = 1


		data:dict = json.loads(rawdata)
		if "combatants" in data.keys():
			#func_getCombatants(data)
			ws_cliant.send('{"call":"getCombatants","ids":[],"props":["CurrentWorldID","WorldID","WorldName","BNpcID","BNpcNameID","PartyType","ID","OwnerID","Type","type","Job","Level","Name","CurrentHP","MaxHP","CurrentMP","MaxMP","PosX","PosY","PosZ","Heading","TargetID","ModelStatus","IsTargetable","TransformationId","WeaponId"],"rseq":"specificCombatants"}')
			continue
		else:
			if (data["type"] == "ChangePrimaryPlayer"):
				func_ChangePrimaryPlayer(data)
				ChangePrimaryPlayer_data=rawdata
			elif (data["type"] == "ChangeZone"):
				func_ChangeZone(data)
				ChangeZone_data=rawdata
			elif (data["type"] == "PartyChanged"):
				func_PartyChanged(data)
				PartyChanged_data=rawdata
			elif (data["type"] == "LogLine"):
				func_LogLine(data)
			elif (data["type"] == "InCombat"):
				func_InCombat(data)
				InCombat_data = rawdata
		if((1 == g.fg_combat) and True == req_write):
			write_buf = write_buf + rawdata + "\n"
			if(len(write_buf) >= 1048576):
				log_fd.write(write_buf)
				write_buf = ""

		req_write = True

if __name__ == "__main__":
	main()

