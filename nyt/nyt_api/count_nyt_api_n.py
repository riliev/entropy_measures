from helper_functions import *
import time
from nytimesarticle import articleAPI
import collections
import csv
import sys
import warnings
import re



api = articleAPI('xxx')

folder_path = "xxx"
file_name = "shark_date_location.csv"
file_path = folder_path + file_name

file = open(file_path, 'r')

counter = 0
max_counter = 2800
for line in file:
     line = line[:-1]
     line = re.sub('[!@#$"]', '', line)
     split_line =  line.split(',')
     first_date = split_line[1]
     last_date =  split_line[2]
     place = split_line[3]

     q_string = q = [ 'shark', place]

     if counter == 0:
          new_line = "counter" + "," +  line + "," + "hits" + "," + "error_msg" + "," + "articles"
          print new_line

     if counter > 0 and counter < max_counter:
          time.sleep(1.2)
          try:
               articles = api.search(
                    q = q_string,
                    begin_date = nyt_api_date(first_date),
                    end_date = nyt_api_date(last_date))
               hits = articles['response']['meta'][u'hits']
               error_msg = "NA"
          except Exception, e:
               hits = -1
               error_msg = str(e)
               articles = "NA"
          new_line = str(counter) + "," +  line + "," + str(hits) + "," +error_msg + "," + str(articles)
          print new_line

     
     counter +=1
     #print line, 
