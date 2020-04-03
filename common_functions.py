import csv
import datetime
import pickle

import re
from nltk.stem.porter import PorterStemmer

from gensim.models.ldamodel import LdaModel


def fix_nulls(s):
    for line in s:
        yield line.replace('\0', ' ')
        
def str_to_datetime(s):
    s = s.replace(' ','-').replace(':','-')
    return datetime.datetime(*[int(x) for x in s.split('-')])

def read_segments(f, min_duration=0, datetime_window=[]):
    segments = []
    offset = 1 if "snippets" in f else 0 
    csv_f = fix_nulls(open(f,'r'))
    for i,row in enumerate(csv.reader(csv_f)):
        if i==0:
            header_index = {header:j for j,header in enumerate(row)}
            continue
        if int(row[header_index["Duration"]]) < min_duration:
            continue
        if datetime_window and datetime_window[0] < str_to_datetime(row[header_index["Day"]]) <= datetime_window[1]:
            segments.append(row[header_index["Text"]])
    csv_f.close()
    return segments

p_stemmer = PorterStemmer()
def clean_for_lda(text):
    text = text.lower()
    no_punctuation = re.sub(r'([^\s\w]|_)+','', text)
    no_2digits = re.sub(r'\s[0-9]{2}', '__number__', no_punctuation)
    no_time = re.sub(r'[0-9]{1,2}:[0-9]{2}','__time__', no_2digits)
    tokens = [p_stemmer.stem(w).strip() for w in no_time.split()]
    return ' '.join(tokens)

def build_gensim_bow(text, vocab):
    id_count_dict = {}
    tokens = text.split(' ')
    for token in tokens:
        if token in vocab: # if it's one of our vocabulary
            id_count_dict[vocab[token]] = id_count_dict.get(vocab[token], 0) + 1
    return sorted(id_count_dict.items(), key=lambda x: x[0])


def load_model_vocab(model_dir, k):
    model = LdaModel.load(model_dir + '/model-gensim_k={}'.format(k))
    return [model, pickle.load(open(model_dir+'/term_to_index.p','rb')), pickle.load(open(model_dir+'/index_to_term.p','rb'))]