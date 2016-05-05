# 
# CSC401. Natural Language Computing 
#
# Assignemnt 1. 
# Part3. Classifying tweets using WEKA 
# Task: script, make 1 test and 9 train files from train.arff file(part2). 
#       Then calculate accuracy, precision, recall and p-value.
#       Write all calculated data to 3.4output.txt file!
#
# main.py
# create_script.py
#
# Created by Seungkyu Kim on Feb 13th, 2016 
# Copyright 2016 Seungkyu Kim All rights reserved.
#
#
# >$ ./python <input filename> <input filename>
# >$ python run_script.py <test.arff> <train.arff>


import sys
import math
import re
import linecache
import os
from scipy import stats


HEAD = "@relation tweet_classification\n\n\n\
@attribute 1st_person_pronouns numeric\n\
@attribute 2nd_person_pronouns numeric\n\
@attribute 3rd_person_pronouns numeric\n\
@attribute coor_conjunctions numeric\n\
@attribute past_verbs numeric\n\
@attribute future_verbs numeric\n\
@attribute commas numeric\n\
@attribute colon_and_semi numeric\n\
@attribute dashes numeric\n\
@attribute parentheses numeric\n\
@attribute ellipses numeric\n\
@attribute common_nouns numeric\n\
@attribute proper_nouns numeric\n\
@attribute adverbs numeric\n\
@attribute wh_words numeric\n\
@attribute modern_slang numeric\n\
@attribute words_all_upper numeric\n\
@attribute avg_sentences numeric\n\
@attribute avg_tokens numeric\n\
@attribute num_sentences numeric\n\
@attribute polarity {0,4}\n\n\n\
@data\n\
"
# part 3.1
def part_3_1(test,train):
    ''' classifiers 
    
    Build two arff files: one for all of the training and one for all of the testing data. Report classification
    accuracy on test data among support vector machines (SVMs), na¨ıve Bayes, and decision trees. Pipe the
    output of WEKA for the best classifier to the file 3.1output.txt. Use the best classification algorithm for
    the following questions unless instructed otherwise. 
    '''
    
    os.system("java -cp ./weka.jar weka.classifiers.trees.J48 -t " + "./" + test + " > 3.1output.txt")
    os.system("java -cp ./weka.jar weka.classifiers.trees.J48 -t " + "./" + train + " >> 3.1output.txt")

    return True
    
# part 3.2
def part_3_2(fname):
    ''' Amount of training data 
        
    Many researchers attribute the success of modern machine learning to the sheer volume of data that is
    now available. Modify the amount of data that is used to train your system in increments of 500, starting
    at 500 (i.e., n = 500, 1000, ..., 5500) and report the resulting accuracies in a table in 3.2output.txt. 
    '''

    # read line from actual data
    start_data = 28
    line = linecache.getline(fname, start_data).rstrip()
    
    # partition data
    partition_class0 = []
    partition_class4 = []
    
    max_count = 500
    count_class0 = 0
    count_class4 = 0
    
    partition_lines_class0 = ''
    partition_lines_class4 = ''
    
    i = 0
    #(i * max_count) < 5500
    while (line):
        if (count_class0 < max_count and line[-1] == "0"):
            partition_lines_class0 += line.strip() + "\n"
            count_class0 += 1
            if (count_class0 == max_count):
                count_class0 = 0
                partition_class0.append(partition_lines_class0)
                partition_lines_class0 = ""            
            start_data += 1
            line = linecache.getline(fname, start_data).rstrip() 
        elif (count_class4 < max_count and line[-1] == "4"):
            partition_lines_class4 += line.strip() + "\n"
            count_class4 += 1
            if (count_class4 == max_count):
                count_class4 = 0
                partition_class4.append(partition_lines_class4)
                partition_lines_class4 = ""            
            start_data += 1
            line = linecache.getline(fname, start_data).rstrip()
        else:
            print("shuoldn't reach here!! line is -> ", line)
            start_data += 1
            line = linecache.getline(fname, start_data).rstrip()
        i += 1
            
    # append lines that are less than maximum lines
    if (partition_lines_class0 != ""):
        partition_class0.append(partition_lines_class0)
    if (partition_lines_class4 != ""):
        partition_class4.append(partition_lines_class4)    
    
    trainings = ["","","","","","","","","","",""]
    # concatenate 500, 1000, 1500, ... 5500 lines from the chopped lines
    
    i = 0
    while(i < 11):
        j = 0
        trainings[i] += HEAD
        while (j <= i):
            trainings[i] += partition_class0[j] + partition_class4[j]
            j+=1
        writeFile("./partition/part3_2_partition" + str((i*500) + 500) + ".arff",trainings[i])
        i+=1
    
    i = 0
    for i in range(11):
        os.system("java -cp ./weka.jar weka.classifiers.trees.J48 -t ./partition/part3_2_partition" + str((i*500) + 500) + ".arff -o > ./partition/3.2output_" + str((i*500) + 500) + ".txt")
    
    result = ""
    result += "PART 3.2 output with weka.classifiers.trees.J48 algorithm \n\n"
    for i in range(11):
        # get accuracy line
        line = linecache.getline("./partition/3.2output_" + str((i*500) + 500) + ".txt", 7).rstrip()
        # need to use REGEX to find the accuracy
        line = line.split(" ")
        for token in line:
            if re.search(r"[0-9\.0-9]", token):
                accuracy = token
        result += str((i*500) + 500) + " lines from 11,000 training file, Accuracy is " + accuracy + "%\n"
    
    # write all the result to 3.2output.txt
    writeFile("3.2output.txt", result)
    
    return True



