# Repository: 2017-09.project-2.template
# Assignment #2: Recommender Systems 

> Course: **[CS 1656 - Introduction to Data Science](http://cs1656.org)** (CS 2056) -- Fall 2017    
> Instructor: [Alexandros Labrinidis](http://labrinidis.cs.pitt.edu)  
> 
> Assignment: #2.  
> Released: October 5, 2017  
> **Due:      October 23, 2017**

### Description
This is the **second assignment** for the CS 1656 -- Introduction to Data Science (CS 2056) class, for the Fall 2017 semester.

### Goal
The goal of this assignment is to familiarize you with simple recommender systems (i.e., collaborative filtering algorithms).


### What to do -- pittrecsys.py
You are asked to write a Python program, called `pittrecsys.py` that will:
1. provide movie recommendations (i.e., predict ratings for a specific user-movie combination, given other ratings) and   
1. evaluate the performance of different recommendation algorithms using a combination of training and test data.


You program should be invoked as:
```
python3 pittrecsys.py command optional_arguments
```
There are two possible options for _command_ and multiple options for _optional_arguments_; these are specified next.

### (1) pittrecsys.py predict TrainingFile K Algorithm UserID MovieID  
This command will use simple user-based collaborative filtering to predict the rating of user userID for movie movieID, with the following parameters: 
* **TrainingFile** is the training data file (see next section for more information on DataSets)  
* **K** means that the algorithm should consider only the K nearest (most similar) users to user **UserID**. Note that a value of K=0 means that there is no limit and all the users should be considered.  
* **UserID** is the user for whom we want to predict their rating for **MovieID**   
* **Algorithm** is the specific algorithm used, which can be one of the following:  
	* **average**, just computing the average rating for MovieID based on all other ratings for that movie (K is effectively set to 0 for this, regardless of user input)  
	* **euclid**, when using Euclidean distance to measure user-user similarity and then use the nearest K users to UserID to predict his/her rating for MovieID (through a simple weighted average, where the similarities are the weights)  
	* **pearson**, when using Pearson Similarity to measure user-user similarity and then use the nearest K users to UserID to predict his/her rating for MovieID (through a simple weighted average, where the similarities are the weights). You should use the Pearson function provided in thr `scipy.stats` module:  https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html  
	* **cosine**, when using Cosine Similarity to measure user-user similarity and then use the nearest K users to UserID to predict his/her rating for MovieID (through a simple weighted average, where the similarities are the weights). 

For example:  
`python3 pittrecsys.py predict train.data 20 euclid 101 62` 
should use train.data and predict the rating of user 101 for movie 62 using the euclidean distance metric for user-user similarity, while only considering the 20 most similar users to user 101.

The output format of your program should be as follows:
```
pittrecsys.command    = predict
pittrecsys.training   = train.data
pittrecsys.algorithm  = euclid
pittrecsys.k          = 20
pittrecsys.userID     = 101
pittrecsys.movieID    = 62
pittrecsys.prediction = 3.34
```

Please note that the predicted rating shown above is just for formatting purposes only and that you should show all available decimal points.

Also, you should show an error message in case the userID or movieID are invalid, the training data file is not readable, the provided algorithm does not match one of the four specified, and K is not a positive integer.


### (2) pittrecsys.py evaluate TrainingFile K Algorithm TestingFile  
This command will use simple user-based collaborative filtering to evaluate the performance of the specified algorithm, with the following parameters: 
* **TrainingFile** is the training data file  
* **K** means that the algorithm should consider only the K nearest (most similar) users to user **UserID**. Note that a value of K=0 means that there is no limit and all the users should be considered.    
* **TestingFile** is the testing data file    
* **Algorithm** is the specific algorithm used, which can be one of the following:  
	* **average**, just computing the average rating for MovieID based on all other ratings for that movie (K is effectively set to 0 for this, regardless of user input)  
	* **euclid**, when using Euclidean distance to measure user-user similarity and then use the nearest K users to UserID to predict his/her rating for MovieID (through a simple weighted average, where the similarities are the weights)  
	* **pearson**, when using Pearson Similarity to measure user-user similarity and then use the nearest K users to UserID to predict his/her rating for MovieID (through a simple weighted average, where the similarities are the weights). You should use the Pearson function provided in the `scipy.stats` module:   https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html  
	* **cosine**, when using Cosine Similarity to measure user-user similarity and then use the nearest K users to UserID to predict his/her rating for MovieID (through a simple weighted average, where the similarities are the weights).   

For example:  
`python3 pittrecsys.py evaluate train.data 20 pearson test.data` 
should use train.data for training the user-user collaborative filtering algorithm, and then try to predict the test.data UserID/MovieID pairs and compare the predictions to the corresponding ratings in the test.data file. Your program should aggregate these differences by computing the Root Mean Squared Error (RMSE) and reporting that number.

The output format of your program should be as follows:
```
pittrecsys.command    = evaluate
pittrecsys.training   = train.data
pittrecsys.testing    = test.data
pittrecsys.algorithm  = pearson
pittrecsys.k          = 20
pittrecsys.RMSE       = 1234.1234
```

Please note that the RMSE shown above is just for formatting purposes only and that you should show all available decimal points.

Also, you should show an error message in cas the training or testing data file is not readable, the provided algorithm does not match one of the four specified, and K is not a positive integer.

### Datasets
We will use the [MovieLens Data](https://grouplens.org/datasets/movielens/) and in particular we will use the 100K dataset which we make available locally, as part of this repository. This has 100,000 movie ratings (1-5) from 943 users on 1,682 movies. We will test your programs using a variant of these datasets. You are encouraged to use smaller datasets for testing, especially in the beginning.


### Important notes about grading
It is absolutely imperative that your python program:  
* runs without any syntax or other errors (using Python 3)  
* strictly adheres to the format specifications for input and output, as explained above.     

Failure in any of the above will result in **severe** point loss. 


### Allowed Python Libraries (Updated)
You are allowed to use the following Python libraries (although a fraction of these will actually be needed):
```
argparse
collections
csv
json
glob
math 
os
pandas
re
requests
scipy.stats
sklearn.metrics
string
sys
time
xml
```
If you would like to use any other libraries, you must ask permission by Friday, September 15, 2017, using [piazza](http://piazza.cs1656.org).


### About your github account
It is very important that:  
* Your github account can do **private** repositories. If this is not already enabled, you can do it by visiting <https://education.github.com/>  
* You use the same github account for the duration of the course  
* You use the github account that you specified during the test assignment (i.e., this one)  

### How to submit your assignment
For this assignment, you must use the repository that was created for you after visiting the classroom link. You need to update the repository to include file `wheresmybus.py` as described above, and other files that are needed for running your program. You need to make sure to commit your code to the repository provided. We will clone all repositories shortly after midnight:  
* the day of the deadline **Monday, October 23rd, 2017 (i.e., at 12:15am, Tuesday, October 24th, 2017)**  
* 24 hours later (for submissions that are one day late / -5 points), and  
* 48 hours after the first deadline (for submissions that are two days late / -15 points). 

Our assumption is that everybody will submit on the first deadline. If you want us to consider a late submission, you need to email us at `cs1656-staff@cs.pitt.edu`
