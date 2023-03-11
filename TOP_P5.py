#import splatool
import pandas
import datetime
import splatool_util
import math
import splatool_global as g
import json
import time
import random
from decimal import Decimal, ROUND_HALF_UP
from numba import jit

SIGMA_OMEGA_ARM_POS = {
	"marker":	["A",	"1",	"B",	"2",	"C",	"3",	"D",	"4"],
	"x":		[100,	107,	110,	107,	100,	93,		90,		93]	,
	"y":		[90,	93,		100,	107,	110,	107,	100,	93]
}

SIGMA_OMEGA_M_POS = {
	"marker":	["A",		"1",	"B",	"2",	"C",	"3",	"D",	"4"],
	"x":		[100.00,	114.14,	120.00,	114.14,	100.00,	85.86,	80.00,	85.86],
	"y":		[80.00,		85.86,	100.00,	114.14,	120.00,	114.14,	100.00,	85.86]
}

SIGMA_OMEGA_M_MARKER = {
	"marker":	["A",	"1",	"B",	"2",	"C",	"3",	"D",	"4"],
	"MARK1":	["2",	"C",	"3",	"D",	"4",	"A",	"1",	"B"],
	"MARK2":	["3",	"D",	"4",	"A",	"1",	"B",	"2",	"C"]
}

SIGMA_OMEGA_M_POS_MARKERS = {
	"A":["AC","BD","1","3","4","2"],
	"1":["13","24","B","D","A","C"],
	"B":["BD","AC","2","4","1","3"],
	"2":["24","13","C","A","B","D"],
	"C":["AC","BD","3","1","2","4"],
	"3":["13","24","D","B","C","A"],
	"D":["BD","AC","4","2","3","1"],
	"4":["24","13","A","C","D","B"]
}

PLAYSTATION_PRIO = {
	"Circle":0,
	"Cross":1,
	"Triangle":2,
	"square":3
}