# part 3.3  You need to run the command sh /u/cs401/WEKA/infogain.sh *arff file* > *output file* on CDF!!!
def part_3_3():
    ''' Feature analysis 
    For each of n = 500 and n = 5500 in Section 3.2, run WEKA’s information gain attribute selector and
    copy the output of WEKA into the file 3.3output.txt.
    '''
    
    
    os.system("sh ./infogain.sh ./partition/part3_2_partition500.arff > ./partition/part3_3_partition500.txt")
    os.system("sh ./infogain.sh ./partition/part3_2_partition5500.arff > ./partition/part3_3_partition5500.txt")
    
    result = ""
    
    # read partition with 500 lines
    file = open("./partition/part3_3_partition500.txt", 'r+')
    content = file.read()
    result += content
    
    # read partition with 5500 lines
    file = open("./partition/part3_3_partition5500.txt", 'r+')
    content = file.read()
    result += content
    
    # write results from 500 and 5500 partitions 
    writeFile("3.3output.txt", result)
    

# part 3.4
def scripts(fname):
    ''' cross validation
    
    For each of the classifiers in subtask 3.1, run 10-fold
    cross-validation on the arff file containing all 11,000 training tweets
    '''
    
    # read line from actual data
    start_data = 28
    line = linecache.getline(fname, start_data).rstrip()

    # partition data
    partition_class0 = []
    partition_class4 = []
    
    max_count = 550   # shuold be 550
    count_class0 = 0
    count_class4 = 0
    
    partition_lines_class0 = ''
    partition_lines_class4 = ''
    while (line):
        if (count_class0 < max_count and line[-1] == "0"):
            partition_lines_class0 += line.strip() + "\n"
            count_class0 += 1
            if (count_class0 == max_count):
                count_class0 = 0
                partition_class0.append(partition_lines_class0)
                partition_lines_class0 = ""            
            start_data += 1
            line = linecache.getline(fname, start_data).rstrip() 
        elif (count_class4 < max_count and line[-1] == "4"):
            partition_lines_class4 += line.strip() + "\n"
            count_class4 += 1
            if (count_class4 == max_count):
                count_class4 = 0
                partition_class4.append(partition_lines_class4)
                partition_lines_class4 = ""            
            start_data += 1
            line = linecache.getline(fname, start_data).rstrip()
        else:
            print("shuoldn't reach here!! line is -> ", line)
            start_data += 1
            line = linecache.getline(fname, start_data).rstrip()            
            
    # append lines that are less than maximum lines
    if (partition_lines_class0 != ""):
        partition_class0.append(partition_lines_class0)
    if (partition_lines_class4 != ""):
        partition_class4.append(partition_lines_class4)
            
    # now create 10 partitions files
    trainings = ["","","","","","","","","",""]
    for i in range(10):  #should be 10
        trainings[i] += HEAD
        for j in range(10):  #should be 10
            if not (i == j):
                trainings[i]+= partition_class0[j] + partition_class4[j]
        writeFile("./partition/part3_partition" + str(i) + ".arff",trainings[i])
    
    
    # run 10 partition files with 3 algorithms and save all the output
    for i in range(10):
        os.system("java -cp ./weka.jar weka.classifiers.functions.SMO -t ./partition/part3_partition" + str(i) + ".arff -o  > ./partition/output_SMO" + str(i) +".txt")
        os.system("java -cp ./weka.jar weka.classifiers.bayes.NaiveBayes -t ./partition/part3_partition" + str(i) + ".arff -o -no-cv > ./partition/output_bayes" + str(i) +".txt")
        os.system("java -cp ./weka.jar weka.classifiers.trees.J48 -t ./partition/part3_partition" + str(i) + ".arff -o -no-cv > ./partition/output_tree" + str(i) + ".txt")
    
    # calculate accuracy, precision and recall from the output above 
    result = ""
    
    algos = ["./partition/output_SMO","./partition/output_bayes","./partition/output_tree"]
    head = ["Algorithm: SVMs, Input Files: 10 partitions from train.arff",\
            "Algorithm: naive Bayes, Input Files: 10 partitions from train.arff",\
            "Algorithm: Decision Trees, Input Files: 10 partitions from train.arff"]
    j = 0
    for algo in algos:
        result += head[j] + "\n"
        for i in range(10):
            # get accuracy line
            line = linecache.getline(algo + str(i) +".txt", 7).rstrip()
            line = line.split(" ")
            for token in line:
                if re.search(r"[0-9\.0-9]", token):
                    accuracy = token
            
            # get table line
            line = linecache.getline(algo + str(i) +".txt", 20).rstrip()
            if (line):
                tokens = line.strip().split(" ")
                a1 = int(tokens[0])
                b1 = int(tokens[1])
            line = linecache.getline(algo + str(i) +".txt", 21).rstrip()    
            if (line):
                tokens = line.strip().split(" ")
                a2 = int(tokens[0])
                b2 = int(tokens[1])
                
            # calculate precision and recall
            precision_0 = float(a1)/float(a1 + a2)
            precision_4 = float(b2)/float(b1 + b2)
            
            recall_0 = float(a1)/float(a1 + b1)
            recall_4 = float(a2)/float(a2 + b2)
            
            avg_precision = float(precision_0 + precision_4) /2
            avg_recall = float(recall_0 + recall_4) /2
            
            # find p-value
            a = [a1,a2]
            b = [b1,b2]
            S = stats.ttest_rel(a, b)
        
            result += "Result from partition"+ str(i) + "\n"+\
                "accuracy: " + str(accuracy) + "\n" +\
                "precision for class 0: " + str(precision_0) + "\n" +\
                "precision for class 4: " + str(precision_4) + "\n" +\
                "average precision for class 0 and 4: " + str(avg_precision) + "\n" +\
                "recall for class0: " + str(recall_0) + "\n" +\
                "recall for class4: " + str(recall_4) + "\n" +\
                "average recall for class 0 and 4: " + str(avg_recall) + "\n" +\
                "p-value: " + str(S) + "\n\n" 
            
        result += "\n\n"
        j+=1

    # write all the result to 3.4output.txt
    writeFile("3.4output.txt", result)
    
    return True
            
            
def writeFile(fname, contents):
    '''  open and write data to file '''
    
    file = open(fname, 'w')
    file.write(str(contents))
    file.close()

if __name__ == "__main__":
    
    
    # Declare input and output file
    testFile = sys.argv[1]
    trainFile = sys.argv[2] 
    
    # part 3.1
    #part_3_1(testFile, trainFile)
    
    # part 3.2
    #part_3_2(trainFile)
    
    # part 3.3
    #part_3_3()
    
    # part 3.4
    #check = scripts(trainFile)
    
