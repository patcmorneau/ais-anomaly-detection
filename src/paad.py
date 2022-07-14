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

def build_data_struct(dbData):
	data = []
	for row in dbData:
		#print(row[2:])
		features = [float(x) for x in row[2:]]
		data.append(features)
	return data

def split_data(data):
	lat,lon,speed,course,heading = [],[],[],[],[]
	for row in data:
		#print(row)
		speed.append(row[0])
		course.append(row[1])
		lat.append(row[2])
		lon.append(row[3])
		heading.append(row[4])
		#break;
	return speed,course,lat,lon,heading

def compute_areas(lat, lon):
	lat.sort()
	lon.sort()
	latMin = lat[0]
	lonMin = lon[0]
	latMax = lat[len(lat)-1]
	lonMax = lon[len(lon)-1]
	middleLat = (latMax-latMin)/2 + latMin
	middleLon = (lonMax-lonMin)/2 + lonMin
	return [[[latMax, lonMin],[middleLat, middleLon]],
		 	[[middleLat, lonMin],[latMin, middleLon]],
		 	[[latMax, middleLon],[middleLat, lonMax]],
		 	[[middleLat, middleLon],[latMin, lonMax]]]

def point_is_in_area(point, area):
	if point[0] <= area[0][0] and point[0] >= area[1][0] and point[1] >= area[0][1] and point[1] <= area[1][1]:
		return True
	else:
		return False
"""		
area = [[48.766898, -68.978717], [48.611174, -68.66099249999999]]
point = [48.65, -68.7]
print(point_is_in_area(point, area))
"""

def gen_anomalies(nb_anomalies, means, meanErrors):
	n = 0
	anomalies = []
	while( n < nb_anomalies):
		n+=1
		speedAnomaly = means[0] + random.uniform(meanErrors[0]*2, meanErrors[0]*3)
		courseAnomaly = means[1] + random.uniform(meanErrors[1]*2, meanErrors[0]*3)
		latAnomaly = means[2] + random.uniform(meanErrors[2]/10, meanErrors[0]/5)
		lonAnomaly = means[3] + random.uniform(meanErrors[3]/10, meanErrors[0]/5)
		headingAnomaly = means[4] + random.uniform(meanErrors[4]*2, meanErrors[0]*3)
		anomalies.append([speedAnomaly, courseAnomaly, latAnomaly, lonAnomaly, headingAnomaly])
	return anomalies

def write_points_2_file(points, outfilePath):
	with open(outfilePath, 'a') as fp:
		fp.write("x y\n")
		for point in points:
			fp.write(str(point[1])+ " "+ str(point[0])+"\n")

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

speed,course,lat,lon,heading = split_data(data)

#print(len(lat), len(data))

areas = compute_areas(lat, lon)
#print(areas)
"""

latMin = areas[0][1][1]
lonMin = areas[0]
latMax = areas[0]
lonMax = areas[0]

print()
"""

area1 = []
area2 = []
area3 = []
area4 = []
for row in data:
	point = [row[2],row[3]]
	for i in range(len(areas)):

		if(point_is_in_area(point, areas[i])):
			if i == 0:
				area1.append(row)
			elif i == 1:
				area2.append(row)
			elif i == 2:
				area3.append(row)
			elif i == 3:
				area4.append(row)

if (len(area1)+len(area2)+len(area3)+len(area4)) == len(data):
	print("ok")


rowsInAreas = [area1,area2,area3,area4]

anomaliesData = []
for areaData in rowsInAreas:
	if len(areaData) > 0:
		speed,course,lat,lon,heading = split_data(areaData)
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
#print(len(anomaliesData), len(data)/4)


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
		valids.append(trainingData[i][2:4])
	elif preds[i] == -1:
		anomalies.append(trainingData[i][2:4])
#print(valids, anomalies)
write_points_2_file(valids, "true_valid.txt")
write_points_2_file(anomalies, "true_anomalies.txt")


valids = []
anomalies = []
for i in range(len(trainingData[len(data):])):
	if preds[i] == 1:
		valids.append(trainingData[i][2:4])
	elif preds[i] == -1:
		anomalies.append(trainingData[i][2:4])
#print(valids, anomalies)
write_points_2_file(valids, "generated_valid.txt")
write_points_2_file(anomalies, "generated_anomalies.txt")
