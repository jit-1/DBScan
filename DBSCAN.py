import os
import sys
from math import *
import math
import numpy as np
# from scipy.optimize import brentq

def get_spherical_distance(lat1,lat2,long1,long2):
	"""
	Get spherical distance any two points given their co-ordinates (latitude, longitude)
	"""
	q=radians(lat2-lat1)
	r=radians(long2-long1)
	lat2r=radians(lat2)
	lat1r=radians(lat1)
	a=sin(q/2)*sin(q/2)+cos(lat1r)*cos(lat2r)*sin(r/2)*sin(r/2)
	c=2*atan2(sqrt(a),sqrt(1-a))
	R=6371*1000
	d=R*c
	return d

def expandCluster(point,pointSet):
	# print "Expanding cluster for", point
	Nn = []
	for pt in pointSet:
		dist = get_spherical_distance(pt[0],point[0],pt[1],point[1])
		if dist<eps:
			Nn.insert(len(Nn),pt)
	return Nn

def union(list1,list2):
	res = list1
	for i in list2:
		if i not in res:
			res.append(i)
	return res

def getMean(points):
	total_lat= 0
	total_long = 0
	for point in points:
		total_long += point[1]
		total_lat += point[0]
	length = len(points)
	mean_lat = total_lat/length
	mean_long = total_long/length
	total_distance = 0
	tn_sum =0
	for point in points:
		total_distance += math.sqrt(math.pow(mean_lat-point[0],2)+math.pow(mean_long-point[1],2))
		#tn_sum = tn_sum + int(point[2])
	mean_distance = total_distance/length
	return (mean_lat,mean_long,mean_distance,float(tn_sum)/length,counter)

def getOne(points):
	return points[len(points)/2]

def fileWrite(points,file):
	for point in points:
		#print("In fileWriter")
		#print (point)
		#print("Out of FW")
		for item in range(len(point)):
			if item != (len(point)-1):
				print("here")
				print (item)
				print("outofhere")
				file.write(str(point[item])+",")
			else:
				file.write(str(point[item]))
		file.write("\n")

def minus(totalPts,neighbourhood):
	tp = totalPts[:]
	for n in neighbourhood:
		try:
			tp.remove(n)
		except Exception as e:
			print('fishy!!')
	return tp
try:
	fileName= sys.argv[1]
	eps = float(sys.argv[2])
	minpts = int(sys.argv[3])
	outputFile = sys.argv[4]
except Exception as e:
	with open('config','r') as inf:
			config = eval(inf.read())

	fileName= config["input_file"]
	eps = float(config["eps"])
	minpts = int(config["minpts"])
	outputFile = config["output_file"]

file = open(fileName,"r")
lines = file.read().split('\n')
file.close()
counter=0

lines = lines[1:]

pointSet = []

for line in lines:
	components = line.split(',')
	try:
		point_x = float(components[0])
		point_y = float(components[1])
		#timeunits = components[2].split(':')
		#point_t = ((int(timeunits[0])*60) + int(timeunits[1])) * 60 + int(timeunits[2])
		#pointSet.insert(len(pointSet), (point_x,point_y,point_t))
		#pointSet += [(point_x,point_y,point_t)]
		pointSet += [(point_x,point_y,counter)]
	except Exception as e:
		print(e)
	#print(line)
	pass

pts = pointSet[:]

clusters = []
for point in pointSet:
	# print point
	if(point not in pts):
		continue
	pts.remove(point)
	#print len(pts), len(pointSet)
	N = expandCluster(point,pts)
	#fileWrite(N)	
	if len(N) >= minpts:
		# print point,'is corepoint with'
		C = [point]
		pts = minus(pts,N)
		for neighbour in N:
			#print C,neighbour,(neighbour in pts)
			#print "Neighbour ", neighbour
			C = C + [neighbour]
			#pts.remove(neighbour)	
			N1 = expandCluster(neighbour,pts)
			if len(N1) > minpts:
				N = N + N1
				pts = minus(pts,N1)
		clusters.insert(len(clusters),C)
print ("\n\n************Cluster**************\n\n")
stops=[]
test=[]
#print (type(temp))
for count in range(0,len(clusters)):
	print ("Cluster %d" % count)
	#print (temp[count])
	for in_cluster in range(0,len(clusters[count])):
		
		temp=list(clusters[count][in_cluster])
		#print(type(temp))
		#temp[count][in_cluster][2]=count
		temp[2]=count
		#clusters=tuple(temp)
		print (temp)
		test.append(temp)
	stops.append(temp)
"""
file
#print(clusters)
stops = []
#i=0
for stop in clusters:
	'''
	i=i+1
	file = open('clus_'+str(i),'w')
	fileWrite(stop,file)
	file.close()
	'''
	mean_stop = getMean(stop)
	stops.append(mean_stop)
	#stops.append(counter)
	#counter+=1
"""

file = open(outputFile,'w')
fileWrite(test,file)
file.close()

print("**********************test****************")
print(test)
print("*********************end*******************")
print(len(clusters), " stops found")
print("Created PS file...",outputFile)

