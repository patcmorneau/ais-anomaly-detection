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
		point = [float(x) for x in row[2:4]]
		points.append(point)
	return points
	
def get_speed_lat_lon(data):
	sll = []
	for row in data:
		point = [row[0], row[2], row[3]]
		sll.append(point)
	return sll

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


def gen_cluster_anomalies(nb_anomalies, minMaxs, means, meanErrors):
	n = 0
	anomalies = []
	
	mCourse = means[1]
	mHeading = means[4]
	
	if mCourse > 180:
		mCourse -= 180
	
	if mHeading > 180:
		mHeading -= 180

	while( n < nb_anomalies):
		n+=1
		speedAnomaly = random.uniform(means[0], minMaxs[0][1]) + meanErrors[0]*3
		courseAnomaly = random.uniform(mCourse+90, mCourse+180)
		latAnomaly = random.uniform(minMaxs[2][0], minMaxs[2][1])
		lonAnomaly = random.uniform(minMaxs[3][0], minMaxs[3][1])
		headingAnomaly = random.uniform(mHeading+90, mHeading+180)
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

def get_min_max(array):
	return [np.min(array), np.max(array)]


def gen_anomalies(pointsPerCluster):
	anomaliesData = []
	for cluster in pointsPerCluster:
		write_points_2_file(pointsPerCluster[cluster], "/media/sf_linux_virt_share/anomaly/cluster_{}.txt".format(cluster))
		speed,course,lat,lon,heading = split_data(pointsPerCluster[cluster])

		speedMinMax = get_min_max(speed)
		mSpeed = np.mean(speed)
		meSpeed = np.mean(abs(mSpeed - speed))
		
		courseMinMax = get_min_max(course)
		mCourse = np.mean(course)
		meCourse = np.mean(abs(mCourse -course))
		
		latMinMax = get_min_max(lat)
		mLat = np.mean(lat)
		meLat = np.mean(abs(mLat -lat))
		
		lonMinMax = get_min_max(lon)
		mLon = np.mean(lon)
		meLon = np.mean(abs(mLon -lon))
		
		headingMinMax = get_min_max(heading)
		mHeading = np.mean(heading)
		meHeading = np.mean(abs(mHeading -heading))
		
		#print(np.mean(speed), np.mean(course), np.mean(lat), np.mean(lon), np.mean(heading))
		means = [mSpeed, mCourse, mLat, mLon, mHeading]
		minMaxMaxs = [speedMinMax, courseMinMax, latMinMax, lonMinMax, headingMinMax]
		meanErrors = [meSpeed, meCourse, meLat, meLon, meHeading]
		
		anomaliesData+= gen_cluster_anomalies(len(speed)/10, minMaxMaxs, means, meanErrors)
	return anomaliesData
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

#speedLatLon = get_speed_lat_lon(data)


#nbCluster = find_best_nb_cluster(points, 50)
nbCluster = 8

#print("nb cluster: ", nbCluster)

kmeans = KMeans(n_clusters=nbCluster)
kmeans.fit(points)

#print(kmeans.labels_)

pointsPerCluster = {}
for i in range(nbCluster):
	pointsPerCluster[i] = []

#print(pointsPerCluster.keys())


for i in range(len(kmeans.labels_)):
	pointsPerCluster[kmeans.labels_[i]].append(data[i])
	

anomaliesData = gen_anomalies(pointsPerCluster)
trainingData = data + anomaliesData

clf = IsolationForest()
clf.fit(np.array(trainingData))
preds = clf.predict(trainingData)


valids = []
anomalies = []
for i in range(len(data)):
	if preds[i] == 1:
		valids.append(data[i])
	elif preds[i] == -1:
		anomalies.append(data[i])
#print(valids, anomalies)
write_points_2_file(valids, "/media/sf_linux_virt_share/anomaly/true_valid.txt")
write_points_2_file(anomalies, "/media/sf_linux_virt_share/anomaly/true_anomalies.txt")

print("anomalies %: ", (len(anomalies) / len(data)) * 100)

valids = []
anomalies = []
for i in range(len(anomaliesData)):
	if preds[i] == 1:
		valids.append(anomaliesData[i])
	elif preds[i] == -1:
		anomalies.append(anomaliesData[i])
#print(valids, anomalies)
write_points_2_file(valids, "/media/sf_linux_virt_share/anomaly/generated_valid.txt")
write_points_2_file(anomalies, "/media/sf_linux_virt_share/anomaly/generated_anomalies.txt")


