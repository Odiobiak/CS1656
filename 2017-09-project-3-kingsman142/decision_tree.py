import sys
import pandas as pd
import csv
import os

def read_tree(tree_input): # Read the actual tree text from file
    with open(tree_input) as tree_file:
        lines = tree_file.readlines()
        lines = [x.rstrip() for x in lines if x.rstrip()] # Remove newline characters
    return lines

def parse_line(line): # Given a line in the tree, parse its information (depth in tree, feature, value, category, category count)
    tokens = line.split(" ")
    tokens = [x for x in tokens if x]
    num_pipes = tokens.count("|") # The number of pipes indicates the depth
    feature = tokens[num_pipes]
    feature_value = tokens[num_pipes+1].strip(":")
    category = None # Final classification category
    category_count = -1
    if ( len(tokens) - num_pipes ) == 4: # We reached a classification
        category = tokens[num_pipes+2]
        category_count_token = tokens[num_pipes+3]
        category_count = int(category_count_token[1:len(category_count_token)-1]) # Grab the number, or count, within the two parentheses at the front and end
    return (num_pipes, feature, feature_value, category, category_count) # depth, feature, feature label, end category outcome if one exists, and count

def form_tree(tree_text): # Form the tree in a dictionary data structure
    tree = {}
    first_level = (None, None) # Keep track of the path that we've travelled down in the tree for the first traversal
    second_level = (None, None) # Keep track of the path that we've travelled down in the tree for the first traversal
    possible_decisions = set([]) # All possible classifications in the tree (e.g. "good" and "bad")
    for line in tree_text:
        depth, feature, feature_value, category, category_count = parse_line(line) # Grab this line's information
        if depth == 0:
            if not feature in tree:
                tree[feature] = {}
                tree[feature][feature_value] = {}
            else:
                if not feature_value in tree[feature]:
                    tree[feature][feature_value] = {}

            if not category is None:
                tree[feature][feature_value][category] = 0 # Number of occurrences, initialize to 0
                possible_decisions.add(category) # Found a new category!

            first_level = (feature, feature_value)
            second_level = (None, None) # Reset just in case we went back up the decision tree rather than down
        elif depth == 1:
            first_level_feature = first_level[0]
            first_level_value = first_level[1]
            if not feature in tree[first_level_feature][first_level_value]:
                tree[first_level_feature][first_level_value][feature] = {}
                tree[first_level_feature][first_level_value][feature][feature_value] = {}
            else:
                if not feature_value in tree[first_level_feature][first_level_value][feature]:
                    tree[first_level_feature][first_level_value][feature][feature_value] = {}

            if not category is None:
                tree[first_level_feature][first_level_value][feature][feature_value][category] = 0 # Number of occurrences, initialize to 0
                possible_decisions.add(category) # Found a new category!

            second_level = (feature, feature_value)
        else: # depth must be 2 (0-based, so we're at level 3)
            first_level_feature = first_level[0]
            first_level_value = first_level[1]
            second_level_feature = second_level[0]
            second_level_value = second_level[1]

            if not feature in tree[first_level_feature][first_level_value][second_level_feature][second_level_value]:
                tree[first_level_feature][first_level_value][second_level_feature][second_level_value][feature] = {}
                tree[first_level_feature][first_level_value][second_level_feature][second_level_value][feature][feature_value] = {}
            else:
                if not feature_value in tree[first_level_feature][first_level_value][second_level_feature][second_level_value][feature]:
                    tree[first_level_feature][first_level_value][second_level_feature][second_level_value][feature][feature_value] = {}

            if not category is None:
                tree[first_level_feature][first_level_value][second_level_feature][second_level_value][feature][feature_value][category] = 0 # Number of occurrences, initialize to 0
                possible_decisions.add(category) # Found a new category!

    tree["UNMATCHED"] = 0 # Important category to keep track of; everything else goes into UNMATCHED
    return (tree, possible_decisions)

