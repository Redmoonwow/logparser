#import splatool
import pandas
import datetime
import splatool_util
import math



# シグマ オメガMの出現場所
#03|2023-03-01T23:41:01.6360000+09:00|4001249A|オメガ|00|5A|0000|00||7695|15724|10380000|10380000|10000|10000|||100.00|80.00|0.00|0.00|2bbe6e7b71706db5				A
#03|2023-03-05T21:26:25.5610000+09:00|40021BCC|オメガ|00|5A|0000|00||7695|15724|10380000|10380000|10000|10000|||114.14|85.86|0.00|0.79|64db1a9c1e19bf45				2
#03|2023-03-01T23:55:45.1760000+09:00|40013399|オメガ|00|5A|0000|00||7695|15724|10380000|10380000|10000|10000|||120.00|100.00|0.00|-1.57|a2e5d3c00f745f4b			B
#03|2023-03-01T22:23:50.2690000+09:00|4000DF85|オメガ|00|5A|0000|00||7695|15724|10380000|10380000|10000|10000|||114.14|114.14|0.00|-2.36|ecf554cfc480bcb9			2
#03|2023-03-02T23:00:20.2130000+09:00|4000A667|オメガ|00|5A|0000|00||7695|15724|10380000|10380000|10000|10000|||100.00|120.00|0.00|3.14|cf5224a3a2a45e14			C
#03|2023-03-01T23:54:15.6880000+09:00|40013255|オメガ|00|5A|0000|00||7695|15724|10380000|10380000|10000|10000|||85.86|114.14|0.00|2.36|4a5871419a83fd85				3
#03|2023-03-05T22:18:53.6300000+09:00|40015DB2|オメガ|00|5A|0000|00||7695|15724|10380000|10380000|10000|10000|||80.00|100.00|0.00|1.57|c18c9d6823a0132d				D
#03|2023-03-05T21:26:25.5610000+09:00|40021BCC|オメガ|00|5A|0000|00||7695|15724|10380000|10380000|10000|10000|||85.86|85.86|0.00|0.79|64db1a9c1e19bf45				4

SIGMA_OMEGA_M_POS = {
	"marker":	["A","1","B","2","C","3","D","4"],
	"x":		[100.00,114.14,120.00,114.14,100.00,85.86,80.00,85.86],
	"y":		[80.00,85.86,100.00,114.14,120.00,114.14,100.00,85.86]
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
	__PT_Data = pandas.DataFrame()
	__SIGMA_OMEGA_M_POS = pandas.DataFrame()
	world_cnt = 0
	line_cnt = 0
	playstation_cnt = 0
	tmp_cnt = 0
	is_start = False
	state_delta = 0
	state_sigma = 0
	state_omega = 0

	sigma_omegaM_marker_pos = ""
	fg_sigma_once = False
	my_marker = ""

	def __init__(self):
		self.__PT_Data = pandas.DataFrame()
		self.__SIGMA_OMEGA_M_POS = pandas.DataFrame(SIGMA_OMEGA_M_POS)
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
	
	def update_df(self, PT_array):
		self.__PT_Data.update(PT_array)

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
		self.__PT_Data["world"] = ""
		self.__PT_Data["line"] = ""
		self.tmp_cnt = 0
		self.is_start = True
		self.my_marker = ""
		return
	
	def init(self):
		self.__PT_Data.to_csv(r"E:\works\80.repos\splatool\dumps\top_p5_dump" + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y%m%d%H%M%S") + ".csv" )
		self.__PT_Data = pandas.DataFrame()
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
	
	def interval_init(self):
		self.__PT_Data["1BMARKER"] = 0
		self.__PT_Data["1BMARKER_prio"] = 0
		self.__PT_Data["PlayStation_ID"] = ""
		self.__PT_Data["PlayStation"] = ""
		self.__PT_Data["PlayStation_prio"] = ""
		self.__PT_Data["PlayStation_deg"] = 0
		self.__PT_Data["PlayStation_LR"] = ""
		self.__PT_Data["world"] = ""
		self.__PT_Data["line"] = ""
		self.world_cnt = 0
		self.line_cnt = 0
		self.state_delta = 0
		self.state_sigma = 0
		self.state_omega = 0
		self.tmp_cnt = 0
		self.fg_sigma_once = False
		self.my_marker = ""
		return
	
	def log_chk(self,message_dict):
		global SIGMA_OMEGA_M_POS_MARKERS
		#print(str(message_dict["rawLine"]).replace("\n",""))
		linedata = message_dict["line"]
		# デュナミスバフ管理
		if(splatool_util.log_chk_get_buff_26(message_dict,"D74")):
			self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[7],"Dynamis"] += 1

		if(splatool_util.log_chk_00(message_dict,"この力の増幅は、リミッターカットでは説明不能……。 ヒトの不可解な強さと関係が……？")):
			self.interval_init()
			self.state_sigma = 1

		# シグマ中常に確認
		if (self.state_sigma >= 1): 
			# オメガMの場所確認
			if(splatool_util.log_chk_combatant_entity_03(message_dict,"","15724")):
				omegaM_pos_df = self.__SIGMA_OMEGA_M_POS.loc[(self.__SIGMA_OMEGA_M_POS["x"] == float(linedata[17])) & (self.__SIGMA_OMEGA_M_POS["y"] == float(linedata[18]))]
				omegaM_pos_df.reset_index(drop=True,inplace=True)
				self.sigma_omegaM_marker_pos = str(omegaM_pos_df["marker"][0])

		if (self.state_sigma == 1): # Display PRIORITY
			
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

			if ("27" == linedata[0]):
				self.playstation_cnt += 1
				self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[2],"PlayStation_ID"] = linedata[6]

			if(self.world_cnt >= 2 and self.playstation_cnt >= 8):
				# playstation解析
				self.__PT_Data = self.__PT_Data.sort_values("PlayStation_ID")
				self.__PT_Data = self.__PT_Data.reset_index(drop=True)
				self.__PT_Data.loc[0,"PlayStation"] = "square"
				self.__PT_Data.loc[1,"PlayStation"] = "square"
				self.__PT_Data.loc[2,"PlayStation"] = "Cross"
				self.__PT_Data.loc[3,"PlayStation"] = "Cross"
				self.__PT_Data.loc[4,"PlayStation"] = "Circle"
				self.__PT_Data.loc[5,"PlayStation"] = "Circle"
				self.__PT_Data.loc[6,"PlayStation"] = "Triangle"
				self.__PT_Data.loc[7,"PlayStation"] = "Triangle"
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
				splatool_util.chatprint("# OMEGA M IS " + self.sigma_omegaM_marker_pos)
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
		if (self.state_sigma == 2): #座標データから次の動きを推測
			if ("27" == linedata[0]):
				self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[2],"1BMARKER"] = 1
				self.tmp_cnt += 1

				if (7 <=  self.tmp_cnt):
					# この時点の座標から左右を確認する
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
					match int(disp_df["1BMARKER_prio"]):
						case 0:
							self.my_marker = markers_data[0]
						case 1:
							self.my_marker = markers_data[1]
						case 2:
							if (0 == disp_df["1BMARKER"]):
								self.my_marker = markers_data[2]
							else:
								self.my_marker = markers_data[3]
						case 3:
							if (0 == disp_df["1BMARKER"]):
								self.my_marker = markers_data[4]
							else:
								self.my_marker = markers_data[5]

					splatool_util.chatprint("POS: " + self.my_marker)
					#### TODO : splatoon 要求
					self.state_sigma += 1
			if (self.state_sigma == 3):
				# 塔場所解析
				a = 1
			
		return
	