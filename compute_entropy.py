# this method is partially based on the code which I found here:
# http://pit-claudel.fr/clement/blog/an-experimental-estimation-of-the-entropy-of-english-in-50-lines-of-python-code/



import re, math
from collections import defaultdict, deque, Counter


#take a file and retunrs tokens
def tokenize(file_path, tokenizer):
  with open(file_path, mode="r") as file:
    for line in file:
      for token in tokenizer(line.lower().strip()):
        yield token

#tokenizer 1: each character is a token
def chars(file_path):
  return tokenize(file_path, lambda s: s + " ")

#tokenizer 2: each word is a token (puncutation is removed)
def words(file_path):
  return tokenize(file_path, lambda s: re.findall(r"[a-zA-Z']+", s))


# in this model we look at prefix X1 to Xn, preceding the word Xn+1, and build a model for Xn+1
def forward_model(stream, model_order):
  model = defaultdict(Counter)
  circular_buffer = deque(maxlen = model_order)
  for token in stream:
    prefix = tuple(circular_buffer) 
    circular_buffer.append(token)
    if len(prefix) == model_order:
      model[token][prefix] += 1
  return model


def backward_model(stream, model_order):
  model = defaultdict(Counter)
  circular_buffer = deque(maxlen = model_order + 1)
  for current_token in stream:
    suffix = tuple(circular_buffer) 
    circular_buffer.append(current_token)
    if len(suffix) == model_order + 1:
      real_token = suffix[0]
      real_suffix = suffix[1:]
      model[real_token][real_suffix] += 1
  return model


def count_frequencies(stream):
  stats = Counter()
  for token in stream:
      stats[token] += 1
  return stats
  



#combine them into a single definition (instead of running them twice)



def conditional_information(model):
  information_dict = dict()
  for token in model:
    normalization_factor = sum(model[token].values())*1.0
    sum_information = -sum(math.log(proba / normalization_factor,2) for proba in model[token].values())
    average_information = sum_information/len(model[token])
    information_dict[token] = average_information
  return information_dict


file_path = "/home/rumen/github_data/reversed_enthropy/sample.txt"


model_1 = forward_model(words(file_path), 1)
print "Done model 1"
model_2 = backward_model(words(file_path), 1)
print "Done model 2"

model_1a = conditional_information(model_1)
model_2a = conditional_information(model_2)

counts = count_frequencies(words(file_path))



common_keys = set.intersection(set(model_1a), set(model_2), set(counts))
models_1_2a = dict()

for key in common_keys:
  models_1_2a[key] = (model_1a[key], model_2a[key], counts[key])

print "Done model 1_2"

file_path = "/home/rumen/github_data/reversed_enthropy/models_1_2.txt"

def save_dictionary_as_file(dict_name, file_name):
    #save dictionary to file
    file_path = file_name
    f = open(file_path, 'w')
    for entry in dict_name:
        str1 = entry + "," + str(dict_name[entry]) + "\n"
        #remove ()
        str1 = re.sub('[()]', '', str1)
        f.write(str1)
    f.close()
save_dictionary_as_file(models_1_2a, file_path)

