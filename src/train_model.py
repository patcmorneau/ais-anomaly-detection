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
import pickle
import logging
import vader

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

def gen_anomalies(pointsPerCluster, fakeID):
	anomaliesData = []
	for cluster in pointsPerCluster:
		#write_points_2_file(pointsPerCluster[cluster], "/media/sf_linux_virt_share/anomaly/cluster_{}.txt".format(cluster))
		speed,course,lat,lon,heading = vader.split_data(pointsPerCluster[cluster])

		speedMinMax = vader.get_min_max(speed)
		mSpeed = np.mean(speed)
		meSpeed = np.mean(abs(mSpeed - speed))
		
		courseMinMax = vader.get_min_max(course)
		mCourse = np.mean(course)
		meCourse = np.mean(abs(mCourse -course))
		
		latMinMax = vader.get_min_max(lat)
		mLat = np.mean(lat)
		meLat = np.mean(abs(mLat -lat))
		
		lonMinMax = vader.get_min_max(lon)
		mLon = np.mean(lon)
		meLon = np.mean(abs(mLon -lon))
		
		headingMinMax = vader.get_min_max(heading)
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

	
################MAIN############

if len(sys.argv) != 3:
	sys.stderr.write("Usage: paad.py user password\n")
	sys.exit(1)

username = sys.argv[1]
passwd = sys.argv[2]

logging.basicConfig(filename="training-model_{}.log".format(datetime.date.today()),
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)



db = mysql.connector.connect(
  host="cidco.ca",
  user=username,
  password=passwd,
  database="ais"
)

cursor = db.cursor()

cursor.execute("SELECT * FROM ais.clean_data")

allCleanData = cursor.fetchall()

data = vader.build_data_struct(allCleanData)

logger.info("model train on {} rows".format(len(data)))

""" split the dataset in cluster by lat lon only """
points = vader.get_points(data)
nbCluster = 8
kmeans = KMeans(n_clusters=nbCluster)
kmeans.fit(points)

logger.info("Cluster number used: {}".format(nbCluster))


pointsPerCluster = {}
for i in range(nbCluster):
	pointsPerCluster[i] = []


for i in range(len(kmeans.labels_)):
	pointsPerCluster[kmeans.labels_[i]].append(data[i])

""" perform anomaly detection on each cluster individually """
anomaliesPerCluster = []
for cluster in pointsPerCluster:
	preds = anomalies_in_cluster(pointsPerCluster[cluster])
	valids, anomalies = vader.process_predictions(preds, pointsPerCluster[cluster])
	#write_points_2_file(valids, "/media/sf_linux_virt_share/anomaly/cluster_{}valids.txt".format(cluster))
	#write_points_2_file(anomalies, "/media/sf_linux_virt_share/anomaly/cluster_{}anomalies.txt".format(cluster))
	anomaliesPerCluster += anomalies


""" add anomalic data """
fakeID = len(data)+1
anomaliesData = gen_anomalies(pointsPerCluster, fakeID)
trainingData = data[1:] + anomaliesData[1:]


""" perform anomaly detection on all the data including the generated data """
clf = IsolationForest()
clf.fit(np.array(trainingData))
preds = clf.predict(trainingData)
valids, anomalies = vader.process_predictions(preds, data)

vader.write_rows_2_file(valids, "/media/sf_linux_virt_share/anomaly/true_valid.txt")
vader.write_rows_2_file(anomalies, "/media/sf_linux_virt_share/anomaly/true_anomalies.txt")


logger.info("percentage of anomalies in data: {}".format((len(anomalies) / len(data)) * 100))

""" if anomaly in cluster + anomaly in dataset -> probably an anomaly """
ids = np.array(anomalies)[:, 0]
ids2 = np.array(anomaliesPerCluster)[:, 0]

newlist = [x for x in ids if x in ids2]


logger.info("percentage of anomalies in cluster AND in data: {}".format( (len(newlist) / len(data)) * 100))

anomaliesFinal = []
for ID in newlist:
	x = int(ID)
	anomaliesFinal.append(data[x])


vader.write_rows_2_file(anomaliesFinal, "/media/sf_linux_virt_share/anomaly/anomaliesFinal.txt")

pickle.dump(clf,open("AIS_anomaly_detection_{}.model".format(datetime.date.today()),"wb"))
logger.info("model created :)")
