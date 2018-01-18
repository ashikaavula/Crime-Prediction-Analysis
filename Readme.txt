Link for the project : https://webpages.uncc.edu/gjanapar/CloudProject.html

We have implemented the following algorithms on the Chicago Crime data for the years 2008 to 2010. All algorithms are implemented in pyspark.
Since the file is read as comma seperated values, we have to remove commas if there are any inside each column data.
In our data, Description and Location Description columns have those type of values. So remove commas by finding and replacing them with space in excel.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
1)K-value from elbow method:

Initially for calculating the K value in kmeans clustering we used "Within Set Sum of Squared Error" method.
In this method we plot the output error values and see where the elbow is and k-value at elbow is the final k-value.

The following are the commands used:

--Connect to cluster.
	 ssh -X <cluster-link> -l <username>
	
--Put the files related to calculate k-value in dsba hadoop cluster from virtual machine.
	scp -v -r <path of file in virtual machine> <username>@<cluster-link>:<path to place file in cluster>
	
--Now put input file in hdfs from cluster.
	hadoop fs -put <input file path in local system> <hdfs input path>	

--Next run kFromElbowMethod.py using following command.
	spark-submit <program name or full path of that program> <inputdatafile path>
	
--The output is printed as array of values in the command line itself. Those can be used for plotting graph.	
----------------------------------------------------------------------------------------------------------------------------------------------------------------
2)K means Clustering:

--Put the files related to calculate k-means clustering in dsba hadoop cluster from virtual machine.
	scp -v -r <path of file in virtual machine> <username>@<cluster-link>:<path to place file in cluster>
	
--The input file is same as above(Chicago_Crimes_2008_to_2010.csv).	

--Next run kmeansClustering.py using following command.
	spark-submit <program name or full path of that program> <inputdatafile path>

--The output is written to folder named kmeansOutput. We can move from hdfs to local folder of dsba hadoop cluster using the following command:
	hadoop fs -get <hdfs output path> <path to store the output file in cluster>
--The whole folder is moved to local folder.
--Now move that into local machine using following command.
	scp <username>@<cluster-link>: <file path in cluster>
	
--The output of K-means is written to multiple files but in the same order as given input.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
3)Preprocessing data for Naive Bayes:

--Put the files related to Naive Bayes preprocessing in dsba hadoop cluster from virtual machine.
	scp -v -r <path of file in virtual machine> <username>@<cluster-link>:<path to place file in cluster>

--The input file is same as above(Chicago_Crimes_2008_to_2010.csv).	

--Next run processedDataNB.py using following command.
	spark-submit <program name or full path of that program> <inputdatafile path>
	
--The output is written to folder named kmeansOutput. We can move from hdfs to local folder of dsba hadoop cluster using the following command:
	hadoop fs -get <hdfs output path> <path to store the output file in cluster>
--The whole folder is moved to local folder.
--Now move that into local machine using following command.
	scp <username>@<cluster-link>:<file path in cluster>
	

--This returns the filtered values.
----------------------------------------------------------------------------------------------------------------------------------------

4)Naive Bayes:

--The output from kmeans clustering and naive bayes preprocessing are merged and given as input.

--Put the files related to Naive Bayes in dsba hadoop cluster from virtual machine.
	scp -v -r <path of file in virtual machine> <username>@<cluster-link>:<path to place file in cluster>

--Put the input files in hdfs from cluster. 	
	hadoop fs -put <input file path in local system> <hdfs input path>
	
--Next run NaiveBayes.py using following command.
	spark-submit <program name or full path of that program> <CrimeType>

--The output is printed in the command line itself. We get the probabilities in descending order for the top 10 clusters.




