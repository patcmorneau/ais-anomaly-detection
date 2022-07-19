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

def get_points(data):
	points = []
	for row in data:
		point = [float(x) for x in row[3:5]]
		points.append(point)
	return points

def build_data_struct(dbData):
	data = []
	pointID = 0
	for row in dbData:
		features = [float(x) for x in row[2:]]
		features.insert(0, pointID)
		data.append(features)
		pointID += 1
	return data

def split_data(data):
	lat,lon,speed,course,heading = [],[],[],[],[]
	for row in data:
		speed.append(row[1])
		course.append(row[2])
		lat.append(row[3])
		lon.append(row[4])
		heading.append(row[5])
	return speed,course,lat,lon,heading


def gen_cluster_anomalies(nb_anomalies, minMaxs, means, meanErrors, fakeID):
	n = 0
	anomalies = []
	anomaly = 0
	
	mCourse = means[1]
	mHeading = means[4]
	
	if mCourse > 180:
		anomaly = -180
	
	if mHeading > 180:
		anomaly = -180

	while( n < nb_anomalies):
		n+=1
		fakeID += 1
		speedAnomaly = random.uniform(means[0], minMaxs[0][1]) + means[0]
		courseAnomaly = random.uniform(mCourse+anomaly+90, mCourse+180+anomaly)
		latAnomaly = random.uniform(minMaxs[2][0], minMaxs[2][1])
		lonAnomaly = random.uniform(minMaxs[3][0], minMaxs[3][1])
		headingAnomaly = random.uniform(mHeading+90+anomaly, mHeading+180+anomaly)
		anomalies.append([fakeID, speedAnomaly, courseAnomaly, latAnomaly, lonAnomaly, headingAnomaly])
		
	return anomalies

def write_points_2_file(points, outfilePath):
	with open(outfilePath, 'w') as fp:
		fp.write("id x y speed course heading\n")
		for point in points:
			fp.write(str(point[0])+ " "+str(point[4])+ " "+ str(point[3])+" "+ str(point[1])+" "+ str(point[2])+" "+ str(point[5])+ "\n")

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


def gen_anomalies(pointsPerCluster, fakeID):
	anomaliesData = []
	for cluster in pointsPerCluster:
		#write_points_2_file(pointsPerCluster[cluster], "/media/sf_linux_virt_share/anomaly/cluster_{}.txt".format(cluster))
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
		
		means = [mSpeed, mCourse, mLat, mLon, mHeading]
		minMaxMaxs = [speedMinMax, courseMinMax, latMinMax, lonMinMax, headingMinMax]
		meanErrors = [meSpeed, meCourse, meLat, meLon, meHeading]
		
		anomaliesData += gen_cluster_anomalies(len(speed)/10, minMaxMaxs, means, meanErrors, fakeID)
		fakeID += len(anomalies)+1
	return anomaliesData

def anomalies_in_cluster(clusterPoints):
	clf = IsolationForest()
	clf.fit(np.array(clusterPoints))
	return clf.predict(clusterPoints)
	
	
def process_predictions(preds, data):
	valids = []
	anomalies = []
	for i in range(len(data)):
		if preds[i] == 1:
			valids.append(data[i])
		elif preds[i] == -1:
			anomalies.append(data[i])
	
	return valids, anomalies
	
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


""" split the dataset in cluster by lat lon only """
points = get_points(data)
nbCluster = 8
kmeans = KMeans(n_clusters=nbCluster)
kmeans.fit(points)

pointsPerCluster = {}
for i in range(nbCluster):
	pointsPerCluster[i] = []


for i in range(len(kmeans.labels_)):
	pointsPerCluster[kmeans.labels_[i]].append(data[i])

""" perform anomaly detection on each cluster individually """
anomaliesPerCluster = []
for cluster in pointsPerCluster:
	preds = anomalies_in_cluster(pointsPerCluster[cluster])
	valids, anomalies = process_predictions(preds, pointsPerCluster[cluster])
	#write_points_2_file(valids, "/media/sf_linux_virt_share/anomaly/cluster_{}valids.txt".format(cluster))
	#write_points_2_file(anomalies, "/media/sf_linux_virt_share/anomaly/cluster_{}anomalies.txt".format(cluster))
	anomaliesPerCluster += anomalies


""" add anomalic data """
fakeID = len(data)+1
anomaliesData = gen_anomalies(pointsPerCluster, fakeID)
trainingData = data + anomaliesData


""" perform anomaly detection on all the data including the generated data """
clf = IsolationForest()
clf.fit(np.array(trainingData))
preds = clf.predict(trainingData)
valids, anomalies = process_predictions(preds, data)

write_points_2_file(valids, "/media/sf_linux_virt_share/anomaly/true_valid.txt")
write_points_2_file(anomalies, "/media/sf_linux_virt_share/anomaly/true_anomalies.txt")

print("anomalies %: ", (len(anomalies) / len(data)) * 100) # pourcentage of anomalies in all the real data


""" if anomaly in cluster + anomaly in dataset -> probably an anomaly """
ids = np.array(anomalies)[:, 0]
ids2 = np.array(anomaliesPerCluster)[:, 0]

newlist = [x for x in ids if x in ids2]


print("anomalies %: ", (len(newlist) / len(data)) * 100) 

anomaliesFinal = []
for ID in newlist:
	x = int(ID)
	anomaliesFinal.append(data[x])
	


write_points_2_file(anomaliesFinal, "/media/sf_linux_virt_share/anomaly/anomaliesFinal.txt")





"""
valids = []
anomalies = []
for i in range(len(data),len(trainingData)):
	if preds[i] == 1:
		valids.append(trainingData[i])
	elif preds[i] == -1:
		anomalies.append(trainingData[i])
#print(valids, anomalies)
write_points_2_file(valids, "/media/sf_linux_virt_share/anomaly/generated_valid.txt")
write_points_2_file(anomalies, "/media/sf_linux_virt_share/anomaly/generated_anomalies.txt")

"""
