# point anomaly detection marina establishing

#⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀ ⠀⠀⠀⠀⠀⡠⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⠆⠀⠀⠀⠀⠀⢄⡀⠀⠀⠀⠀⠀
#⠀ ⠀⠀⠀⣴⡟⠀⠀⠀⠀⣰⣦⣀⢻⣿⣿⡏⣀⣴⣄⠀⠀⠀⠀⢻⣦⡀⠀⠀⠀
#⠀ ⠀⢠⣾⡿⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀⢻⣿⣄⠀⠀
#  ⢠⣿⣿⠇⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⡆⠀
#  ⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⠀
# ⢸⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⡇
# ⢸⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⡇
# ⢸⣿⣿⣿⣿⣿⣷⣦⣀⣀⣀⣴⣿⣿⣿⣿⣿⣿⣤⣀⣀⣀⣴⣿⣿⣿⣿⣿⣿⡇
# ⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁
# ⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀
# ⠀⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀
# ⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀
# ⠀⠀⠀⠀⠀⠈⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠿⠿⣿⣿⣿⣿⡿⠿⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀



import mysql.connector
from sklearn.ensemble import IsolationForest
import numpy as np
import time
import matplotlib.pyplot as plt
import sys
import datetime
import logging
import pickle

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

def build_training_data(dbData):
	trainingData = []
	pointID = 0
	for row in dbData:
		features = [float(x) for x in row[2:]]
		features.insert(0, pointID)
		trainingData.append(features)
		pointID += 1
	return trainingData	

def new_data(newNbPoints, oldNbPoints):
	print("new_data :", newNbPoints - oldNbPoints)
	
	if newNbPoints > oldNbPoints:
		return True
	else:
		return False
	
def get_points(dbData):
	points = []
	for row in dbData:
		point = [float(x) for x in row[4:6]]
		points.append(point)
	return points

def write_points_2_file(points, outfilePath):
	with open(outfilePath, 'a') as fp:
		fp.write("x y\n")
		for point in points:
			fp.write(str(point[1])+ " "+ str(point[0])+"\n")

def process_predictions(preds, points):
	valids = []
	anomalies = []
	for i in range(len(points)):
		if preds[i] == 1:
			valids.append(points[i])
		elif preds[i] == -1:
			anomalies.append(points[i])
	
	tday = datetime.date.today()
	time = datetime.datetime.now()
	
	write_points_2_file(valids, "valid_{}_{}_{}.txt".format(tday, time.hour, time.minute ))
	write_points_2_file(anomalies, "anomalies_{}_{}_{}.txt".format(tday, time.hour, time.minute ))
	
################MAIN############

if len(sys.argv) != 5:
	sys.stderr.write("Usage: padme.py user password modelFilename nb-of-rows-model-trained-on\n")
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
	data = build_training_data(dbData)
	#print(data)
	points = get_points(dbData)
	preds = model.predict(data)
	process_predictions(preds, points)
	nbPoints += len(data)
	logger.info("new data # rows: {}".format(nbPoints))
	logger.info(data)
	logger.info(preds)

while(True):
	dbData = pull_data(username, passwd)
	newNbPoints = len(dbData)
	if(new_data(newNbPoints, nbPoints)):
		newData = dbData[nbPoints:]
		newData = build_training_data(newData)
		points = get_points(newData)
		preds = model.predict(newData)
		process_predictions(preds, points)
		nbPoints = newNbPoints
		logger.info("new data # rows: {}".format(nbPoints))
		logger.info(newData)
		logger.info(preds)
	time.sleep(900) # every 15 min

