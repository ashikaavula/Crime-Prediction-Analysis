import sys
import numpy as np
from pyspark import SparkContext

sc = SparkContext(appName ="Preprocessing data for Naive Bayes")

#The input file is full chicago crimes dataset
input = sc.textFile(sys.argv[1])

#The first line is read into h 
h = input.first()

#We are filtering out the data by removing the header which contains headings
inputWithNoHeader = input.filter(lambda line : line!= h)  
rddInitial = inputWithNoHeader.map(lambda line: line.split(','))

#Deleting the rows in which location column is empty
rdd =  rddInitial.filter(lambda x: x[20] is not u'')

#The Primary type( i.e., crime type) column is retrieved from the whole data.
rddFinal = rdd.map(lambda line: (line[6]))

rddFinal.saveAsTextFile('processedOutput')
#save this to local system and convert it to .csv file

sc.stop()
