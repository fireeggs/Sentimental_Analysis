# 
# CSC401. Natural Language Computing 
#
# Assignemnt 1. 
# Part4. IBM Watson on BlueMix 
# Task: fill out all of the functions in this file following 
#       the specifications exactly. DO NOT modify the headers of any
#       functions. Doing so will cause your program to fail the autotester.
#
# main.py
# ibmTrain.py
#
# Created by Seungkyu Kim on Feb 16th, 2016 
# Copyright 2016 Seungkyu Kim All rights reserved.
#
#


import os
import requests
import json
import sys
import itertools

###HELPER FUNCTIONS##########################

def convert_training_csv_to_watson_csv_format(input_csv_name, group_id, output_csv_name):
    # Converts an existing training csv file. The output file should
    # contain only the 11,000 lines of your group's specific training set.
    #
    # Inputs:
    #	input_csv - a string containing the name of the original csv file
    #		ex. "my_file.csv"
    #
    #	output_csv - a string containing the name of the output csv file
    #		ex. "my_output_file.csv"
    #
    # Returns:
    #	None

    tweets = open(input_csv_name, "r")
    output = open(output_csv_name, "w")

    #lines = input.readlines()
    # training_data = lines[group_id * 5500: (group_id + 1) * 5500] + \
    # lines[800000 + group_id * 5500: 800000 + (group_id + 1) * 5500]
    class_range = [[group_id * 5500, ((group_id + 1) * 5500 - 1)],
                   [800000 + group_id * 5500, (800000 + (group_id + 1) * 5500 - 1)]]

    #for i in range(len(training_data)):
    #	temp = training_data[i].split(',"')
    #	tempTweet = '"' + temp[-1][:-2].strip() + '"' + ',' + temp[0][1:-1] + '\n'
    #	resTemp = tempTweet.replace("\t", "\\t")
    #	output_csv.write(resTemp.decode('utf-8','ignore').encode("utf-8"))

    for i in range(0, len(class_range)):

        #if i == 0:
        #    print "Class: 0 -- reading from " + \
        #          str(class_range[i][0]) + " " + str(class_range[i][1])
        #else:
        #   print "Class: 4 -- reading from " + \
        #         str(class_range[i][0]) + " " + str(class_range[i][1])

        for tweet in itertools.islice(tweets, class_range[i][0], class_range[i][1]):
            contents = tweet.split(",")
            info = contents[:5]
            text_tweet = tweet.split(info[4]+",")
            text_tweet = text_tweet[1][1:-2]

            output.write(text_tweet.rstrip() + "," + info[0][1] + "\n")
    return


def extract_subset_from_csv_file(input_csv_file, n_lines_to_extract, output_file_prefix='ibmTrain'):
    # Extracts n_lines_to_extract lines from a given csv file and writes them to
    # an outputfile named ibmTrain#.csv (where # is n_lines_to_extract).
    #
    # Inputs:
    #	input_csv - a string containing the name of the original csv file from which
    #		a subset of lines will be extracted
    #		ex. "my_file.csv"
    #
    #	n_lines_to_extract - the number of lines to extract from the csv_file, as an integer
    #		ex. 500
    #
    #	output_file_prefix - a prefix for the output csv file. If unspecified, output files
    #		are named 'ibmTrain#.csv', where # is the input parameter n_lines_to_extract.
    #		The csv must be in the "watson" 2-column format.
    #
    # Returns:
    #	None

	lines = open(input_csv_file, "r")
	output_csv = open(output_file_prefix + str(n_lines_to_extract) + ".csv", "w")

	count0 = 0
	count4 = 0

	for line in lines:
		if(line[-2] == "0" and count0 < n_lines_to_extract):		#class 0
			output_csv.write(line)
			count0 += 1
		elif(line[-2] == "4" and count4 < n_lines_to_extract):		#class 4
			output_csv.write(line)
			count4 += 1

		if (count0 + count4) == n_lines_to_extract * 2:				#no need to read All.
			break

	#print str(count0) + " / " + str(count4) + " ---- " + str(n_lines_to_extract)

	return


def create_classifier(username, password, n, input_file_prefix='ibmTrain'):
    # Creates a classifier using the NLClassifier service specified with username and password.
    # Training_data for the classifier provided using an existing csv file named
    # ibmTrain#.csv, where # is the input parameter n.
    #
    # Inputs:
    # 	username - username for the NLClassifier to be used, as a string
    #
    # 	password - password for the NLClassifier to be used, as a string
    #
    #	n - identification number for the input_file, as an integer
    #		ex. 500
    #
    #	input_file_prefix - a prefix for the input csv file, as a string.
    #		If unspecified data will be collected from an existing csv file
    #		named 'ibmTrain#.csv', where # is the input parameter n.
    #		The csv must be in the "watson" 2-column format.
    #
    # Returns:
    # 	A dictionary containing the response code of the classifier call, will all the fields
    #	specified at
    #	http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/natural-language-classifier/api/v1/?curl#create_classifier
    #
    #
    # Error Handling:
    #	This function should throw an exception if the create classifier call fails for any reason
    #	or if the input csv file does not exist or cannot be read.
    #

    input_file_name = input_file_prefix + str(n) + '.csv'
    nlclassifier_service_url = 'https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers'
    files = {
        'training_data': open(input_file_name, 'rb'),
        'training_metadata': "{\"language\":\"en\",\"name\":\"Classifier " + str(n) + "\"}"
    }
    r = requests.post(nlclassifier_service_url,
                      auth=(username, password),
                      # headers={'Content-Type': 'application/multi-part/form-data'},
                      files=files)

    print r.text

    #print "hello"
    #response_dict = json.loads(r.text)
    # if not 'status' in response_dict or response_dict['status'] in ['Training', 'Available']:
    #     if 'status_description' in response_dict:
    #         raise Exception(response_dict['status_description'])
    #     else:
    #         raise Exception(response_dict['description'])
    #print "hello"
    ##print r.text
    #if "error" in response_dict:
    #    errorMsg = response_dict['error'] + ": " + response_dict['description']
    #    raise Exception(errorMsg)
    #else:
    #    return r

if __name__ == "__main__":
    print("ibmTrain.py START")

    ### STEP 1: Convert csv file into two-field watson format
    input_csv_name = './training.1600000.processed.noemoticon.csv'
    # DO NOT CHANGE THE NAME OF THIS FILE
    output_csv_name = './training_11000_watson_style.csv'

    convert_training_csv_to_watson_csv_format(input_csv_name, 24, output_csv_name)

    ### STEP 2: Save 11 subsets in the new format into ibmTrain#.csv files

    # TODO: extract all 11 subsets and write the 11 new ibmTrain#.csv files
    #
    # you should make use of the following function call:
    #
    # n_lines_to_extract = 500
    # extract_subset_from_csv_file(input_csv,n_lines_to_extract)

    training_set_sizes = [500, 2500, 5000]
    for n_lines_to_extract in training_set_sizes:
        extract_subset_from_csv_file(output_csv_name, n_lines_to_extract)
        break

    ### STEP 3: Create the classifiers using Watson

    # TODO: Create all 11 classifiers using the csv files of the subsets produced in
    # STEP 2
    #
    #
    # you should make use of the following function call
    # n = 500
    
    username = "88b6e713-a722-4f94-b257-550dff421672"
    password = "2vQn2oh6E8zl"

    # create_classifier(username, password, n, input_file_prefix='ibmTrain')
    for n in training_set_sizes:
        create_classifier(username, password, n, input_file_prefix='ibmTrain')

    print("ibmTrain.py END")
