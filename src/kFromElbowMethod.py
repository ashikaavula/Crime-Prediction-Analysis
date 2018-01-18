
import sys
import numpy as np
from pyspark import SparkContext
from numpy import array
from math import sqrt

#importing the library
from pyspark.mllib.clustering import KMeans, KMeansModel


sc = SparkContext(appName="K means Clustering")

#The input file is full chicago crimes dataset
input = sc.textFile(sys.argv[1])

#The first line is read into h 
header = input.first()

#We are filtering out the data by removing the header which contains headings
inputWithNoHeader = input.filter(lambda line : line!= header)  
rddInitial = inputWithNoHeader.map(lambda line: line.split(','))

#Deleting the rows in which location column is empty
rdd =  rddInitial.filter(lambda x: x[20] is not u'')

#Taking latitude and longitude columns data for clustering.
rddLoc = rdd.map(lambda line: (float(line[20]), float(line[21])))
arr=[]

#Finding the optimum K value for clusters we used KMeansModel library
for k in range(10,160,10):

    #Taking sample list for initial centroids 
    samplelist = sc.parallelize(rdd.take(k))
    list = samplelist.map(lambda line: (line[20], line[21])).collect()
    sample_centroidlist = np.array(list).astype('float')
    model = KMeans.train(rddLoc , k, maxIterations= 30, initialModel = KMeansModel(sample_centroidlist))
    #The model trained gives the final centroids.
    #The final centers are used for evaluating clustering.
    # Evaluate clustering by computing Within Set Sum of Squared Errors
    def error(point):
        center = model.centers[model.predict(point)]
        return sqrt(sum([x**2 for x in (point - center)]))

    WSSSE = rddLoc.map(lambda point: error(point)).reduce(lambda x, y: x + y)
    arr.append(WSSSE)
print("Within Set Sum of Squared Error = ")
print(arr)
#Plot the graph for array returned and corresponding K values. The optimum value of k is where there is an elbow in the curve.
#The K value we got is 60. 

sc.stop()
