import sys
import os
import numpy as np
import pandas
import scipy.stats
import math

import warnings
warnings.filterwarnings("ignore") # Ignore all warnings from the pandas library

def normalize_rating(rating):
    return (2.0*(rating - 1.0) - 4.0) / 4.0 # Move the rating scale from 1.0 through 5.0 to -1.0 through +1.0

def denormalize_rating(rating):
    return 0.5 * ((rating + 1.0) * 4) + 1 # Move the rating scale from -1.0 through +1.0 to 1.0 through 5.0

def calc_average_rating(training_file, movie_id): # Given a movie id, calculate the average rating
    data = []
    ratings_sum = 0.0
    num_ratings = 0.0

    if movie_id < 0 or movie_id > 1682: # Movie ID is out of bounds
        print("Invalid movie ID")
        print

    column_names = ['users', 'movies', 'ratings', 'times']
    data = pandas.read_table(filepath_or_buffer = training_file, delimiter = '\t', names = column_names)
    for row in data[data['movies'] == movie_id].iterrows():
        rating = row[1].loc['ratings']
        ratings_sum += float(rating)
        num_ratings += 1.0
    if num_ratings > 0:
        prediction = ratings_sum/num_ratings
        return prediction
    else:
        return None

def calc_euclidian_rating(our_user_ratings, curr_user_ratings): # Given a user's ratings, calculate their distance to every other user based on their ratings on every other movie
    distance = None
    for rating in curr_user_ratings.iterrows():
        curr_movie_id = rating[1].loc['movies']
        curr_user_id = rating[1].loc['users']
        curr_rating = rating[1].loc['ratings']
        if curr_movie_id in our_user_ratings:
            if distance is None:
                distance = (curr_rating - our_user_ratings[curr_movie_id])**2
            else:
                distance += (curr_rating - our_user_ratings[curr_movie_id])**2
    return distance

def calc_pearson_rating(our_user_ratings, curr_user_ratings):
    scatter_plot_x = [] # Hold our user's ratings
    scatter_plot_y = [] # Hold the current user's ratings
    for rating in curr_user_ratings.iterrows():
        curr_movie_id = rating[1].loc['movies']
        curr_user_id = rating[1].loc['users']
        curr_rating = rating[1].loc['ratings']

        if curr_movie_id in our_user_ratings:
            scatter_plot_x.append(our_user_ratings[curr_movie_id])
            scatter_plot_y.append(curr_rating)
    correlation = scipy.stats.pearsonr(scatter_plot_x, scatter_plot_y)[0] # Calculate the correlation between the two users
    if math.isnan(correlation): # We can't calculate the correlation
        return None
    else:
        return correlation

def calc_cosine_rating(our_user_ratings, curr_user_ratings): # Calculate cosine similarity between a user and all other users
    numerator = 0.0 # Numerator of the cosine similarity equation
    our_user_vector_magnitude = 0.0
    curr_user_vector_magnitude = 0.0
    for rating in curr_user_ratings.iterrows():
        curr_movie_id = rating[1].loc['movies']
        curr_user_id = rating[1].loc['users']
        curr_rating = rating[1].loc['ratings']

        if curr_movie_id in our_user_ratings: # Our user has rated the movie; we can compare!
            numerator += (curr_rating * our_user_ratings[curr_movie_id])
            our_user_vector_magnitude += our_user_ratings[curr_movie_id]**2
            curr_user_vector_magnitude += curr_rating**2
    our_user_vector_magnitude = math.sqrt(our_user_vector_magnitude) # Magnitude of the user's vector in the denominator
    curr_user_vector_magnitude = math.sqrt(curr_user_vector_magnitude) # Magnitude of the other user's vector in the denominator
    denominator = our_user_vector_magnitude + curr_user_vector_magnitude # Denominator of the cosine similarity function
    if denominator > 0.0:
        cosine_similarity = numerator / denominator # Calculate the correlation between the two users
        return cosine_similarity
    else:
        return None

