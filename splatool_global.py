import pandas
import numpy

PT_array = pandas.DataFrame(numpy.zeros((8,10)),columns=["name","ID","JOB","x","y","z","PRIO","MINE","HEADMARKER","NUMKEY"])
MY_PC = pandas.DataFrame(numpy.zeros((1,2)),columns=["name","ID"])
combatants_df = pandas.DataFrame()
ZoneID = 462
fg_combat = 0