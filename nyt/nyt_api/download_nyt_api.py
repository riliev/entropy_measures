from helper_functions import *
import time
from nytimesarticle import articleAPI
import collections
import csv
import sys
import warnings

api = articleAPI('xxx')

first_date = '2005-03-28'
last_date =  '2006-03-29'
days_in_step = 200



subject_name = "terrorism"
subject_suffix = '_subj'
# if using a list (e.g. ['accidents', 'terrorism', "airplanes", "earthquakes"]) adjust the file naming procedure

#q_string = subject_name
type_of_material_list = ['news', 'front page','article', 'slideshow', 'video','brief', 'blog','caption']
section_name_list = ['world', 'front page', 'U.S.', 'N.Y. / Region', 'NYRegion', 'National', 'New York', 'New York and Region', 'world']
news_desk_list = ['national', 'foreign','world']
words_list_earthquake = ['earthquake', 'earthquakes', 'quake', 'quakes', 'tremor', 'tremors']
words_list_shark = ['shark']

fq_string =  {#'subject': subject_name,
              'body' : words_list_earthquake,
              'type_of_material': type_of_material_list
              #'section_name': section_name_list,
              #'news_desk': news_desk_list
              }
fq_string =  {'subject': ['AIRLINES AND AIRPLANES'],
              #'body' : ['greece', 'earthquake']
              'document_type': 'article',
              'section_name': section_name_list,
              'news_desk': news_desk_list
              }


articles = api.search(
    #q = [ 'earthquake', 'bomb'],
     fq = fq_string,
     begin_date = nyt_api_date(first_date),
     end_date = nyt_api_date(last_date))
# check number of hits:  articles['response']['meta']

# create time variables
time_steps = divide_time_steps(first_date, last_date, days_in_step)

# for each time step print the number of hits and save as page numbers
page_numbers = list()
expected_records = list()


for time_step in time_steps:
     time.sleep(1.2)
     articles = api.search(
          fq = fq_string,
          begin_date = nyt_api_date(time_step[0]),
          end_date = nyt_api_date(time_step[1]))
     numb_hits =  articles['response']['meta']['hits']
     
     if numb_hits > 1000:
          message_1 = "For the period from " + time_step[0] + " to " + time_step[1] + "there are more than 1000 hits"
          #sys.exit(message_1)
          warnings.warn(message_1)
     if numb_hits == 0:
          numb_hits = -10 # this is an arbirtrary number which later becomes -1, since 0 is a meaningful number
     page_numbers.append(numb_hits/10) # if there are 38 hits, there are 4 pages
     expected_records.append(numb_hits)
     print time_step[0], time_step[1], numb_hits


#sys.exit("Script stopped")
error_list = list()
# dowlnoad data and save to files

for time_step_index in range(len(time_steps)):
     time_step = time_steps[time_step_index]
     max_page_number = page_numbers[time_step_index]
     if max_page_number > 100:
          max_page_number = 100
     if max_page_number == -1:
          continue

     file_name = time_step[0] + "_" + time_step[1] + "_" + subject_name + subject_suffix +".csv"
     print "Starting " + file_name + ":"
     
     data = []
     for page_numb in range(max_page_number+2):
          
          time.sleep(1.2)
          try:
              articles = api.search( 
                    fq = fq_string,
                    begin_date = nyt_api_date(time_step[0]),
                    end_date = nyt_api_date(time_step[1]),
                    page = page_numb)
              articles = convert_keys_to_string(articles)
              dic_list = parse_articles(articles)
              error_code = 'None'
              dic_list = add_to_dics (dic_list, page_numb, file_name, error_code, articles)
              data = data + dic_list
              print file_name + ": Page number: " + str(page_numb)
          except Exception, e:
             print file_name + ": Error in page number: ",
             print e,
             print page_numb
             try:
                  time.sleep(1.5)
                  articles = api.search( 
                         fq = fq_string,
                         begin_date = nyt_api_date(time_step[0]),
                         end_date = nyt_api_date(time_step[1]),
                         page = page_numb)
                  articles = convert_keys_to_string(articles)
                  dic_list = parse_articles(articles)
                  error_code = 'None'
                  dic_list = add_to_dics (dic_list, page_numb, file_name, error_code, articles)
                  data = data + dic_list
                  print file_name + ": Page number: " + str(page_numb)
             except Exception, e:
                  print file_name + ": Error in page number: ",
                  print page_numb,
                  print e
                  try:
                        time.sleep(2.0)
                        articles = api.search( 
                              fq = fq_string,
                              begin_date = nyt_api_date(time_step[0]),
                              end_date = nyt_api_date(time_step[1]),
                              page = page_numb)
                        articles = convert_keys_to_string(articles)
                        dic_list = parse_articles(articles)
                        error_code = 'None'
                        dic_list = add_to_dics (dic_list, page_numb, file_name, error_code, articles)
                        data = data + dic_list
                        print file_name + ": Page number: " + str(page_numb)
                  except Exception, e:
                       time.sleep(1.2)
                       print file_name + ": Fatal error in page number: ",
                       print e,
                       print page_numb
                       error_list.append(file_name)
                       dic_list = empty_article()
                       error_code = e
                       try:
                            articles = articles
                       except:
                            articles = 'error'
                       dic_list = add_to_dics (dic_list, page_numb, file_name, error_code, articles)
                       data = data + dic_list
               
     # save to file
     #if len(data) == (expected_records[time_step_index]):
     if len(data) > 0:
          for element in data:
               element = convert_dic_values(element)
          #data = convert_dic_values(data)
          #for i in range(len(data)):
          #    data[i] = convert2(data[i])

          
          keys = data[0].keys()
          with open(file_name, 'wb') as output_file:
              dict_writer = csv.DictWriter(output_file, keys)
              dict_writer.writeheader()
              dict_writer.writerows(data)
          print "Done with " + file_name
          print "Length data is: " + str(len(data)) + ". Expexted records is :" + str(expected_records[time_step_index])
     else:
          articles = 'error'
          dic_list = empty_article()
          error_code = e
          page_numb = 'error'
          dic_list = add_to_dics (dic_list, page_numb, file_name, error_code, articles)
          data = data + dic_list
          keys = data[0].keys()
          with open(file_name, 'wb') as output_file:
              dict_writer = csv.DictWriter(output_file, keys)
              dict_writer.writeheader()
              dict_writer.writerows(data)
          print "All records in " + file_name + " are empty. "
          print "Length data is: " + str(len(data)) + ". Expexted records is :" + str(expected_records[time_step_index])

          # sys.exit("Error in data")
          


# consider adding an error correction componnent
# Google geocoding API https://andrewpwheeler.wordpress.com/2016/04/05/using-the-google-geocoding-api-with-python/


