# 
# CSC401. Natural Language Computing 
#
# Assignemnt 1. 
# part2. Gathering Feature Information
# Task: takes tokenized and tagged tweets from Part1 and builds an arff datafile
#       that will be used to classify tweets in Part3
#
# main.py
# buildarff.py
#
# Created by Seungkyu Kim on Feb 8th, 2016 
# Copyright 2016 Seungkyu Kim All rights reserved.
#
#
# >$ python <input filename> <output filename> <(OPTIONAL)MAX_num>
# >$ python buildarff.py test.twt some.arff 50


import sys
import math
import re

first_person_pronouns = ["i", "me", "my", "mine", "we", "us", "our", "ours"]
second_person_pronouns = ["you", "your", "yours", "u", "ur", "urs"]
third_person_pronouns = ["he", "him", "his", "hse", "her", "hers", "it", \
                         "its","they", "them", "their", "theirs"]
past_verbs = ["VBD","VBN"]
future_verbs = ["\'ll", "will", "gonna", "going"]
coor_conjunctions = ["and", "but", "for", "nor", "or", "so", "yet"]
parentheses = ["[", "]", "{", "}", "(", ")", "<", ">"] 

common_nouns = ["NN", "NNS"]
proper_nouns = ["NNP", "NNPS"]
adverbs = ["RB","RBR","RBS"]
wh_words = ["WDT", "WP", "WP$", "WRB"]

ARFF_FORMAT = "@relation tweet_classification\n\n\n\
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

def gathering(tweet, num_sentence, slang):
    '''(str, int, str) -> str 
    
    return counting of features for the given tweet
    
    '''
    
    
    features = [0,  # 0 : fist_pronouns 
                0,  # 1 : second_pronouns
                0,  # 2 : thir_pronouns
                0,  # 3 : coor_conjunctions
                0,  # 4 : past_verbs
                0,  # 5 : future_verbs
                0,  # 6 : commas
                0,  # 7 : colon_and_semi
                0,  # 8 : dashes
                0,  # 9 : parentheses
                0,  # 10 : ellipses
                0,  # 11 : common_nouns
                0,  # 12 : proper_nouns
                0,  # 13 : adverbs
                0,  # 14 : wh_words
                0,  # 15 : modern_slang,
                0,  # 16 : words_all_upper
                0,  # 17 : avg_sentences
                0,  # 18 : avg_tokens
                0 ]  # 19 : num_sentences
    
    total_len_word = 0
    total_len_sentence = 0
    num_words = 0
    
    tokens = tweet.split(" ")
    for token in tokens:
        words = token.split("/")
        if len(words) > 1:
            word = words[0]
            tag = words[1]

        # assign number of features
        if word.lower() in first_person_pronouns:
            features[0]+=1
        elif word.lower() in second_person_pronouns:
            features[1]+=1
        elif word.lower() in third_person_pronouns:
            features[2]+=1
        elif word.lower() in coor_conjunctions:
            features[3]+=1
        elif word in past_verbs:
            features[4]+=1
        elif word in future_verbs:
            features[5]+=1
        elif word == ",":
            features[6]+=1
        elif word == ";" or word == ":":
            features[7]+=1
        elif word == "-":
            features[8]+=1
        elif word == parentheses:
            features[9]+=1
        elif (help_check_ellipsis(word)):
            features[10]+=1
        elif tag in common_nouns:
            features[11]+=1
        elif tag in proper_nouns:
            features[12]+=1
        elif tag in adverbs:
            features[13]+=1
        elif tag in wh_words:
            features[14]+=1
        elif tag in slang:
            features[15]+=1
        elif ((word.isupper()) and (len(word) >= 2)):
            features[16]+=1
        if (re.search(r"[\w]+", word)):
            num_words +=1
            total_len_word += len(word)
        
    features[17] = float(total_len_word + num_words - num_sentence) / num_sentence
    if num_words == 0:
        num_words = 1
    features[18] = float(total_len_word) / num_words
    
    return features

def help_check_ellipsis(word):
    '''(str) -> bool
    
    return True if the given word is ellipsis, False otherwise.
    
    '''
    
    answer = False
    if (re.search(r"[^a-zA-Z0-9_ \t\n\r\f\v]", word) and len(word) > 1):
        for index in range(len(word)-1):
            if word[index] != word[index+1]:
                answer = False
                break
    return answer 


def readFile(fname, MAX_num):
    '''(FILE, int) -> str
    
    return contents that contins all counted features from input file.
    If max number is given, return contens that only read and compute 
    up to max number.
    
    '''
    
    #open slang file
    Sfile = open("Slang" ,'r+')
    slang = Sfile.read()
    slang = slang.split("\n")

    file = open(fname, 'r+')
    line = file.readline()
    contents = ARFF_FORMAT
    polarity = ""
        
    count_class0 = 0
    count_class4 = 0
    
    while(line):
        
        # extract class from tweet
        line = line.strip()
        if (re.search(r"<A=", line)):
            new_line = ""
            polarity = int(line[re.search(r"[0-9]", line).end()-1])
            flag = True
            if not (MAX_num == ""):
                if (count_class0 < MAX_num and polarity == 0):
                    count_class0 +=1
                    flag = False
                    line = file.readline().strip()
                elif (count_class4 < MAX_num and polarity == 4):
                    count_class4 +=1
                    flag = False
                    line = file.readline().strip()
                elif (count_class0 == MAX_num and count_class4 == MAX_num):
                    break                    
                else:
                    line = file.readline().strip()
            else:
                flag = False
                line = file.readline().strip()
            
        # feature gathering for the given tweet
        else:
            if not (flag):
                tweet = ''
                num_sentence = 1
                while(line and not re.search(r"^<A=",line)):
                    tweet += line.strip() + " "
                    line = file.readline()
                    num_sentence += 1
                    
                features = gathering(tweet, num_sentence, slang)
                features[19] = num_sentence
                features.append(int(polarity))
                features = str(features)
                features = features[1:-1].replace(" ", "")
                contents += features + "\n"
            else:
                line = file.readline()
    file.close()
    return contents


def writeFile(fname, contents):
    '''(FILE, str) -> null
    
    write contens to the output file
    
    '''
    
    file = open(fname, 'w')
    file.write(str(contents))
    file.close()


def _main():
    '''(Nonetype) -> Nonetype
    count all features of tweets in a given file and write to output file ''' 
    
    # Declare input and output file
    inFile = sys.argv[1]
    outFile = sys.argv[2]
    MAX_num = ""
    if (len(sys.argv) > 3):
        MAX_num = int(sys.argv[3])
        
    # Open and read input file
    contents = readFile(inFile, MAX_num)
    
    # Write tokenned contents to output file
    writeFile(outFile, contents)

if __name__ == "__main__":

    _main()
    