class top_p5:
	__PT_Data				= pandas.DataFrame()
	__SIGMA_OMEGA_M_POS		= pandas.DataFrame()
	__SIGMA_OMEGA_ARM_POS	= pandas.DataFrame()
	__SIGMA_OMEGA_M_POS		= pandas.DataFrame()
	world_cnt				= 0
	line_cnt				= 0
	playstation_cnt			= 0
	tmp_cnt					= 0
	tmp_data				= 0
	is_start				= False
	state_delta				= 0
	state_sigma				= 0
	state_omega				= 0

	sigma_omegaM_marker_pos	= ""
	fg_sigma_once			= False
	my_marker				= ""
	
	def __init__(self):
		self.__PT_Data = pandas.DataFrame()
		self.__SIGMA_OMEGA_ARM_POS = pandas.DataFrame(SIGMA_OMEGA_ARM_POS)
		self.__SIGMA_OMEGA_M_MARKER = pandas.DataFrame(SIGMA_OMEGA_M_MARKER)
		self.__SIGMA_OMEGA_M_POS  = pandas.DataFrame(SIGMA_OMEGA_M_POS)
		self.__PT_Data["Dynamis"] = 0
		self.__PT_Data["1BMARKER"] = 0
		self.__PT_Data["1BMARKER_prio"] = 0
		self.__PT_Data["PlayStation_ID"] = ""
		self.__PT_Data["PlayStation"] = ""
		self.__PT_Data["PlayStation_prio"] = ""
		self.__PT_Data["PlayStation_deg"] = ""
		self.__PT_Data["PlayStation_LR"] = ""
		self.__PT_Data["world"] = ""
		self.__PT_Data["line"] = ""
		self.__PT_Data["PRIO_OMEGA1"] = 0
		self.__PT_Data["PRIO_OMEGA2"] = 0
		self.world_cnt = 0
		self.line_cnt = 0
		self.is_start = False
		self.state_delta = 0
		self.state_sigma = 0
		self.state_omega = 0
		self.fg_sigma_once = False
		self.playstation_cnt = 0
		self.tmp_cnt = 0
		self.my_marker = ""
		return
	@jit
	def update_df(self, PT_array):
		self.__PT_Data.update(PT_array)
	@jit
	def start(self,PT_array:pandas.DataFrame):
		self.__PT_Data = PT_array.copy()
		self.__PT_Data["Dynamis"] = 0
		self.__PT_Data["1BMARKER"] = 0
		self.__PT_Data["1BMARKER_prio"] = 0
		self.__PT_Data["PlayStation_ID"] = ""
		self.__PT_Data["PlayStation"] = ""
		self.__PT_Data["PlayStation_prio"] = ""
		self.__PT_Data["PlayStation_deg"] = ""
		self.__PT_Data["PlayStation_LR"] = ""
		self.__PT_Data["PlayStation_tower"] = 0
		self.__PT_Data["world"] = ""
		self.__PT_Data["line"] = ""
		self.__PT_Data["PRIO_OMEGA1"] = 0
		self.__PT_Data["PRIO_OMEGA2"] = 0
		self.tmp_cnt = 0
		self.is_start = True
		self.my_marker = ""
		return
	@jit
	def init(self):
		self.__PT_Data.to_csv(r"E:\works\80.repos\splatool\dumps\top_p5_dump" + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime(r"%Y%m%d%H%M%S%f") + ".csv" )
		self.__PT_Data = pandas.DataFrame()
		self.__PT_Data["Dynamis"] = 0
		self.__PT_Data["1BMARKER"] = 0
		self.__PT_Data["1BMARKER_prio"] = 0
		self.__PT_Data["PlayStation_ID"] = ""
		self.__PT_Data["PlayStation"] = ""
		self.__PT_Data["PlayStation_prio"] = ""
		self.__PT_Data["PlayStation_deg"] = ""
		self.__PT_Data["PlayStation_LR"] = ""
		self.__PT_Data["PlayStation_tower"] = 0
		self.__PT_Data["world"] = ""
		self.__PT_Data["line"] = ""
		self.__PT_Data["PRIO_OMEGA1"] = 0
		self.__PT_Data["PRIO_OMEGA2"] = 0
		self.world_cnt = 0
		self.line_cnt = 0
		self.is_start = False
		self.state_delta = 0
		self.state_sigma = 0
		self.state_omega = 0
		self.fg_sigma_once = False
		self.playstation_cnt = 0
		self.tmp_cnt = 0
		self.my_marker = ""
		return
	@jit
	def interval_init(self):
		self.__PT_Data["1BMARKER"] = 0
		self.__PT_Data["1BMARKER_prio"] = 0
		self.__PT_Data["PlayStation_ID"] = ""
		self.__PT_Data["PlayStation"] = ""
		self.__PT_Data["PlayStation_prio"] = ""
		self.__PT_Data["PlayStation_deg"] = 0
		self.__PT_Data["PlayStation_LR"] = ""
		self.__PT_Data["PlayStation_tower"] = 0
		self.__PT_Data["world"] = ""
		self.__PT_Data["line"] = ""
		self.__PT_Data["PRIO_OMEGA1"] = 0
		self.__PT_Data["PRIO_OMEGA2"] = 0
		self.__PT_Data = self.__PT_Data.sort_values("PRIO")
		self.__PT_Data = self.__PT_Data.reset_index(drop=True)
		self.world_cnt = 0
		self.line_cnt = 0
		self.state_delta = 0
		self.state_sigma = 0
		self.state_omega = 0
		self.tmp_cnt = 0
		self.fg_sigma_once = False
		self.my_marker = ""
		return
	@jit
	def log_chk(self,message_dict):
		linedata = message_dict["line"]
		nowtime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime(r"%Y%m%d%H%M%S%f")
		# デュナミスバフ管理 #オメガ時はロジック内で加算処理を行うのでnop
		if((splatool_util.log_chk_get_buff_26(message_dict,"D74")) and (self.state_omega == 0)):
			self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[7],"Dynamis"] += 1

		if(splatool_util.log_chk_00(message_dict,"この力の増幅は、リミッターカットでは説明不能……。 ヒトの不可解な強さと関係が……？")):
			self.interval_init()
			self.state_sigma = 1

		if(splatool_util.log_chk_00(message_dict,"仮説……ヒトのリミットブレイク現象が、 生命に備わった機能でないのだとしたら……。")):
			self.interval_init()
			self.state_omega = 1 

		# logic分岐
		if (self.state_delta >= 1):
			self.delta_logic(message_dict)

		if (self.state_sigma >= 1):
			self.sigma_logic(message_dict)

		if (self.state_omega >= 1):
			self.omega_logic(message_dict)

		return
	@jit
	def delta_logic(self,message_dict):
		linedata = message_dict["line"]

		self.state_delta = 0
		return
	@jit
	def sigma_logic(self,message_dict):
		global SIGMA_OMEGA_M_POS_MARKERS
		linedata = message_dict["line"]
		nowtime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime(r"%Y%m%d%H%M%S%f")
		if (self.state_sigma == 1): # Display PRIORITY
			# 初期デバフ取得
			if(splatool_util.log_chk_get_buff_26(message_dict,"D72")):
				self.world_cnt += 1
				self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[7],"world"] = "Near"
			if(splatool_util.log_chk_get_buff_26(message_dict,"D73")):
				self.world_cnt += 1
				self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[7],"world"] = "Far"
			if(splatool_util.log_chk_get_buff_26(message_dict,"D63")):
				self.world_cnt += 1
				self.__PT_Data.loc[:,"line"] = "Middle"
			if(splatool_util.log_chk_get_buff_26(message_dict,"D64")):
				self.world_cnt += 1
				self.__PT_Data.loc[:,"line"] = "Far"

			# オメガMの場所確認
			if (linedata[0] == "35" and "ライトアーム" in linedata[3]):
				df:pandas.DataFrame = g.combatants_df[g.combatants_df["Name"] == linedata[3]]
				df = df.sort_values("ID")
				df = df.reset_index(drop=True)

				df1 = self.__SIGMA_OMEGA_ARM_POS.loc[(self.__SIGMA_OMEGA_ARM_POS["x"] == float(Decimal(str(df["PosX"][1])).quantize(Decimal('1'), rounding=ROUND_HALF_UP))) & \
						(self.__SIGMA_OMEGA_ARM_POS["y"] == float(Decimal(str(df["PosY"][1])).quantize(Decimal('1'), rounding=ROUND_HALF_UP)))]
				df2 = self.__SIGMA_OMEGA_ARM_POS.loc[(self.__SIGMA_OMEGA_ARM_POS["x"] == float(Decimal(str(df["PosX"][2])).quantize(Decimal('1'), rounding=ROUND_HALF_UP))) & \
						(self.__SIGMA_OMEGA_ARM_POS["y"] == float(Decimal(str(df["PosY"][2])).quantize(Decimal('1'), rounding=ROUND_HALF_UP)))]
				df = pandas.concat([df1,df2])
				df.reset_index(drop=True,inplace=True)
				df1 = self.__SIGMA_OMEGA_M_MARKER[(self.__SIGMA_OMEGA_M_MARKER["MARK1"] == df["marker"][0]) & (self.__SIGMA_OMEGA_M_MARKER["MARK2"] == df["marker"][1])]
				df2 = self.__SIGMA_OMEGA_M_MARKER[(self.__SIGMA_OMEGA_M_MARKER["MARK2"] == df["marker"][0]) & (self.__SIGMA_OMEGA_M_MARKER["MARK2"] == df["marker"][1])]
				df3 = self.__SIGMA_OMEGA_M_MARKER[(self.__SIGMA_OMEGA_M_MARKER["MARK1"] == df["marker"][1]) & (self.__SIGMA_OMEGA_M_MARKER["MARK2"] == df["marker"][0])]
				df4 = self.__SIGMA_OMEGA_M_MARKER[(self.__SIGMA_OMEGA_M_MARKER["MARK2"] == df["marker"][1]) & (self.__SIGMA_OMEGA_M_MARKER["MARK2"] == df["marker"][0])]
				
				df = pandas.concat([df1,df2,df3,df4])
				df.reset_index(drop=True,inplace=True)
				self.sigma_omegaM_marker_pos = str(df["marker"][0])

			if ("27" == linedata[0]):
				self.playstation_cnt += 1
				self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[2],"PlayStation_ID"] = linedata[6]

			if((self.world_cnt >= 2) and (self.playstation_cnt >= 8) and ("" != self.sigma_omegaM_marker_pos)):
				# playstation解析
				self.__PT_Data = self.__PT_Data.sort_values("PlayStation_ID")
				self.__PT_Data = self.__PT_Data.reset_index(drop=True)
				self.__PT_Data.loc[0,"PlayStation"] = "Circle"
				self.__PT_Data.loc[1,"PlayStation"] = "Circle"
				self.__PT_Data.loc[2,"PlayStation"] = "Triangle"
				self.__PT_Data.loc[3,"PlayStation"] = "Triangle"
				self.__PT_Data.loc[4,"PlayStation"] = "square"
				self.__PT_Data.loc[5,"PlayStation"] = "square"
				self.__PT_Data.loc[6,"PlayStation"] = "Cross"
				self.__PT_Data.loc[7,"PlayStation"] = "Cross"
				for index, row in self.__PT_Data.iterrows():
					self.__PT_Data.loc[index,"PlayStation_prio"] = PLAYSTATION_PRIO[self.__PT_Data["PlayStation"][index]]
				self.__PT_Data = self.__PT_Data.sort_values("PRIO")
				self.__PT_Data = self.__PT_Data.reset_index(drop=True)

				# 優先度表示
				pri_df = self.__PT_Data[self.__PT_Data["world"] != "Near"]
				pri_df = pri_df[pri_df["world"] != "Far"]
				pri_df = pri_df[pri_df["Dynamis"] == 1]
				pri_df = pri_df.reset_index(drop=True)
				splatool_util.chatprint("------------------------------")
				splatool_util.chatprint("SIGMA:")
				splatool_util.chatprint("# OMEGA M IS " + "\" " + self.sigma_omegaM_marker_pos + " \"")
				splatool_util.chatprint("# PRIORITY")
				disnumkey =""
				for index, row in pri_df.iterrows():
					splatool_util.chatprint(str(index + 1) + ": " + row["name"])
					#pyautogui.press(str(row["NUMKEY"]))
					disnumkey = disnumkey + str(row["NUMKEY"]).replace("num","")
					
					if (row["MINE"] == 1):
						# 今だけ TODO: 試験完了後にattackマーカーの数字を記憶する
						splatool_util.chatprint("attack is ON!!!!")
						splatool_util.ExecuteCommand("/mk attack <1>")
				splatool_util.chatprint("NUMKEY: " + disnumkey)
				self.state_sigma += 1
				return
		if (self.state_sigma == 2): #座標データから次の動きを推測
			if ("27" == linedata[0]):
				if(False == self.__PT_Data.loc[self.__PT_Data["PlayStation_ID"] == linedata[6]].empty):
					return
				self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[2],"1BMARKER"] = 1
				self.tmp_cnt += 1

				if (6 <=  self.tmp_cnt):
					# この時点の座標から左右を確認する
					g.combatants_df.to_csv("E:\\works\\1.projects\\svn\\logparser\\logparser\\combatants\\" + nowtime + "_sigma01.csv")
					sigma_omegaM_pos = self.__SIGMA_OMEGA_M_POS[self.__SIGMA_OMEGA_M_POS["marker"] == self.sigma_omegaM_marker_pos]
					sigma_omegaM_pos = sigma_omegaM_pos.reset_index(drop=True)
					sigma_omegaM_pos_x = float(sigma_omegaM_pos["x"][0])
					sigma_omegaM_pos_y = float(sigma_omegaM_pos["y"][0])

					self.__PT_Data = self.__PT_Data.sort_values("PlayStation_prio")
					self.__PT_Data = self.__PT_Data.reset_index(drop=True)
					tmp_rad = 0
					tmp_pair_1B = 0
					tmp_pair_chked = False
					prio_both = 0
					prio_one_side = 2
					for index, row in self.__PT_Data.iterrows():
						rad = \
							splatool_util.calc_2point_pos(100,100,sigma_omegaM_pos_x,sigma_omegaM_pos_y,float(row["x"]),float(row["y"]))
						
						self.__PT_Data.loc[index,"PlayStation_deg"] = rad
						
						if ( 0 == tmp_rad):
							tmp_rad = rad
						else:
							if (tmp_rad > rad):
								self.__PT_Data.loc[index - 1,"PlayStation_LR"] = "RIGHT"
								self.__PT_Data.loc[index,"PlayStation_LR"] = "LEFT"
							else:
								self.__PT_Data.loc[index - 1,"PlayStation_LR"] = "LEFT"
								self.__PT_Data.loc[index,"PlayStation_LR"] = "RIGHT"
							tmp_rad = 0

						if ( False == tmp_pair_chked):
							tmp_pair_1B = self.__PT_Data["1BMARKER"][index]
							tmp_pair_chked = True
						else:
							tmp_pair_1B += self.__PT_Data["1BMARKER"][index]
							if (tmp_pair_1B >= 2):
								self.__PT_Data.loc[index - 1,"1BMARKER_prio"] = prio_both
								self.__PT_Data.loc[index,"1BMARKER_prio"] = prio_both
								prio_both += 1
							else:
								self.__PT_Data.loc[index - 1,"1BMARKER_prio"] = prio_one_side
								self.__PT_Data.loc[index,"1BMARKER_prio"] = prio_one_side
								prio_one_side += 1
							tmp_pair_1B = 0
							tmp_pair_chked = False
						
					# 波動砲立ち位置表示
					disp_df = self.__PT_Data[self.__PT_Data["MINE"] == 1]
					disp_df = disp_df.reset_index(drop=False)
					disp_df = disp_df.iloc[0]

					markers_data = SIGMA_OMEGA_M_POS_MARKERS[self.sigma_omegaM_marker_pos]
					splatool_util.chatprint("")
					splatool_util.chatprint("# Wave Cannon Pos")
					if (int(disp_df["1BMARKER_prio"]) == 0):
						self.my_marker = markers_data[0]
					elif (int(disp_df["1BMARKER_prio"]) == 1):
						self.my_marker = markers_data[1]
					elif (int(disp_df["1BMARKER_prio"]) == 2):
						if (0 == disp_df["1BMARKER"]):
							self.my_marker = markers_data[2]
						else:
							self.my_marker = markers_data[3]
					elif (int(disp_df["1BMARKER_prio"]) == 3):
						if (0 == disp_df["1BMARKER"]):
							self.my_marker = markers_data[4]
						else:
							self.my_marker = markers_data[5]

					splatool_util.chatprint("POS: " + self.my_marker)
					#### TODO : splatoon 要求
					self.state_sigma += 1
		if (self.state_sigma == 3):
			g.combatants_df.to_csv("E:\\works\\1.projects\\svn\\logparser\\logparser\\combatants\\" + nowtime + "_sigma02.csv")
			disp_df = self.__PT_Data[self.__PT_Data["MINE"] == 1]
			disp_df = disp_df.reset_index(drop=False)
			disp_df = disp_df.iloc[0]
			splatool_util.chatprint("------------------------------")
			splatool_util.chatprint("# 塔:")
			if ( "Middle" == disp_df["line"]):
				if ( "Circle" == disp_df["PlayStation"]):
					if ( "LEFT" == disp_df["PlayStation_LR"]):
						splatool_util.chatprint("左〇")
						splatool_util.chatprint("       ミドル        ")
						splatool_util.chatprint("     ×    〇        ")
						splatool_util.chatprint("                        ")
						splatool_util.chatprint(" ×            ×    ")
						splatool_util.chatprint("     ×    ×       ")
						self.__PT_Data["PlayStation_tower"] = 5

					if ( "RIGHT" == disp_df["PlayStation_LR"]):
						splatool_util.chatprint("右〇")
						splatool_util.chatprint("       ミドル        ")
						splatool_util.chatprint("     ×    ×        ")
						splatool_util.chatprint("                        ")
						splatool_util.chatprint(" ×            〇    ")
						splatool_util.chatprint("     ×    ×       ")
						self.__PT_Data["PlayStation_tower"] = 4

				if ( "Cross" == disp_df["PlayStation"]):
					if ( "LEFT" == disp_df["PlayStation_LR"]):
						splatool_util.chatprint("左×")
						splatool_util.chatprint("       ミドル        ")
						splatool_util.chatprint("     〇    ×        ")
						splatool_util.chatprint("                        ")
						splatool_util.chatprint(" ×            ×    ")
						splatool_util.chatprint("     ×    ×       ")
						self.__PT_Data["PlayStation_tower"] = 0

					if ( "RIGHT" == disp_df["PlayStation_LR"]):
						splatool_util.chatprint("右×")
						splatool_util.chatprint("       ミドル        ")
						splatool_util.chatprint("     ×    ×        ")
						splatool_util.chatprint("                        ")
						splatool_util.chatprint(" 〇            ×    ")
						splatool_util.chatprint("     ×    ×       ")
						self.__PT_Data["PlayStation_tower"] = 1

				if ( "Triangle" == disp_df["PlayStation"]):
					if ( "LEFT" == disp_df["PlayStation_LR"]):
						splatool_util.chatprint("左△")
						splatool_util.chatprint("       ミドル        ")
						splatool_util.chatprint("     ×    ×        ")
						splatool_util.chatprint("                        ")
						splatool_util.chatprint(" 〇            ×    ")
						splatool_util.chatprint("     ×    ×       ")
						self.__PT_Data["PlayStation_tower"] = 1

					if ( "RIGHT" == disp_df["PlayStation_LR"]):
						splatool_util.chatprint("右△")
						splatool_util.chatprint("       ミドル        ")
						splatool_util.chatprint("     ×    ×        ")
						splatool_util.chatprint("                        ")
						splatool_util.chatprint(" ×           ×    ")
						splatool_util.chatprint("     ×    〇       ")
						self.__PT_Data["PlayStation_tower"] = 3

				if ( "square" == disp_df["PlayStation"]):
					if ( "LEFT" == disp_df["PlayStation_LR"]):
						splatool_util.chatprint("左□")
						splatool_util.chatprint("       ミドル        ")
						splatool_util.chatprint("     ×    ×        ")
						splatool_util.chatprint("                        ")
						splatool_util.chatprint(" ×           ×    ")
						splatool_util.chatprint("     〇    ×       ")
						self.__PT_Data["PlayStation_tower"] = 2

					if ( "RIGHT" == disp_df["PlayStation_LR"]):
						splatool_util.chatprint("右□")
						splatool_util.chatprint("       ミドル        ")
						splatool_util.chatprint("     ×    ×        ")
						splatool_util.chatprint("                        ")
						splatool_util.chatprint(" ×           〇    ")
						splatool_util.chatprint("     ×    ×       ")
						self.__PT_Data["PlayStation_tower"] = 4

			if ( "Far" == disp_df["line"]):
				if ( "Circle" == disp_df["PlayStation"]):
					if ( "LEFT" == disp_df["PlayStation_LR"]):
						splatool_util.chatprint("左〇")
						splatool_util.chatprint("         ファー  ")
						splatool_util.chatprint("           〇")
						splatool_util.chatprint("")
						splatool_util.chatprint("    ×           ×")
						splatool_util.chatprint("       ×       ×")
						self.__PT_Data["PlayStation_tower"] = 4

					if ( "RIGHT" == disp_df["PlayStation_LR"]):
						splatool_util.chatprint("右〇")
						splatool_util.chatprint("         ファー  ")
						splatool_util.chatprint("           ×")
						splatool_util.chatprint("")
						splatool_util.chatprint("    ×           ×")
						splatool_util.chatprint("       ×       〇")
						self.__PT_Data["PlayStation_tower"] = 2

				if ( "Cross" == disp_df["PlayStation"]):
					if ( "LEFT" == disp_df["PlayStation_LR"]):
						splatool_util.chatprint("左×")
						splatool_util.chatprint("         ファー  ")
						splatool_util.chatprint("           〇")
						splatool_util.chatprint("")
						splatool_util.chatprint("    ×           ×")
						splatool_util.chatprint("       ×       ×")
						self.__PT_Data["PlayStation_tower"] = 4

					if ( "RIGHT" == disp_df["PlayStation_LR"]):
						splatool_util.chatprint("右×")
						splatool_util.chatprint("         ファー  ")
						splatool_util.chatprint("           ×")
						splatool_util.chatprint("")
						splatool_util.chatprint("    ×           ×")
						splatool_util.chatprint("       〇       ×")
						self.__PT_Data["PlayStation_tower"] = 1

				if ( "Triangle" == disp_df["PlayStation"]):
					if ( "LEFT" == disp_df["PlayStation_LR"]):
						splatool_util.chatprint("左△")
						splatool_util.chatprint("         ファー  ")
						splatool_util.chatprint("           ×")
						splatool_util.chatprint("")
						splatool_util.chatprint("    〇           ×")
						splatool_util.chatprint("       ×       ×")
						self.__PT_Data["PlayStation_tower"] = 0

					if ( "RIGHT" == disp_df["PlayStation_LR"]):
						splatool_util.chatprint("右△")
						splatool_util.chatprint("         ファー  ")
						splatool_util.chatprint("           ×")
						splatool_util.chatprint("")
						splatool_util.chatprint("    ×           ×")
						splatool_util.chatprint("       ×      〇")
						self.__PT_Data["PlayStation_tower"] = 2

				if ( "square" == disp_df["PlayStation"]):
					if ( "LEFT" == disp_df["PlayStation_LR"]):
						splatool_util.chatprint("左□")
						splatool_util.chatprint("         ファー  ")
						splatool_util.chatprint("           ×")
						splatool_util.chatprint("")
						splatool_util.chatprint("    ×           ×")
						splatool_util.chatprint("       〇      ×")
						self.__PT_Data["PlayStation_tower"] = 1

					if ( "RIGHT" == disp_df["PlayStation_LR"]):
						splatool_util.chatprint("右□")
						splatool_util.chatprint("         ファー  ")
						splatool_util.chatprint("           ×")
						splatool_util.chatprint("")
						splatool_util.chatprint("    ×           〇")
						splatool_util.chatprint("       ×      ×")
						self.__PT_Data["PlayStation_tower"] = 3

			splatool_util.chatprint("------------------------------")
			self.state_sigma += 1
			return
		#### 塔場所確認
		if (self.state_sigma == 4):
			# 塔がでてくるまで待機
			tower_df1 = g.combatants_df[(g.combatants_df["BNpcID"] == 2013245)]
			tower_df2 = g.combatants_df[(g.combatants_df["BNpcID"] == 2013246)]
			tower_df = pandas.concat([tower_df1,tower_df2])
			if (True == tower_df.empty):
				return
			tower_df = tower_df.sort_values("ID")

			self.state_sigma += 1
		#### ハロワ位置表示
		if (self.state_sigma == 5):
			self.interval_init()
			return
		return
	@jit
	def omega_logic(self,message_dict):
		linedata = message_dict["line"]

		if(1 == self.state_omega):
			if(splatool_util.log_chk_get_buff_26(message_dict,"D72")):
				self.world_cnt += 1
				self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[7],"world"] = "Near"
			if(splatool_util.log_chk_get_buff_26(message_dict,"D73")):
				self.world_cnt += 1
				self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[7],"world"] = "Far"
			if(splatool_util.log_chk_get_buff_26(message_dict,"BBC")):
				self.line_cnt += 1
				self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[7],"line"] = 1
			if(splatool_util.log_chk_get_buff_26(message_dict,"BBD")):
				self.line_cnt += 1
				self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[7],"line"] = 2

			if(4 <= self.world_cnt and 4<= self.line_cnt):
				# 検知時の優先度判定
				## 検知者判定
				dete_cnt = 11
				# デュナミス2 ハロワ2持ち → 検知確定
				pri_df = self.__PT_Data[self.__PT_Data["Dynamis"] == 2]
				pri_df = pri_df[pri_df["line"] == 2]
				pri_df = pri_df.reset_index(drop=True)
				for index, row in pri_df.iterrows():
					if (dete_cnt >= 13):
						break
					self.__PT_Data.loc[self.__PT_Data["ID"] == row["ID"],"PRIO_OMEGA1"] = dete_cnt
					dete_cnt += 1

				# デュナミス2のみ持ち → 検知確定
				pri_df = self.__PT_Data[self.__PT_Data["Dynamis"] == 2]
				pri_df = pri_df[pri_df["PRIO_OMEGA1"] == 0]
				pri_df = pri_df[pri_df["line"] != 1]
				pri_df = pri_df.reset_index(drop=True)
				for index, row in pri_df.iterrows():
					if (dete_cnt >= 13):
						break
					self.__PT_Data.loc[self.__PT_Data["ID"] == row["ID"],"PRIO_OMEGA1"] = dete_cnt
					dete_cnt += 1

				# 残りの人でハロワファーストでない人に割り振る
				pri_df = self.__PT_Data[self.__PT_Data["PRIO_OMEGA1"] == 0]
				pri_df = pri_df[pri_df["line"] != 1]
				pri_df = pri_df.reset_index(drop=True)
				for index, row in pri_df.iterrows():
					self.__PT_Data.loc[self.__PT_Data["ID"] == row["ID"],"PRIO_OMEGA1"] = (index + 1)

				# 検知でつくデュナミス付与
				pri_df = self.__PT_Data[self.__PT_Data["PRIO_OMEGA1"] < 9]
				for index, row in pri_df.iterrows():
					self.__PT_Data.loc[self.__PT_Data["ID"] == row["ID"],"Dynamis"] += 1

				# ブラスター時の優先度判定
				## ブラスター対象者判定
				pri_df = self.__PT_Data[self.__PT_Data["Dynamis"] == 3]
				pri_df = pri_df.reset_index(drop=True)
				for index, row in pri_df.iterrows():
					self.__PT_Data.loc[self.__PT_Data["ID"] == row["ID"],"PRIO_OMEGA2"] = (index + 11)

				# 残りの人でハロワではない人を割り振る
				pri_df = self.__PT_Data[self.__PT_Data["Dynamis"] == 2]
				pri_df = pri_df[pri_df["line"] != 2]
				pri_df = pri_df.reset_index(drop=True)
				for index, row in pri_df.iterrows():
					self.__PT_Data.loc[self.__PT_Data["ID"] == row["ID"],"PRIO_OMEGA2"] = (index + 1)
				
				splatool_util.chatprint("------------------------------")
				splatool_util.chatprint("OMEGA:")
				splatool_util.chatprint("# PRIORITY WHEN DETECT TIME")
				pri_df = self.__PT_Data[self.__PT_Data["PRIO_OMEGA1"] != 0]
				pri_df = pri_df.reset_index(drop=True)
				disp_df = pri_df[pri_df["PRIO_OMEGA1"] > 9]
				disnumkey = ""
				disp_df = disp_df.reset_index(drop=True)
				splatool_util.chatprint("## DETECTER BIND")
				for index, row in disp_df.iterrows():
					splatool_util.chatprint(str(index + 1) + ": " + row["name"])
					disnumkey = disnumkey + str(row["NUMKEY"])
					splatool_util.ExecuteCommand("/mk bind <" + str(row["NUMKEY"]) + ">")
					time.sleep(random.uniform(0.8,1.5))
				splatool_util.chatprint("BIND NUMKEY: " + str(disnumkey))
				splatool_util.chatprint("")

				disp_df = pri_df[pri_df["PRIO_OMEGA1"] < 9]
				disp_df = disp_df.reset_index(drop=True)
				disnumkey = ""
				splatool_util.chatprint("## ATTACK PRIORITY")
				for index, row in disp_df.iterrows():
					splatool_util.chatprint(str(index + 1) + ": " + row["name"])
					disnumkey = disnumkey + str(row["NUMKEY"])
					splatool_util.ExecuteCommand("/mk attack <" + str(row["NUMKEY"]) + ">")
					time.sleep(random.uniform(0.8,1.5))
				splatool_util.chatprint("ATTACK NUMKEY: " + str(disnumkey))
				splatool_util.chatprint("------------------------------")
				self.state_omega += 1
			return
		if(2 == self.state_omega):
			if((linedata[0] != "20") or ("検知式波動砲" not in linedata[5])):
				return
			
			# 右B検知 左D安置
			if((linedata[0] == "20") and ("7B96" == linedata[4])):
				a = 1 # TODO

			# 左D検知 右B安置
			if((linedata[0] == "20") and ("7B97" == linedata[4])):
				a = 1 # TODO

			self.state_omega += 1
			return
		if(3 == self.state_omega):
			if(((linedata[0] != "30") or ("D72" != linedata[2])) and ((linedata[0] != "30") or ("D73" != linedata[2]))):
				return

			splatool_util.chatprint("------------------------------")
			splatool_util.chatprint("# PRIORITY WHEN BLASTER TIME")
			pri_df = self.__PT_Data[self.__PT_Data["PRIO_OMEGA2"] != 0]
			pri_df = pri_df.reset_index(drop=True)
			disp_df = pri_df[pri_df["PRIO_OMEGA2"] > 9]
			disnumkey = ""
			disp_df = disp_df.reset_index(drop=True)
			splatool_util.chatprint("## DETECTER BIND")
			for index, row in disp_df.iterrows():
				splatool_util.chatprint(str(index + 1) + ": " + row["name"])
				disnumkey = disnumkey + str(row["NUMKEY"])
				#splatool_util.ExecuteCommand("/mk bind <" + str(row["NUMKEY"]) + ">")
			splatool_util.chatprint("BIND NUMKEY: " + str(disnumkey))
			splatool_util.chatprint("")

			disp_df = pri_df[pri_df["PRIO_OMEGA2"] < 9]
			disp_df = disp_df.reset_index(drop=True)
			disnumkey = ""
			splatool_util.chatprint("## ATTACK PRIORITY")
			for index, row in disp_df.iterrows():
				splatool_util.chatprint(str(index + 1) + ": " + row["name"])
				disnumkey = disnumkey + str(row["NUMKEY"])
				splatool_util.ExecuteCommand("/mk attack <" + str(row["NUMKEY"]) + ">")
				time.sleep(random.uniform(0.8,1.5))
			splatool_util.chatprint("ATTACK NUMKEY: " + str(disnumkey))
			splatool_util.chatprint("------------------------------")

			self.state_omega += 1
			return
		if(4 == self.state_omega):
			if((linedata[0] != "20") or ("7E76"  != linedata[4])):
				return
			# TODO: splatoon

			self.interval_init()
			self.state_delta = 0
			return
		return
