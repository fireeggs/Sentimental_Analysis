# 
# CSC401. Natural Language Computing 
#
# Assignemnt 1. 
# Part1. Semtiment Analysis with Tweets 
# Task: split the tweets into sentences, tag them with a PoS tagger.
#
# main.py
# twtt.py
#
# Created by Seungkyu Kim on Feb 3rd, 2016 
# Copyright 2016 Seungkyu Kim All rights reserved.
#
#
# >$ ./python <input filename> <group number> <output filename>
# >$ python twtt.py testHTML.txt 71 output.txt

import sys
import math
import re
import NLPlib
import linecache

def removeHTML(tweet):
    ''' (str) -> str
    All HTML tags and attributes are removed ''' 

    tag_re = re.compile(r'<[^>]+>')
    return tag_re.sub('', tweet)


def repalceHTML(tweet):
    '''(str) -> str
    
    return string that is replaced with ASCHIE code 
    '''
    
    tweet = tweet.replace("&amp", "&")
    tweet = tweet.replace("&lt","<")
    tweet = tweet.replace("&gt", ">")
    tweet = tweet.replace("&quot", "\"")
    
    return tweet

    
def removeURL(tweet):
    ''' (str) -> str
    
    return string that is removed URLs
    
    ''' 
    
    new_tweet = ""
    if( re.search("www.|WWW.|http:|HTTP:",tweet)):
        words = tweet.strip().split(" ")
        for word in words:
            if not((re.search("www.|WWW.|http:|HTTP:",word))):
                new_tweet = new_tweet + word  + " "
        tweet = new_tweet.strip() + "\n"
    else:
        new_tweet = tweet
    return new_tweet


def removeTAG(tweet):
    '''  (str) -> str
    
    return string that is removed first character if it is a tag. 
    '''
    
    new_tweet = ""
    tweet = tweet.strip().split(" ")
    for word in tweet:
        if (word):
            if word[0] == "@" or word[0] == "#":
                new_tweet += word[1:] + " "
            else:
                new_tweet += word + " "

    return new_tweet + "\n"

def detectEND_prac(tweet):
    ''' (str) -> str
    
    return string that is seperated by new line character
    '''
    
    lines = tweet.strip().split(" ")
    new_lines = ""
    end_punctuation = ["\?", "\!", "\:", "\-", "\;"]
    for word in lines:
        count = 1
        flag = 0
        for punc in end_punctuation:
            if (re.search(punc, word)):              
                new_lines = new_lines + word.strip() + "\n"
                flag = 1
            elif(re.search("\.", word) and flag == 0):
                for char in word:
                    char_flag = True
                    if (char.isupper()):
                        new_lines = new_lines + word.strip() + " "
                        char_flag = False
                        break
                if(char_flag):
                    word = word.strip()
                    new_lines = new_lines + word.strip() + "\n"
                flag = 1
            else:
                if (count == 5 and flag == 0):                    
                    new_lines = new_lines + word.strip() + " "
            count+=1
    return new_lines.strip() + "\n"

    
def help_findEndOfEllipsis(tweet):
    ''' (str) -> str
    ''' 
    
    i = 1
    while(tweet[0] == tweet[i]):
        i+=1
    return i-1


def seperateSPACE(tweet):
    ''' (str) -> str
    
    return a list of strings that is seperated by a space
    
    '''
       
    new_tweet = ""
    temp_tweet = tweet
     
    # find any non-white, chracters, digits from the given tweet
    while( re.search(r"[^a-zA-Z0-9_ \t\n\r\f\v]", temp_tweet)):
        clitics = re.search(r"[^a-zA-Z0-9_ \t\n\r\f\v]", temp_tweet)
        
        # check tweet has ellipsis or multiple punctuations
        punctuation_index = clitics.end()-1
        punctuation = temp_tweet[punctuation_index]
    
        # not clitics or possessive 's
        if (punctuation != "'"):
            if(punctuation == temp_tweet[clitics.end()]):
                # index is the last ocurrence of ellipsis or punctuations
                index = help_findEndOfEllipsis(temp_tweet[punctuation_index:])
                
                # character follows after punctuation eg.  ...i know -> ... i know                
                if (temp_tweet[punctuation_index:clitics.end()+index+1] != " "):
                    new_tweet = new_tweet + temp_tweet[:punctuation_index] + " " + temp_tweet[punctuation_index:clitics.end()+index] + " "
                else:
                    new_tweet = new_tweet + temp_tweet[:punctuation_index] + " " + temp_tweet[punctuation_index:clitics.end()+index]
                temp_tweet = temp_tweet[clitics.end()+index:]
            else:
                # space is already placed in front of the punctuation or end of line is placed after another punctuation
                if (temp_tweet[clitics.end()-2] == " ") or (temp_tweet[clitics.end()-2] == "\n"):
                    if (punctuation == "'"):
                        new_tweet = new_tweet + temp_tweet[:punctuation_index] + punctuation
                    else:
                        new_tweet = new_tweet + temp_tweet[:punctuation_index] + punctuation + " "
                else:
                    # different punctuations are combined except "'", eg.hello?! -> hello ! ?
                    if (re.search(r"[^a-zA-Z0-9_ \t\n\r\f\v]", temp_tweet[punctuation_index+1])):
                        new_tweet = new_tweet + temp_tweet[:punctuation_index] + " " + punctuation + " "
                    else: 
                        # character follows after punctuation eg. @hello -> @ hello
                        if (temp_tweet[punctuation_index+1] != " "):
                            new_tweet = new_tweet + temp_tweet[:punctuation_index] + " " + punctuation + " "
                        else:
                            new_tweet = new_tweet + temp_tweet[:punctuation_index] + " " + punctuation
    
                temp_tweet = temp_tweet[clitics.end():]
        
        # deal with clitics and possessive 's
        else:
            # clitics, where wasn't -> was n't or WASN'T -> WAS N'T
            if (temp_tweet[punctuation_index-1] == "n" or temp_tweet[punctuation_index-1] == "N"):
                new_tweet = new_tweet + temp_tweet[:punctuation_index-1] + " " + \
                temp_tweet[punctuation_index-1:punctuation_index] + punctuation
                temp_tweet = temp_tweet[clitics.end():]
                
            # possessive 's eg. dogs' -> dogs '
            else:
                new_tweet = new_tweet + temp_tweet[:punctuation_index] + " " + punctuation
                temp_tweet = temp_tweet[clitics.end():]
            
    # last word of line contains punctuation but not added to new line
    if (temp_tweet.strip()):
        new_tweet = new_tweet + temp_tweet.strip()
        
    return new_tweet.strip() + "\n"
    
    
