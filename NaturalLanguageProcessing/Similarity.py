
# coding: utf-8

# In[8]:

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora
import os
from gensim import corpora, models, similarities
import tempfile
TEMP_FOLDER = tempfile.gettempdir()
print('Folder "{}" will be used to save temporary dictionary and corpus.'.format(TEMP_FOLDER))
documents = ["Human machine interface for lab abc computer applications",
                "A survey of user opinion of computer system response time",
                 "The EPS user interface management system",
                "System and human system engineering testing of EPS",
                "Relation of user perceived response time to error measurement",
                "The generation of random binary unordered trees",
                "The intersection graph of paths in trees",
                "Graph minors IV Widths of trees and well quasi ordering",
                "Graph minors A survey"]
     # remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
          for document in documents]

# remove words that appear only once
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
     for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1]
          for text in texts]

from pprint import pprint  # pretty-printer
pprint(texts)
dictionary = corpora.Dictionary(texts)
dictionary.save(os.path.join(TEMP_FOLDER,'deerwester.dict'))  # store the dictionary, for future reference
print(dictionary)
print(dictionary.token2id)
new_doc = "Human computer interaction"
new_vec = dictionary.doc2bow(new_doc.lower().split())
print(new_vec)  # the word "interaction" does not appear in the dictionary and is ignored
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize(os.path.join(TEMP_FOLDER,'deerwester.dict'), corpus)  # store to disk, for later use
print(corpus)


# In[2]:

print('Folder "{}" will be used to save temporary dictionary and corpus.'.format(TEMP_FOLDER))


# In[ ]:




# In[3]:

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)


# In[4]:

doc = "Human computer interaction"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow] # convert the query to LSI space
print(vec_lsi)


# In[5]:

index = similarities.MatrixSimilarity(lsi[corpus]) # transform corpus to LSI space and index it


# In[6]:

index.save(os.path.join(TEMP_FOLDER, 'deerwester.index'))
#index = similarities.MatrixSimilarity.load(os.path.join(TEMP_FOLDER, 'index'))


# In[1]:

sims = index[vec_lsi] # perform a similarity query against the corpus
print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples


# In[ ]:



