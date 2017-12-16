# concatenates all files from TEXT_FOLDER into a single file
# and saves it in the DATA_FOLDER

import os

TEXT_FOLDER = "/home/rumen/nltk_data/corpora/gutenberg/"

file_names = os.listdir(TEXT_FOLDER)
file_paths = [TEXT_FOLDER + s for s in file_names]

DATA_FOLDER = "/home/rumen/github_data/reversed_enthropy/"
output_file = DATA_FOLDER + "sample.txt"


with open(output_file, 'w') as outfile:
    for fname in file_paths:
        with open(fname, 'r') as readfile:
            outfile.write(readfile.read() + "\n\n")

print "Done"
