# -*- coding: utf-8 -*-
from ..core.processor_class import Processer
from ..core.basic_utils import dotkeys
import logging
import re
import sys


logger = logging.getLogger("INCA")



class word2vec_googlenews(Processer):
    """"""

    def process(self, document_field):
        """process text for use with pre-trained word embeddings generated from the Google News dataset.
        - number of vectors: 3000000
        - file size:         1.6 GB
        - base dataset:      Google News (about 100 billion words)
        
        - the word embeddings are downloaded from gensim
            - gensim: https://github.com/RaRe-Technologies/gensim-data
            - google: https://code.google.com/archive/p/word2vec/
                - model is no longer hosted at http://word2vec.googlecode.com/svn/trunk/

        - advice for how to preprocess text similar to pre-trained word embeddings
            - https://www.kaggle.com/christofhenkel/how-to-preprocessing-when-using-embeddings
        - https://mccormickml.com/2016/04/12/googles-pretrained-word2vec-model-in-python/

        1. remove html tags
        2. remove extra spaces
        3. remove stopwords
        4. add bigrams
        5. add trigrams

        - do not lowercase
        - do not lemmatize

        - filtering for corpus-level frequency is down elsewhere
        """
        return 


