import mysql.connector
from sklearn.ensemble import IsolationForest
import numpy as np
import time
import matplotlib.pyplot as plt
import sys
import datetime
import logging
import pickle
import vader

def pull_data(username, passwd):
	db = mysql.connector.connect(
	  host="cidco.ca",
	  user=username,
	  password=passwd,
	  database="ais"
	)

	cursor = db.cursor()

	cursor.execute("SELECT * FROM ais.clean_data")
	
	return cursor.fetchall()


def new_data(newNbPoints, oldNbPoints):
	print("new_data :", newNbPoints - oldNbPoints)
	
	if newNbPoints > oldNbPoints:
		return True
	else:
		return False


################MAIN############

if len(sys.argv) != 5:
	sys.stderr.write("Usage: padme.py user password modelFilename nb-of-rows-model-trained-on\n")
	sys.stderr.write("the nb-of-rows-model-trained-on can be found in the training-model.log file\n")
	sys.exit(1)

username = sys.argv[1]
passwd = sys.argv[2]
modelFilename = sys.argv[3]
nbRowsModelTrained = int(sys.argv[4])

dbData = pull_data(username, passwd)

nbPoints = len(dbData)

model = pickle.load(open(modelFilename,"rb"))

logging.basicConfig(filename="model-run_{}.log".format(datetime.date.today()),
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info("anomaly detection start")
logger.info("model loaded {}".format(modelFilename))
logger.info("loaded {} rows".format(nbPoints))

if nbRowsModelTrained != nbPoints:

	dbData = dbData[nbRowsModelTrained:]
	data = vader.build_data_struct(dbData)
	
	preds = model.predict(data)
	valids, anomalies = vader.process_predictions(preds, data)
	
	tday = datetime.date.today()
	now = datetime.datetime.now()
	vader.write_rows_2_file(valids, "valid_{}_{}_{}.txt".format(tday, now.hour, now.minute ))
	vader.write_rows_2_file(anomalies, "anomalies_{}_{}_{}.txt".format(tday, now.hour, now.minute ))
	
	logger.info("new data # rows: {}".format(nbPoints))
	logger.info(data)
	logger.info(preds)


while(True):
	dbData = pull_data(username, passwd)
	newNbPoints = len(dbData)
	if(new_data(newNbPoints, nbPoints)):
	
		newData = dbData[nbPoints:]
		newData = vader.build_data_struct(newData)
		
		preds = model.predict(newData)
		valids, anomalies = vader.process_predictions(preds, newData)
		
		tday = datetime.date.today()
		now = datetime.datetime.now()
		vader.write_rows_2_file(valids, "valid_{}_{}_{}.txt".format(tday, now.hour, now.minute ))
		vader.write_rows_2_file(anomalies, "anomalies_{}_{}_{}.txt".format(tday, now.hour, now.minute ))
		
		nbPoints = newNbPoints
		logger.info("new data # rows: {}".format(nbPoints))
		logger.info(newData)
		logger.info(preds)
	time.sleep(900) # every 15 min
