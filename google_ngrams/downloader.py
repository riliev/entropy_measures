# dowlnads files specified in a csv file and saves them in folders

# the csv file shold have the following columns:
# folder - where the file will be saved
# file name - what is the name of the saved file
# source - the url link to download the file

# at the end the csv file is updated with status (0 failure, 1 success), processing time and size in bytes



import csv
import os
import time
import urllib

#read path to the csv file
csv_filenames = raw_input("Please enter the path to the csv file with url links (e.g. /home/xxx/file_paths.csv) : ")


# read from csv file names and folers where the files will be saved
count_rows = 0
folders = list()
file_names = list()
source = list()
status = list()
size = list()
proc_time = list()
with open(csv_filenames, 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
     for row in spamreader:
          if count_rows > 0:
               folders.append(row[0])
               file_names.append(row[1])
               source.append(row[2])
               status.append(0)
               size.append(0)
               proc_time.append(0)
          count_rows +=1


# download each file and save it in a folder. if the folder does not exist, create it

for file_index in range(0, len(folders)):
     directory = folders[file_index]
     if not os.path.exists(directory):
          os.makedirs(directory)
     # compute time
     tic = time.clock()
     try:
          import urllib
          testfile = urllib.URLopener()
          testfile.retrieve(source[file_index], folders[file_index] + "/" + file_names[file_index])
          status[file_index] = 1
          # get the size of the file
          size[file_index] = os.path.getsize(folders[file_index] + "/" + file_names[file_index])
          print "Done with file ", str(file_index)
     except:
          print "ERROR in file ", str(file_index)
     toc = time.clock()
     print toc - tic, size[file_index]
     proc_time[file_index] = toc - tic
     





with open(csv_filenames, 'wb') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['folders', 'file_names','source', 'status','size', 'proc_time'])
    for row_ind in range(0,len(folders)):
         csv_writer.writerow([folders[row_ind], file_names[row_ind], source[row_ind], status[row_ind],size[row_ind], proc_time[row_ind]])
