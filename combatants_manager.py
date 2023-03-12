import websocket
import json
import pandas
import datetime
import splatool_global as g
import time


# ギミッククラス
import splatool_util

# config

# テストモード
fg_test_mode = False
fg_PT_setup_done = False
fg_gimmkck_open_fd = False
dammy_combatants_fd = 0
test_combatants_filename = ""
dammy_combatants_df = ""
wipeout_cnt = 1
log_fd = 0

def func_getCombatants(message_dict):
	g.combatants_df = pandas.DataFrame.from_dict(message_dict["combatants"])
	g.combatants_df = g.combatants_df.fillna(0)

	if(0 == g.fg_combat):
		return

	nowtime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime(r"%Y%m%d%H%M%S%f")
	g.combatants_df.to_csv("E:\\works\\1.projects\\svn\\logparser\\logparser\\combatants\\combatants_tmp\\" + nowtime + "_specificCombatants.csv")
	return

def main():
	global log_fd
	ws_cliant = websocket.WebSocket()
	ws_cliant.connect("ws://127.0.0.1:10501/ws",)
	ws_cliant.send('{"call":"getCombatants","ids":[],"props":["CurrentWorldID","WorldID","WorldName","BNpcID","BNpcNameID","PartyType","ID","OwnerID","Type","type","Job","Level","Name","CurrentHP","MaxHP","CurrentMP","MaxMP","PosX","PosY","PosZ","Heading","TargetID","ModelStatus","IsTargetable","TransformationId","WeaponId"],"rseq":"specificCombatants"}')
	ws_cliant.send('{"rseq":"allCombatants","props":["CurrentWorldID","WorldID","WorldName","BNpcID","BNpcNameID","PartyType","ID","OwnerID","Type","type","Job","Level","Name","CurrentHP","MaxHP","CurrentMP","MaxMP","PosX","PosY","PosZ","Heading","TargetID","ModelStatus","IsTargetable","TransformationId","WeaponId"],"call":"getCombatants"}')
	
	while True:
		rawdata = ws_cliant.recv()
		data:dict = json.loads(rawdata)
		g.combatants_df = pandas.DataFrame.from_dict(data["combatants"])
		g.combatants_df = g.combatants_df.fillna(0)

		if(1 == g.fg_combat):
			log_fd.write(rawdata + "\n")
		
		time.sleep(0.8)
		ws_cliant.send('{"call":"getCombatants","ids":[],"props":["CurrentWorldID","WorldID","WorldName","BNpcID","BNpcNameID","PartyType","ID","OwnerID","Type","type","Job","Level","Name","CurrentHP","MaxHP","CurrentMP","MaxMP","PosX","PosY","PosZ","Heading","TargetID","ModelStatus","IsTargetable","TransformationId","WeaponId"],"rseq":"specificCombatants"}')


"""
def damy_main():
	global fg_test_mode
	global dammy_combatants_df
	splatool_util.set_test()
	globdata = glob.glob(r"E:\\works\\1.projects\\svn\\logparser\\logparser\\combatants\\combatants_tmp\\*")
	dammy_combatants_df = pandas.DataFrame(globdata,columns=["path"])
	for index, row in dammy_combatants_df.iterrows():
		dammy_combatants_df.loc[index,"time"] = (str(os.path.basename(row["path"])).split("_")[0])
	log_p = open(r"E:\\logs\\Network_26801_20230308_1.log",encoding = "utf-8")

	for log_rawdata in log_p:
		log_array = log_rawdata.split("|")
		log_dict = { "rawLine":log_rawdata,"line":log_array }

def damy_main_netw():
	global fg_test_mode
	splatool_util.set_test()
	log_p = open(r"E:\\logs\\Network_26801_20230308_1.log",encoding = "utf-8")
	for log_rawdata in log_p:
		func_LogLine(log_rawdata)
"""

if __name__ == "__main__":
	main()

