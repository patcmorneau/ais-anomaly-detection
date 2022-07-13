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


def build_training_data(dbData):
	trainingData = []
	for row in dbData:
		#print(row[2:])
		features = [float(x) for x in row[2:]]
		trainingData.append(features)
	return trainingData	

def check_4_new_data(oldNbPoints):
	cursor.execute("SELECT * FROM ais.clean_data")
	allCleanData = cursor.fetchall()
	if len(allCleanData > oldNbPoints):
		return true, (allCleanData - oldNbPoints)
	else:
		return false, 0

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
	
################MAIN############

if len(sys.argv) != 3:
	sys.stderr.write("Usage: padme.py user password\n")
	sys.exit(1)

username = sys.argv[1]
passwd = sys.argv[2]


db = mysql.connector.connect(
  host="cidco.ca",
  user= username,
  password=passwd,
  database="ais"
)

cursor = db.cursor()

cursor.execute("SELECT * FROM ais.clean_data")

allCleanData = cursor.fetchall()

trainingData = build_training_data(allCleanData)

points = get_points(allCleanData)


nbPoints = len(allCleanData)

#print(trainingData)

clf = IsolationForest()
clf.fit(np.array(trainingData))
preds = clf.predict(trainingData)


valids = []
anomalies = []
for i in range(len(points)):
	if preds[i] == 1:
		valids.append(points[i])
	elif preds[i] == -1:
		anomalies.append(points[i])

write_points_2_file(valids, "valid.txt")
write_points_2_file(anomalies, "anomalies.txt")


validXs = []
validYs = []
for point in valids:
	validXs.append(point[1])
	validYs.append(point[0])

anomalieXs = []
anomalieYs = []
for point in anomalies:
	anomalieXs.append(point[1])
	anomalieYs.append(point[0])


plt.scatter(validXs, validYs, c="green")
plt.scatter(anomalieXs, anomalieYs, c="red")
plt.show()


# TODO
"""
while(true):
	newData, nbNewPoints = check_4_new_data(nbPoints)
	if(newData):
		clf.predict(newPoints)
	
	time.sleep(900) # every 15 min
"""