def calc_rating(algorithm, training_file, k, user_id, movie_id): # General purpose rating calculation
    users = {}
    column_names = ['users', 'movies', 'ratings', 'times']
    data = pandas.read_table(filepath_or_buffer = training_file, delimiter = '\t', names = column_names)

    users = data['users'].unique() # Find all the unique user ids
    our_user_ratings = {} # Keep track of our user's ratings
    user_similiarities = {} # Keep track of each user's similarity to our user

    for row in data[data['users'] == user_id].iterrows(): # Gather all the ratings of our user
        rating_movie_id = row[1].loc['movies']
        rating_value = row[1].loc['ratings']
        our_user_ratings[rating_movie_id] = rating_value

    if len(our_user_ratings) == 0 or movie_id < 0 or movie_id > 1682 or user_id < 0 or user_id > 943: # User ID or movie ID are invalid
        print("Invalid movie ID or user ID!")
        return

    for user in users: # For each user, compute the similarity to our user based on the input algorithm
        if user == user_id: # Don't compute the similarity of our user against themself
            pass
        curr_user_ratings = data[data['users'] == user] # Find all the movie ratings of the current user
        if algorithm == "euclid":
            distance = calc_euclidian_rating(our_user_ratings, curr_user_ratings) # Calculate distance between the users for every movie
            if not distance == None: # Valid distance
                user_similiarities[user] = distance
        elif algorithm == "pearson":
            correlation = calc_pearson_rating(our_user_ratings, curr_user_ratings) # Calculate the correlation between the users
            if not correlation == None:
                user_similiarities[user] = correlation
        elif algorithm == "cosine":
            cosine_similarity = calc_cosine_rating(our_user_ratings, curr_user_ratings) # Calculate the cosine similarity between the users' ratings
            if not cosine_similarity == None:
                user_similiarities[user] = cosine_similarity # Calculate the correlation between the two users

    i = 0 # Number of users we have seen so far
    weighted_sum = 0.0
    weights = 0.0
    for key, value in sorted(user_similiarities.items(), key = lambda pair: pair[1], reverse=True): # Sort users by similarity and choose k most similar
        if i >= k and k > 0: # We have read in the k nearest neighbors and k is not 0 (if k = 0, we take into account all users)
            break
        i_user_movie_rating = data.loc[(data['users'] == key) & (data['movies'] == int(movie_id))] # Find this user's movie rating for our specified movie to predict
        if len(i_user_movie_rating.index) == 0: # That user did not rate the movie
            pass
        else:
            for row in i_user_movie_rating.iterrows(): # Should only be one row
                if algorithm == "euclid":
                    weight = 1.0/(1.0 + value) # Compute similarity
                    weighted_sum += weight * row[1].loc['ratings']
                    weights += weight
                elif algorithm == "pearson":
                    weighted_sum += value * normalize_rating(row[1].loc['ratings']) # Multiply the correlation values by the ratings
                    weights += abs(value)
                elif algorithm == "cosine":
                    weighted_sum += value * row[1].loc['ratings'] # Multiply the cosine similarity by the ratings
                    weights += value
        i += 1 # We've finished seeing this person and taken them into account
    if weights == 0.0:
        prediction = 3.0 # None of the k nearest neighbors rated the movie; default prediction is 3.0 as Prof. Labrinidis has stated on Piazza
        return prediction
    else:
        prediction = weighted_sum / weights
        if algorithm == "pearson":
            prediction = denormalize_rating(prediction)
        return prediction

def predict(args):
    if not len(args) == 5:
        print("Not enough arguments for predict! Returning...")
        return
    training_file = args[0]
    k = int(args[1])
    algorithm = args[2].lower()
    user_id = int(args[3])
    movie_id = int(args[4])
    prediction = None
    if not algorithm in ["average", "euclid", "pearson", "cosine"]:
        print("Not a valid algorithm!")
        return
    elif k < 0:
        print("Not a valid k value!")
        return
    elif not os.path.exists(training_file):
        print("That training file doesn't exist!")
        return

    if algorithm == "average":
        prediction = calc_average_rating(training_file, movie_id)
    elif algorithm == "euclid":
        prediction = calc_rating(algorithm, training_file, k, user_id, movie_id)
    elif algorithm == "pearson":
        prediction = calc_rating(algorithm, training_file, k, user_id, movie_id)
    elif algorithm == "cosine":
        prediction = calc_rating(algorithm, training_file, k, user_id, movie_id)

    print("pittrecsys.command    = predict\npittrecsys.training   = " + training_file + "\npittrecsys.algorithm  = " + algorithm + "\npittrecsys.k          = " + str(k) + "\npittrecsys.userID     = " + str(user_id) + "\npittrecsys.movieID    = " + str(movie_id) + "\npittrecsys.prediction = " + str(prediction))

def evaluate(args):
    if not len(args) == 4:
        print("Not enough arguments for evaluate! Returning...")
        return
    training_file = args[0]
    k = int(args[1])
    algorithm = args[2].lower()
    testing_file = args[3]
    if not algorithm in ["average", "euclid", "pearson", "cosine"]:
        print("Not a valid algorithm!")
        return
    elif k < 0:
        print("Not a valid k value!")
        return
    elif not os.path.exists(training_file) or not os.path.exists(testing_file):
        print("That training file or testing file doesn't exist!")
        return

    column_names = ['users', 'movies', 'ratings', 'times']
    data = pandas.read_table(filepath_or_buffer = testing_file, delimiter = '\t', names = column_names)
    error = 0.0
    num_ratings = 0
    for row in data.iterrows(): # Make a prediction for each line in the data table
        user_id = row[1].loc['users']
        movie_id = row[1].loc['movies']
        rating = row[1].loc['ratings']

        prediction = None
        if algorithm == "average":
            prediction = calc_average_rating(training_file, movie_id)
        elif algorithm == "euclid":
            prediction = calc_rating(algorithm, training_file, k, user_id, movie_id)
        elif algorithm == "pearson":
            prediction = calc_rating(algorithm, training_file, k, user_id, movie_id)
        elif algorithm == "cosine":
            prediction = calc_rating(algorithm, training_file, k, user_id, movie_id)

        if not prediction == None:
            error += (prediction - rating)**2
            num_ratings += 1
    if num_ratings > 0:
        error = math.sqrt(error / num_ratings) # Calculate RMSE = square root of MSE = sum of differences between prediction and actual value divided by number of predictions
        print("pittrecsys.command    = evaluate\npittrecsys.training   = " + training_file + "\npittrecsys.testing    = " + testing_file + "\npittrecsys.algorithm  = " + algorithm + "\npittrecsys.k          = " + str(k) + "\npittrecsys.RMSE       = " + str(error))
    else:
        print("ERROR: No predictions were made!")

if not len(sys.argv) == 6 and not len(sys.argv) == 7:
    print("Incorrect number of arguments!")

command = sys.argv[1].lower()
if command == "predict":
    predict(sys.argv[2:])
elif command == "evaluate":
    evaluate(sys.argv[2:])
else:
    print("Invalid command!")