def test_tree(tree, data_file, possible_decisions):
    with open(data_file) as test_data: # Grab the test data
        data = pd.read_csv(data_file)
        data.columns = [column.strip(' "') for column in data.columns] # For all the column names, just make sure it's clean data; strip the quotes and spaces

    column_names = data.columns
    original_tree = tree # For each line in the test file, we'll return back to the root of the original tree to traverse down
    for index, row in data.iterrows(): # Iterate through all the rows in the test data set and "test" each one
        path = []
        for i in range(0, 3): # Our decision tree can have a maximum of 3 levels of traversal
            for column in column_names:
                if column in tree: # Check if we can navigate down the decision tree with this column
                    column_val = row[column].strip(' \'"') # Get the column's subtree
                    if column_val in tree[column]: # Check to make sure if the subtree is even in the tree or not
                        tree = tree[column][column_val] # It is, so let's iteratively navigate there

        # Try to increment the number of occurrences of this test data's information in the tree if we can actually classify it
        found_decision = False
        for decision in possible_decisions: # Check if we can possibly make a decision given our data
            if decision in tree:
                tree[decision] += 1
                found_decision = True
                path.append(("decision", decision))
        if not found_decision:
            original_tree["UNMATCHED"] += 1

        tree = original_tree # Reset our tree so the next test row can start from the top/root

    return original_tree

def print_trained_tree(tree_text, tree, possible_decisions): # Once we've trained it and classified everything, print out the occurrences of each class in each subtree
    # This method is similar to the form_tree method since we have to keep track of where we're at in each level of the tree with first_level and second_level
    first_level = (None, None)
    second_level = (None, None)
    for line in tree_text:
        depth, feature, feature_value, category, category_count = parse_line(line)
        if depth == 0:
            subtree = tree[feature][feature_value]

            found_decision = False
            for decision in possible_decisions:
                if decision in subtree:
                    print(feature + " " + str(feature_value) + ": " + decision + " (" + str(subtree[decision]) + ")") # Found a decision in this tree, print out the counts
                    found_decision = True
            if not found_decision:
                print(feature + " " + str(feature_value)) # Just found a feature to split data on

            first_level = (feature, feature_value)
            second_level = (None, None) # Reset just in case we went back up the decision tree rather than down
        elif depth == 1:
            first_level_feature = first_level[0]
            first_level_value = first_level[1]

            subtree = tree[first_level_feature][first_level_value][feature][feature_value]

            found_decision = False
            for decision in possible_decisions:
                if decision in subtree:
                    print("|   " + feature + " " + str(feature_value) + ": " + decision + " (" + str(subtree[decision]) + ")") # Found a decision in this tree, print out the counts
                    found_decision = True
            if not found_decision:
                print("|   " + feature + " " + str(feature_value)) # Just found a feature to split data on

            second_level = (feature, feature_value)
        else: # depth must be 2 (level 3 in the tree since depth is 0-based)
            first_level_feature = first_level[0]
            first_level_value = first_level[1]
            second_level_feature = second_level[0]
            second_level_value = second_level[1]

            subtree = tree[first_level_feature][first_level_value][second_level_feature][second_level_value][feature][feature_value]

            found_decision = False
            for decision in possible_decisions:
                if decision in subtree:
                    print("|   |   " + feature + " " + str(feature_value) + ": " + decision + " (" + str(subtree[decision]) + ")") # Found a decision in this tree, print out the counts
                    found_decision = True
            if not found_decision:
                print("|   |   " + feature + " " + str(feature_value)) # Just found a feature to split data on

    unmatched_val = tree["UNMATCHED"]
    if unmatched_val > 0: # Only print the unmatched results if there's at least 1
        print("UNMATCHED: " + str(tree["UNMATCHED"]))

    return tree_text

if not len(sys.argv) == 3:
    print("Invalid number of arguments!")
    sys.exit()
tree_input = sys.argv[1]
test_data = sys.argv[2]
if not os.path.exists(tree_input):
    print("Tree file doesn't exist!")
    sys.exit()
elif not os.path.exists(test_data):
    print("Test data doesn't exist!")
    sys.exit()

tree_text = read_tree(tree_input)
train_tree, possible_decisions = form_tree(tree_text)
test_tree = test_tree(train_tree, test_data, possible_decisions)
print_trained_tree(tree_text, test_tree, possible_decisions)
