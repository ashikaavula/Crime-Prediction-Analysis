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
	 ssh -X dsba-hadoop.uncc.edu -l <username>
	 ssh -X dsba-hadoop.uncc.edu -l aavula


--Put the files related to calculate k-value in dsba hadoop cluster from virtual machine.
	scp -v -r <path of file in virtual machine> <username>@dsba-hadoop.uncc.edu:<path to place file in cluster>
	scp -v -r /home/cloudera/cloud_project/kFromElbowMethod.py aavula@dsba-hadoop.uncc.edu:/users/aavula/project
	scp -v -r /home/cloudera/cloud_project/Chicago_Crimes_2008_to_2010.csv aavula@dsba-hadoop.uncc.edu:~/project
	(or)
	scp -v -r /home/cloudera/cloud_project/* aavula@dsba-hadoop.uncc.edu:~/project (this command moves all the files in folder to cluster)

--Now put input file in hdfs from cluster.
	hadoop fs -put /users/aavula/project/Chicago_Crimes_2008_to_2010.csv /user/aavula/input	

--Next run kFromElbowMethod.py using following command.
	spark-submit <program name or full path of that program> <inputdatafile path>
	spark-submit /users/aavula/project/kFromElbowMethod.py /user/aavula/input/Chicago_Crimes_updated.csv
--The output is printed as array of values in the command line itself. Those can be used for plotting graph.	
----------------------------------------------------------------------------------------------------------------------------------------------------------------
2)K means Clustering:

--Put the files related to calculate k-means clustering in dsba hadoop cluster from virtual machine.
	scp -v -r <path of file in virtual machine> <username>@dsba-hadoop.uncc.edu:<path to place file in cluster>
	scp -v -r /home/cloudera/cloud_project/kmeansClustering.py aavula@dsba-hadoop.uncc.edu:/users/aavula/project
	(or)
	scp -v -r /home/cloudera/cloud_project/* aavula@dsba-hadoop.uncc.edu:~/project (this command moves all the files in folder to cluster)

--The input file is same as above(Chicago_Crimes_2008_to_2010.csv).	

--Next run kmeansClustering.py using following command.
	spark-submit <program name or full path of that program> <inputdatafile path>
	spark-submit /users/aavula/project/kmeansClustering.py /user/aavula/input/Chicago_Crimes_updated.csv	

--The output is written to folder named kmeansOutput. We can move from hdfs to local folder of dsba hadoop cluster using the following command:
	hadoop fs -get /user/aavula/kmeansOutput/ /users/aavula/CrimeLocClusterOutput/
--The whole folder "kmeansOutput" is moved to local folder.
--Now move that into local machine using following command.
	scp <username>@dsba-hadoop.uncc.edu:/users/<username>/outputfile .
	scp aavula@dsba-hadoop.uncc.edu:/users/aavula/CrimeLocClusterOutput/kmeansOutput/* .
        
--The output of K-means is written to multiple files but in the same order as given input.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
3)Preprocessing data for Naive Bayes:

--Put the files related to Naive Bayes preprocessing in dsba hadoop cluster from virtual machine.
	scp -v -r <path of file in virtual machine> <username>@dsba-hadoop.uncc.edu:<path to place file in cluster>
	scp -v -r /home/cloudera/cloud_project/processedDataNB.py aavula@dsba-hadoop.uncc.edu:/users/aavula/project
	(or)
	scp -v -r /home/cloudera/cloud_project/* aavula@dsba-hadoop.uncc.edu:~/project (this command moves all the files in folder to cluster)

--The input file is same as above(Chicago_Crimes_2008_to_2010.csv).	

--Next run processedDataNB.py using following command.
	spark-submit <program name or full path of that program> <inputdatafile path>
	spark-submit /users/aavula/project/processedDataNB.py /user/aavula/input/Chicago_Crimes_updated.csv	

--The output is written to folder named kmeansOutput. We can move from hdfs to local folder of dsba hadoop cluster using the following command:
	hadoop fs -get /user/aavula/processedOutput/ /users/aavula/CrimeLocClusterOutput/
--The whole folder "processedOutput" is moved to local folder.
--Now move that into local machine using following command.
	scp <username>@dsba-hadoop.uncc.edu:/users/<username>/outputfile .
	scp aavula@dsba-hadoop.uncc.edu:/users/aavula/CrimeLocClusterOutput/processedOutput/* .

--This returns the filtered values.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
4)Naive Bayes:

--The output from kmeans clustering and naive bayes preprocessing are merged and given as input.

--Put the files related to Naive Bayes in dsba hadoop cluster from virtual machine.
	scp -v -r <path of file in virtual machine> <username>@dsba-hadoop.uncc.edu:<path to place file in cluster>
	scp -v -r /home/cloudera/cloud_project/NaiveBayes.py aavula@dsba-hadoop.uncc.edu:/users/aavula/project
	scp -v -r /home/cloudera/cloud_project/NBinput-part-00000.csv aavula@dsba-hadoop.uncc.edu:/users/aavula/project
	scp -v -r /home/cloudera/cloud_project/NBinput-part-00001.csv aavula@dsba-hadoop.uncc.edu:/users/aavula/project
	(or)
	scp -v -r /home/cloudera/cloud_project/* aavula@dsba-hadoop.uncc.edu:~/project (this command moves all the files in folder to cluster)

--Put the input files in hdfs from cluster. 	
	hadoop fs -put /users/aavula/project/NBinput-part-00000.csv /user/aavula/input
	hadoop fs -put /users/aavula/project/NBinput-part-00001.csv /user/aavula/input

--Next run NaiveBayes.py using following command.
	spark-submit <program name or full path of that program> <CrimeType>
	spark-submit /users/aavula/project/NaiveBayes.py HOMICIDE 

--The output is printed in the command line itself. We get the probabilities in descending order for the top 10 clusters.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------



