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

	def __init__(self):
		self.__PT_Data = pandas.DataFrame()
		self.__SIGMA_OMEGA_M_POS = pandas.DataFrame(SIGMA_OMEGA_M_POS)
		self.__PT_Data["Dynamis"] = 0
		self.__PT_Data["1BMARKER"] = 0
		self.__PT_Data["PlayStation_ID"] = ""
		self.__PT_Data["PlayStation"] = ""
		self.__PT_Data["PlayStation_deg"] = ""
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
		tmp_cnt = 0
		return
	
	def update_df(self, PT_array):
		self.__PT_Data.update(PT_array)

	def start(self,PT_array:pandas.DataFrame):
		self.__PT_Data = PT_array.copy()
		self.__PT_Data["Dynamis"] = 0
		self.__PT_Data["1BMARKER"] = 0
		self.__PT_Data["PlayStation_ID"] = ""
		self.__PT_Data["PlayStation"] = ""
		self.__PT_Data["PlayStation_deg"] = ""
		self.__PT_Data["world"] = ""
		self.__PT_Data["line"] = ""
		tmp_cnt = 0
		self.is_start = True
		return
	
	def init(self):
		self.__PT_Data.to_csv(r"E:\works\80.repos\splatool\dumps\top_p5_dump" + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y%m%d%H%M%S") + ".csv" )
		self.__PT_Data = pandas.DataFrame()
		self.__PT_Data["Dynamis"] = 0
		self.__PT_Data["1BMARKER"] = 0
		self.__PT_Data["PlayStation_ID"] = ""
		self.__PT_Data["PlayStation"] = ""
		self.__PT_Data["PlayStation_deg"] = ""
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
		tmp_cnt = 0
		return
	
	def interval_init(self):
		self.__PT_Data["1BMARKER"] = 0
		self.__PT_Data["PlayStation_ID"] = ""
		self.__PT_Data["PlayStation"] = ""
		self.__PT_Data["PlayStation_deg"] = ""
		self.__PT_Data["world"] = ""
		self.__PT_Data["line"] = ""
		self.world_cnt = 0
		self.line_cnt = 0
		self.state_delta = 0
		self.state_sigma = 0
		self.state_omega = 0
		tmp_cnt = 0
		self.fg_sigma_once = False
		return
	
	def log_chk(self,message_dict):
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
			if ("27" == linedata[0]):
				self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[2],"1BMARKER"] = 1

			if(splatool_util.log_chk_get_buff_26(message_dict,"D72")):
				self.world_cnt += 1
				self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[7],"world"] = "Near"
			if(splatool_util.log_chk_get_buff_26(message_dict,"D73")):
				self.world_cnt += 1
				self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[7],"world"] = "Far"

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
				splatool_util.chatprint("------------------------------")
				self.state_sigma += 1
		if (self.state_sigma == 2): #座標データから次の動きを推測
			if ("27" == linedata[0]):
				self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[2],"1BMARKER"] = 1
				self.tmp_cnt += 1

				if (6 <=  self.tmp_cnt):
					# この時点の座標から左右を確認する
					sigma_omegaM_pos = self.__SIGMA_OMEGA_M_POS[self.__SIGMA_OMEGA_M_POS["marker"] == self.sigma_omegaM_marker_pos]
					sigma_omegaM_pos = sigma_omegaM_pos.reset_index(drop=True)
					sigma_omegaM_pos_x = float(sigma_omegaM_pos["x"][0])
					sigma_omegaM_pos_y = float(sigma_omegaM_pos["y"][0])
					for index, row in self.__PT_Data.iterrows():
						self.__PT_Data.loc[index,"PlayStation_deg"] = \
							splatool_util.calc_2point_pos(100,100,sigma_omegaM_pos_x,sigma_omegaM_pos_y,float(row["x"]),float(row["y"]))

					self.state_sigma += 1

			# dump 塔の出現パターン
		return
	
"""
27|2023-03-01T22:43:11.1030000+09:00|1028540A|Mosin Nagant|0000|0000|0158|0000|0000|0000|676f8fdcb7530cd6
27|2023-03-01T22:43:11.1030000+09:00|102F254D|Natsuru Yukine|0000|0000|0158|0000|0000|0000|90860d4ddf2f2693
27|2023-03-01T22:43:11.1030000+09:00|10300FB1|Zera Gloria|0000|0000|0158|0000|0000|0000|25d39c51bd6ac639
27|2023-03-01T22:43:11.1030000+09:00|102ED585|Ds Oshige|0000|0000|0158|0000|0000|0000|e8fe9da0f325464c
27|2023-03-01T22:43:11.1030000+09:00|102D563F|Morusun Shiga|0000|0000|0158|0000|0000|0000|370d9dba2f995f1e
27|2023-03-01T22:43:11.1030000+09:00|1028B6BB|Sawa'i Seven|0000|0000|0158|0000|0000|0000|ad206ade63bdf549
"""