def tagPOS(tweet):
    ''' (str) -> str
    
    return string that is tagged on
    '''
    tagger = NLPlib.NLPlib()
    total_lines = tweet.strip().split("\n")
    tagged_line = ""
    
    for line in total_lines:
        line = line.strip().split(" ")
        tags = tagger.tag(line)
        for index in range(len(line)):
            tagged_line = tagged_line + line[index] + "/" + tags[index] + " "
        tagged_line = tagged_line.strip() + "\n"
        
    return tagged_line.strip() + "\n"


def tokenizing(line):
    ''' (str) -> str
    
    tokenizing the given input line
    
    '''
    
    # get the polarity of tweets from line
    polarity = line[1]
    
    # get a tweet from line
    line = re.split("\"\,", line)
    text_tweet = line[5][1:-1]
    
    # ========== tokenizing ==========
    
    # 1st step, remove html tags and attributes
    text_tweet = removeHTML(text_tweet)
                            
    # 2nd step, replace with an ASCII equivalent
    text_tweet = repalceHTML(text_tweet)
                        
    # 3rd step, remove URLs(where token starts with http or WWW)
    text_tweet = removeURL(text_tweet)
                            
    # 4th step, remove first chracter of user name @ and has tag #
    text_tweet = removeTAG(text_tweet)
                            
    # 5th step, detecting end-of-sentence punctuation
    text_tweet = detectEND_prac(text_tweet)
                            
    # 6th and 7th step, punctuation and clitics are seperated by space
    text_tweet = seperateSPACE(text_tweet)
                            
    # 8th step, token is tagged with its part-of-speech
    text_tweet = tagPOS(text_tweet)
    
    # 9th step, show polarity of each tweet before the tweet
    text_tweet = "<A=" + polarity + ">" + "\n" + text_tweet
    
    return text_tweet


def readLines(fname, groupNum):
    '''  (FILE, int) -> str
    
    read file and group num, if group num is given, read file up to that line.
    otherwise, read file and tokenizing each lines
    '''
    
    # file is training file
    new_lines = ''
    if (fname == "training.1600000.processed.noemoticon.csv"):
        line_class0_start = groupNum * 5500
        line_class0_end = (groupNum+1) * (5500 - 1)
        line_class4_start = 800000 + groupNum * 5500
        line_class4_end = 800000 + ((groupNum + 1) * (5500 - 1))
        
        # read and tokenizing lines for class 0
        while(line_class0_start <= line_class0_end):
            line = linecache.getline(fname, line_class0_start).rstrip()
            
            # tokenizing line
            new_lines += tokenizing(line)
            line_class0_start+=1
            
        # read and tokenizing lines for class 0
        while(line_class4_start <= line_class4_end):
            line = linecache.getline(fname, line_class4_start).rstrip()
           
            # tokenizing line
            new_lines += tokenizing(line)
            line_class4_start+=1            
            
    # file is a test file    
    else:
        file = open(fname, 'r+')
        line = file.readline()
        while(line):
            # get rid of the end of line by slicing
            line = line[:-1]
            new_lines += tokenizing(line)
            line = file.readline()
        file.close()         
        
    return new_lines


def writeFile(fname, contents):
    ''' (FILE, str) -> NoneType

    take input file with string, write it to output file
    
    '''
    
    file = open(fname, 'w')
    file.write(contents)
    file.close()
    

def _main():
    ''' (NoneType) -> NoneType
    
    Read test and training files then creat output file with tagged tokens 
    
    ''' 
    
    # Declare input and output file
    inFile = sys.argv[1]
    groupNum = int(sys.argv[2])
    outFile = sys.argv[3]
    
    # read file and tokenizing lines    
    tokenned_lines = readLines(inFile, groupNum)    
    
    # Write tokenned contents to output file
    writeFile(outFile, tokenned_lines)

if __name__ == "__main__":

    _main()