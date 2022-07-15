#P.A.A.D. point anomaly in area detection

#                ▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                        
#            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                  
#        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓              
#      ▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            
#    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒          
#  ▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓          
#  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        
#░░▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      
#▒▒▓▓▓▓▓▓▓▓▓▓▒▒░░░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░
#▓▓▓▓▓▓▓▓▓▓▓▓▒▒░░░░░░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓▓▓▓▓▓░░
#▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓▓▓▓▓▓      
#▓▓▓▓▓▓▓▓▓▓▒▒▒▒░░░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓          
#▓▓▓▓▓▓▓▓▓▓▓▓▒▒░░░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                
#▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒░░░░▒▒▒▒▓▓▓▓▓▓████████  ██                
#▒▒▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▓▓██        ████  ██                
#░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓██████      ████  ░░                
#  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████████  ████                    
#  ▒▒▓▓▓▓██████▓▓▓▓██▒▒████▓▓▓▓██████████                  
#    ▓▓▓▓▓▓▓▓████████        ▓▓▓▓████████                  
#          ▓▓                    ██▓▓▓▓██                  
#                                    ████                  
#                                      ██                  
#                                      ▓▓▒▒                
#                                      ████                
#                                      ▓▓██                



import mysql.connector
from sklearn.ensemble import IsolationForest
import numpy as np
import time
import matplotlib.pyplot as plt
import sys
import datetime
import random
from sklearn import mixture
from sklearn.cluster import KMeans

def get_points(dbData):
	points = []
	for row in dbData:
		point = [float(x) for x in row[4:6]]
		points.append(point)
	return points

def build_data_struct(dbData):
	data = []
	for row in dbData:
		features = [float(x) for x in row[2:]]
		data.append(features)
	return data

def split_data(data):
	lat,lon,speed,course,heading = [],[],[],[],[]
	for row in data:
		speed.append(row[0])
		course.append(row[1])
		lat.append(row[2])
		lon.append(row[3])
		heading.append(row[4])
	return speed,course,lat,lon,heading


def gen_anomalies(nb_anomalies, means, meanErrors):
	n = 0
	anomalies = []
	while( n < nb_anomalies):
		n+=1
		speedAnomaly = means[0] + random.uniform(meanErrors[0]*2, meanErrors[0]*5)
		courseAnomaly = means[1] + random.uniform(meanErrors[1]*2, meanErrors[0]*5)
		latAnomaly = means[2] + random.uniform(meanErrors[2]/10, meanErrors[0]/5)
		lonAnomaly = means[3] + random.uniform(meanErrors[3]/10, meanErrors[0]/5)
		headingAnomaly = means[4] + random.uniform(meanErrors[4]*2, meanErrors[0]*5)
		anomalies.append([speedAnomaly, courseAnomaly, latAnomaly, lonAnomaly, headingAnomaly])
	return anomalies

def write_points_2_file(points, outfilePath):
	with open(outfilePath, 'w') as fp:
		fp.write("x y speed course heading\n")
		for point in points:
			fp.write(str(point[3])+ " "+ str(point[2])+" "+ str(point[0])+" "+ str(point[1])+" "+ str(point[4])+ "\n")

def find_best_nb_cluster(data, maxClusters):
	n = 4
	bic = []
	lowest_bic = np.infty
	while n <= maxClusters :
		model = mixture.GaussianMixture(n, covariance_type = "full")
		n += 1
		model.fit(np.array(data))
		performance = model.bic(np.array(data))
		bic.append(performance)
		if performance < lowest_bic:
			lowest_bic = performance
		else:
			break;
	return 4 + bic.index(min(bic))

################MAIN############

if len(sys.argv) != 3:
	sys.stderr.write("Usage: paad.py user password\n")
	sys.exit(1)

username = sys.argv[1]
passwd = sys.argv[2]

db = mysql.connector.connect(
  host="cidco.ca",
  user=username,
  password=passwd,
  database="ais"
)

cursor = db.cursor()

cursor.execute("SELECT * FROM ais.clean_data")

allCleanData = cursor.fetchall()

data = build_data_struct(allCleanData)

points = get_points(data)

nbCluster = find_best_nb_cluster(points, 50)

print("nb cluster: ", nbCluster)

kmeans = KMeans(n_clusters=nbCluster)
kmeans.fit(points)

#print(kmeans.labels_)

pointsPerCluster = {}
for i in range(nbCluster):
	pointsPerCluster[i] = []

#print(pointsPerCluster.keys())


for i in range(len(kmeans.labels_)):
	pointsPerCluster[kmeans.labels_[i]].append(data[i])
	

#print(pointsPerCluster)
anomaliesData = []
for cluster in pointsPerCluster:
	write_points_2_file(pointsPerCluster[cluster], "cluster_{}.txt".format(cluster))
	speed,course,lat,lon,heading = split_data(pointsPerCluster[cluster])
	mSpeed = np.mean(speed)
	meSpeed = np.mean(abs(mSpeed - speed))
	mCourse = np.mean(course)
	meCourse = np.mean(abs(mCourse -course))
	mLat = np.mean(lat)
	meLat = np.mean(abs(mLat -lat))
	mLon = np.mean(lon)
	meLon = np.mean(abs(mLon -lon))
	mHeading = np.mean(heading)
	meHeading = np.mean(abs(mHeading -heading))
	means = [mSpeed, mCourse, mLat, mLon, mHeading]
	meanErrors = [meSpeed, meCourse, meLat, meLon, meHeading]
	anomaliesData+= gen_anomalies(len(speed)/2, means, meanErrors)
	
print(len(anomaliesData), len(data)/2)


trainingData = data + anomaliesData
#print(trainingData[0])
#print(trainingData[len(trainingData)-1])

clf = IsolationForest()
clf.fit(np.array(trainingData))
preds = clf.predict(trainingData)


valids = []
anomalies = []
for i in range(len(trainingData[:len(data)-1])):
	if preds[i] == 1:
		valids.append(trainingData[i])
	elif preds[i] == -1:
		anomalies.append(trainingData[i])
#print(valids, anomalies)
write_points_2_file(valids, "true_valid.txt")
write_points_2_file(anomalies, "true_anomalies.txt")


valids = []
anomalies = []
for i in range(len(trainingData[len(data):])):
	if preds[i] == 1:
		valids.append(trainingData[i])
	elif preds[i] == -1:
		anomalies.append(trainingData[i])
#print(valids, anomalies)
write_points_2_file(valids, "generated_valid.txt")
write_points_2_file(anomalies, "generated_anomalies.txt")
