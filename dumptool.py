import splatool_util

def damy_main():
	P5_str = False
	once = False
	log_p = open(r"E:\\works\\98.tmp\\Network_26800_20230301.2023.03.02.log",encoding = "utf-8")
	for log_rawdata in log_p:
		log_array = log_rawdata.split("|")
		log_dict = { "rawLine":log_rawdata,"line":log_array }
		linedata = log_dict["line"]
		
		if (	(249 <= int(linedata[0]))	and \
				(260 > int(linedata[0]))	):
			print(log_dict["rawLine"],end="")
			
		if ("00" == linedata[0]):
			chatID = linedata[2]
			chatauther = linedata[3]
			chatdata = linedata[4]
			if ("Hojoring" in chatdata):
				continue
			if ("Sonar" in chatauther):
				continue
			if ("0044" not in chatID):
				continue
			if(splatool_util.log_chk_00(log_dict,"この力の増幅は、リミッターカットでは説明不能……。 ヒトの不可解な強さと関係が……？")):
				P5_str = True
				print("")
				continue
			if(splatool_util.log_chk_00(log_dict,"アナタはアルファであり、ワタシはオメガである。 これは最初であり、最後の検証……記録……開始……。")):
				P5_str = False
				once = False
			if(splatool_util.log_chk_00(log_dict,"仮説……ヒトのリミットブレイク現象が、 生命に備わった機能でないのだとしたら……。")):
				P5_str = False
				once = False
			if(splatool_util.log_chk_get_buff_26(log_dict,"9E6") and P5_str == True):
				P5_str = False
				once = False

		if (False == P5_str):
			continue
		"""
		if (linedata[0] == "00" and "オメガ" in linedata[3]):
			print(log_dict["rawLine"],end="")

		if (linedata[0] == "21" and "オメガ" in linedata[3]):
			print(log_dict["rawLine"],end="")
		if(splatool_util.log_chk_get_buff_26(log_dict,"D63") and False == once):
			print(log_dict["rawLine"],end="")
			once = True
		if(splatool_util.log_chk_get_buff_26(log_dict,"D64") and False == once):
			print(log_dict["rawLine"],end="")
			once = True
			"""
		

if __name__ == "__main__":
	damy_main()
	