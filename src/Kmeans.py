
import sys
import numpy as np
from pyspark import SparkContext
from numpy import array
from math import sqrt



def kmeans(latitude,longitude):
  min_distance = float("inf")# initializing the minimum distance from the centroid
  j = 1#count for the centroids
  cluster=0#initializing cluster number
  #clusterCenter=[]
  for i in centroidList:#loop in the centroid list to find the nearest one
    distance=np.sqrt((float(latitude)-i[0])**2 + (float(longitude)-i[1])**2)# finding the distance between the point and the centroid
    #dist = np.sqrt(sum((latlong - i) ** 2))	
    if distance < min_distance:# if the distance is less than the minimum distance assign the minimum distance to the present distance
	  min_distance = distance
	  cluster = j
          clusterCenter=i
    j = j + 1# increment the j value
  return (cluster, (float(latitude),float(longitude)))# return the cluster number and the latitute and the longitute
 

if __name__ == "__main__":
  if len(sys.argv) !=2:
    print >> sys.stderr, "Usage: spark-submit Kmeans.py <inputdatafile>"
    exit(-1)

  sc = SparkContext(appName="K means Clustering")

  inputf = sc.textFile(sys.argv[1])
  h = inputf.first()# the header of the input file
  inputWithoutHeader = inputf.filter(lambda line : line!= h) #taking the input without the header and just the values 
  rddR = inputWithoutHeader.map(lambda line: line.split(','))# split to array seperated by commas
  rdd =  rddR.filter(lambda x: x[20] is not u'')#take the values for which the latitude and longitute is not null
  N = rdd.count()# total number of crimes occurred
  k = 60# found optimal k value from the elbow method
  Iterations = 35# found optimal iterations value from the elbow method
  f = ((k+30)/(N*0.1)) * 0.1
  sample = rdd.sample(True, f, 2000)
  listv = sample.map(lambda line: (line[20], line[21])).take(k)# taking the sample data for the initial centroid values
  centroidList = np.array(listv).astype('float')# initial centroid list
  
  for i in range(Iterations):
    rddCluster = rdd.map(lambda line: kmeans(line[20], line[21]))# passing the values for k means function with latitude and longitude to find the nearest centroid
    rddsum=rddcluster.reduceByKey(lambda a,b :(a[0]+b[0], a[1]+b[1]))
    rddcount=rddcluster.countByKey()
    rddAvg=rddsum.map(lambda v: (v[0],(v[1][0]/rddcount[v[0]], v[1][1]/rddcount[v[0]])))#calculating the average for the values in the centroid
    centroidList = np.array(rddAvg.values().collect()).astype('float')#assigning the new centroid list
  rddFinal = rdd.map(lambda line: kmeans(line[20], line[21]))

  
  l = rddFinal.map(lambda line :','.join(str(d) for d in line))# converting the output to csv file. we get output in many parts but in same sequence as input
  l.saveAsTextFile('kmeansOutput')# save as text file
  
  
  sc.stop()
