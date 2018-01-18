
import sys
import numpy as np
from pyspark import SparkContext

if __name__ == "__main__":
  if len(sys.argv) !=2:
    print >> sys.stderr, "spark-submit NaiveBayes.py <crimeType>"
    exit(-1)

  sc = SparkContext(appName="Naive Bayes")

  # For Naive Bayes the outputs from kmeans clustering and processedDataNB.py are merged and given as input.
  # The input for Naive Bayes contains fields: crimetype, clusternumber, location.
  input = sc.textFile("input/NBinput-part-00000.csv,input/NBinput-part-00001.csv")

  rddInitial = input.map(lambda line: line.split(','))
  
  #getting count of total rows
  rowCount = rddInitial.count()

  #The crime type given in command line is passed into CrimeType
  CrimeType = sys.argv[1]

  #Filtering the rows which contain specified crime type
  rddcrimeType=rddInitial.filter(lambda line: line[0]==CrimeType)

  #Counting the crime type occurences in a cluster by using <K,V> pair and reducing them
  rddCount = rddcrimeType.map(lambda line: (line[1],1))
  rddReduce = rddCount.reduceByKey(lambda a,b: a+b)
 
  #Counting the occurences for different crimes in cluster by using <K,V> pair.  
  rddOcurrences = rddInitial.map(lambda line: (line[1],1))
  locationDict = rddOcurrences.countByKey()

  #calculating the posterior probability:  
  rddFinal = rddReduce.map(lambda line: ((float(line[1])/locationDict[line[0]])*(float(locationDict[line[0]])/rowCount),line[0]))

  #Printed in order of descending probabilities. 
  list = rddFinal.takeOrdered(10, key = lambda x: -x[0])
  
  #Printing the top 10 clusters in which the given crime type can occur in the form of list.
  for coeff in list:
    print coeff
  
  sc.stop()
