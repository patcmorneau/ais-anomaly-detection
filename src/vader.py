# vessel anomaly detection and error report
#
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⢄⡲⠖⠛⠉⠉⠉⠉⠉⠙⠛⠿⣿⣶⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠔⣡⠖⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠔⣡⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡔⢡⣶⠏⠀⠀⠀⠀⠀⠀⣠⣴⣶⣶⣶⣶⣶⣶⣦⣄⣸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠌⢀⣿⠏⠀⠀⠀⠀⠀⠀⠸⠿⠋⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡞⠀⡼⢿⣦⣄⠠⠤⠐⠒⠒⠒⠢⠤⣄⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠀⠀⠀⣸⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⢠⠞⠁⠀⠀⠠⠇⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠈⠙⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⢀⣴⣁⠀⣀⣤⣴⣾⣿⣿⣿⣿⡿⢿⣿⣶⣄⠀⠀⠀⠀⠀⣿⣷⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⡇⠘⠟⣻⣿⣧⠀⠀⠀⠀⢿⣿⣤⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡿⠀⠀⠸⣿⠿⠋⠉⠁⠛⠻⠿⢿⣧⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⣿⣿⣿⡿⠋⠁⠀⢀⣄⡀⠀⠀⠀⢀⣀⣤⣴⣿⣿⣧⠀⢀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⣿⣿⠏⢀⠀⢀⡴⠿⣿⣿⣷⣶⣾⣿⣿⣿⣿⣿⣿⣿⣇⠀⢷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⣿⣿⣤⣿⣷⡈⠀⠀⠀⠙⠻⣿⣿⣿⣿⠿⠛⠛⣻⣿⣿⡄⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠈⠋⢉⣠⣴⣾⣿⣿⣿⣿⣷⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⢸⣿⣿⢻⡏⢹⠙⡆⠀⠀⠀⠒⠚⢛⣉⣉⣿⣿⣿⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⢀⡞⠁⠉⠀⠁⠀⣄⣀⣠⣴⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣈⡛⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀
#⠀⠀⠀⠀⠛⠋⠉⠉⠉⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⣻⠿⠿⢿⣿⠿⠿⠋⠁⠀⠙⣿⡁⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⠋⠉⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣈⣹⣦⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣀⣀⣼⣿⣄⣀⣀⡄⠀⣀⣀⣠⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀
#⠀⠀⠀⠀⠀⢰⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀
#⠀⠀⠀⢀⣤⣤⣤⣶⣿⣿⣿⣿⠿⠿⠟⠋⢹⠇⠀⠀⢀⣼⣿⣿⣿⣿⣿⡿⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
#⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⢀⡏⠀⠀⢀⣾⠋⣹⣿⣿⣿⡟⠀⠀⣸⡟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
#⢠⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⡼⠀⠀⢀⣾⠏⢀⣿⣿⣿⠋⠀⠀⣰⣿⣧⡀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
#
#____________________________________________________________________________


import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from sklearn.ensemble import IsolationForest

def curve(x, a, b, c):
	return a*np.log(x + b)+c


def line(x, a, b, c):
	return a * x + b


def calculate_curve_rmse(x, y, fittedParam):
	modelPredictions = curve(x, *fittedParam) 
	absError = modelPredictions - y
	SE = np.square(absError)
	MSE = np.mean(SE) 
	return np.sqrt(MSE)


def calculate_line_rmse(x, y, fittedParam):
	modelPredictions = line(x, *fittedParam) 
	absError = modelPredictions - y
	SE = np.square(absError) 
	MSE = np.mean(SE)
	return np.sqrt(MSE)


def vessel_exist(vessels, vessel):
	for boat in vessels:
		if boat == vessel:
			return True
	return False


def build_vessels_data(dbData):
	vessels = {}
	rowData = []
	for row in dbData:
		vesselID = row[0]
		if vessel_exist(list(vessels.keys()), vesselID):
			rowData = row[1:]
			vesselData = vessels[row[0]]
			vesselData.append(rowData)
			vessels[vesselID] = vesselData
		else:
			rowData = row[1:]
			vesselData = []
			vesselData.append(rowData)
			vessels[vesselID] = vesselData

	return vessels


def get_coordinates(vesselData):
	coordinates = []
	for row in vesselData:
		coord = [row[3],row[4]]
		coordinates.append(coord)
	return coordinates

	
