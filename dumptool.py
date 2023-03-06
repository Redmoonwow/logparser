import splatool_util

def damy_main():
	log_p = open(r"E:\\works\\98.tmp\\Network_26800_20230305_hane.log",encoding = "utf-8")
	for log_rawdata in log_p:
		log_array = log_rawdata.split("|")
		log_dict = { "rawLine":log_rawdata,"line":log_array }
		linedata = log_dict["line"]
		if (	(249 <= int(linedata[0]))	and \
				(260 > int(linedata[0]))	):
			continue
		
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
			print(log_dict["rawLine"],end="")
		if (splatool_util.log_chk_combatant_entity_03(log_dict,"","15724")):
			print("------------------------03 found!!------------------------")
			print(log_dict["rawLine"])

if __name__ == "__main__":
	#main()
	damy_main()
	