def get_lat_lon_speed(vesselData):
	lat = []
	lon = []
	speed = []
	for row in vesselData:
		lat.append(row[3])
		lon.append(row[4])
		speed.append(row[1])
	return lat, lon, speed

def get_trajectories(lat, lon, speed):
	index = 0
	trajectories = []
	start = 0
	
	while(index < len(lat)-1):
		index = start+5
		trajectoryLat = lat[start:index]
		trajectoryLon = lon[start:index]
		speedTrajectory = speed[start:index]
		if len(trajectoryLat) > 5:
			lopt, lcov = curve_fit(line, np.array(trajectoryLat), np.array(trajectoryLon))
			rmse = calculate_line_rmse(np.array(trajectoryLat), np.array(trajectoryLon), lopt)
		
			while(rmse < 0.00009 and index < len(lat)-1):
				index = index +1
				trajectoryLat.append(lat[index])
				trajectoryLon.append(lon[index])
				speedTrajectory.append(speed[index])
				lopt, lcov = curve_fit(line, np.array(trajectoryLat), np.array(trajectoryLon))
				rmse = calculate_line_rmse(np.array(trajectoryLat), np.array(trajectoryLon), lopt)

		trajectories.append([trajectoryLat, trajectoryLon, speedTrajectory])
		start = index + 1
	
	return trajectories

def compute_vector(trajectory):
	x1 = trajectory[0][0]
	y1 = trajectory[1][0]
	x2 = trajectory[0][len(trajectory[1])-1]
	y2 = trajectory[1][len(trajectory[1])-1]
	return [ x2-x1 , y2 - y1]

def compute_avg_speed(trajectory):
	return np.average(trajectory[2])

def compute_features(trajectories):
	vectors = []
	avgSpeeds =[]
	trajectoriesStartPosition = []
	for trajectory in trajectories:
		vectors.append(compute_vector(trajectory))
		avgSpeeds.append(compute_avg_speed(trajectory))
		trajectoriesStartPosition.append((trajectory[0][0], trajectory[1][0]))
	return trajectoriesStartPosition, vectors, avgSpeeds
	

def write_trajectory(trajectory, filePath):
	trajectory =  trajectory[:2]
	with open(filePath, 'a') as fp:
		fp.write("y x\n")
		for i in range(len(trajectory[0])-1):
			fp.write(str(trajectory[0][i])+ ' '+ str(trajectory[1][i])+'\n' )

###############MAIN##################

db = mysql.connector.connect(
  host="cidco.ca",
  user="aisuser",
  password="AisOuananiche314151!",
  database="ais"
)

cursor = db.cursor()

cursor.execute("SELECT * FROM ais.clean_data")

allCleanData = cursor.fetchall()

vessels = build_vessels_data(allCleanData)
# print(len(vessels[316022934]))
# print(len(vessels))
# print(vessels.keys())
# print(len(vessels[list(vessels.keys())[8]]))
"""
lat, lon, speed = get_lat_lon_speed(vessels[232027158]) # 316022934
trajectories = get_trajectories(lat, lon, speed)
trajectoriesStartPosition, vectors, avgSpeeds = compute_features(trajectories)
"""
#write_trajectory(trajectories[0], 'test.txt')
"""
for i in range(len(trajectories)):
	filePath = 'trajectory_'+str(i)+'.txt'
	write_trajectory(trajectories[i], filePath)
"""

#plt.plot(np.array(trajectoryLat), line(np.array(trajectoryLat), *lopt))
#plt.scatter(trajectoryLat, trajectoryLon)
#plt.show()

features = []
for vessel in vessels:
	if len(vessels[vessel]) > 5:
		lat, lon, speed = get_lat_lon_speed(vessels[vessel])
		trajectories = get_trajectories(lat, lon, speed)
		trajectoriesStartPosition, vectors, avgSpeeds = compute_features(trajectories)
		for i in range(len(vectors)):
			features.append([trajectoriesStartPosition[i][0],trajectoriesStartPosition[i][1], vectors[i][0],vectors[i][1], avgSpeeds[i]])

#print(len(features))



clf = IsolationForest()
clf.fit(np.array(features))
preds = clf.predict(np.array(features))

valids = []
anomalies = []
for i in range(len(features)):
	if preds[i] == 1:
		valids.append(features[i])
	elif preds[i] == -1:
		anomalies.append(features[i])

#write_points_2_file(valids, "valid.txt")
#write_points_2_file(anomalies, "anomalies.txt")


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

