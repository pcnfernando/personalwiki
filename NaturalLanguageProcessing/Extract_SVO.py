# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import string
import webcolors


import nltk
from nltk.tree import *
from nltk.parse import stanford
import nltk.data
import nltk.draw
import os
import sys
import re
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


stop = stopwords.words('english')



os.environ['STANFORD_PARSER'] = '/Users/chiranfernando/Documents/stanford'
os.environ['STANFORD_MODELS'] = '/Users/chiranfernando/Documents/stanford'

class SVO(object):
    """
    Class Methods to Extract Subject Verb Object Tuples from a Sentence
    """
    def __init__(self):
        """
        Initialize the SVO Methods
        """
        self.noun_types = ["NN", "NNP", "NNPS","NNS","PRP"]
        self.verb_types = ["VB","VBD","VBG","VBN", "VBP", "VBZ"]
        self.adjective_types = ["JJ","JJR","JJS"]
        self.pred_verb_phrase_siblings = None
        self.parser = stanford.StanfordParser()
        self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    def get_attributes(self, sub_tree):
        sub_nodes = []
        sub_nodes = sub_tree.subtrees()
        sub_nodes = [each for each in sub_nodes if each.pos()]
        subject = None

        for each in sub_nodes:

            if each.label() in self.adjective_types:
                attribute = each.leaves()
                break

        return {'attributes': attribute}


    def get_subject(self,sub_tree):
        """
        Returns the Subject and all attributes for a subject, sub_tree is a Noun Phrase
        """
        sub_nodes = []
        sub_nodes = sub_tree.subtrees()
        sub_nodes = [each for each in sub_nodes if each.pos()]
        subject = None

        for each in sub_nodes:

            if each.label() in self.noun_types:
                subject = each.leaves()
                break

        return {'subject':subject}

    def get_object(self,sub_tree):
        """
        Returns an Object with all attributes of an object
        """
        siblings = self.pred_verb_phrase_siblings
        Object = None
        for each_tree in sub_tree:
            if each_tree.label() in ["NP","PP"]:
                sub_nodes = each_tree.subtrees()
                sub_nodes = [each for each in sub_nodes if each.pos()]

                for each in sub_nodes:
                    if each.label() in self.noun_types:
                        Object = each.leaves()
                        break
                break
            else:
                sub_nodes = each_tree.subtrees()
                sub_nodes = [each for each in sub_nodes if each.pos()]
                for each in sub_nodes:
                    if each.label() in self.adjective_types:
                        Object = each.leaves()
                        break
                # Get first noun in the tree
        self.pred_verb_phrase_siblings = None
        return {'object':Object}

    def get_predicate(self, sub_tree):
        """
        Returns the Verb along with its attributes, Also returns a Verb Phrase
        """

        sub_nodes = []
        sub_nodes = sub_tree.subtrees()
        sub_nodes = [each for each in sub_nodes if each.pos()]
        predicate = None
        pred_verb_phrase_siblings = []
        sub_tree  = ParentedTree.convert(sub_tree)
        for each in sub_nodes:
            if each.label() in self.verb_types:
                sub_tree = each
                predicate = each.leaves()

        #get all predicate_verb_phrase_siblings to be able to get the object
        sub_tree  = ParentedTree.convert(sub_tree)
        if predicate:
             pred_verb_phrase_siblings = self.tree_root.subtrees()
             pred_verb_phrase_siblings = [each for each in pred_verb_phrase_siblings if each.label() in ["NP","PP","ADJP","ADVP"]]
             self.pred_verb_phrase_siblings = pred_verb_phrase_siblings

        return {'predicate':predicate}

    def process_parse_tree(self,parse_tree):
        """
        Returns the Subject-Verb-Object Representation of a Parse Tree.
        Can Vary depending on number of 'sub-sentences' in a Parse Tree
        """
        self.tree_root = parse_tree
        # Step 1 - Extract all the parse trees that start with 'S'
        svo_list = [] # A List of SVO pairs extracted
        output_list = []
        output_dict ={}
        i=0

        arrtibure_arr = []
        for idx, subtree in enumerate(parse_tree[0].subtrees()):
            item_attribure = []
            if (subtree.label() in ["NP"]) and subtree[0].label() in ["JJ"]:
                item_attribure.append(subtree[0].leaves()[0])

                if item_attribure not in arrtibure_arr:
                    arrtibure_arr.append(item_attribure)

            subject =None
            predicate = None
            Object = None

            if subtree.label() in ["S", "SQ", "SBAR", "SBARQ", "SINV", "FRAG"]:
                children_list = subtree
                children_values = [each_child.label() for each_child in children_list]
                children_dict = dict(zip(children_values,children_list))

                # Extract Subject, Verb-Phrase, Objects from Sentence sub-trees
                if children_dict.get("NP") is not None:
                    subject = self.get_subject(children_dict["NP"])

                if children_dict.get("VP") is not None:
                    # Extract Verb and Object
                    #i+=1
                    #"""
                    #if i==1:
                    #    pdb.set_trace()
                    #"""
                    predicate = self.get_predicate(children_dict["VP"])
                    Object = self.get_object(children_dict["VP"])

                try:
                    if subject['subject'] is not None:
                        output_dict['subject'] = subject['subject']
                        if predicate['predicate'] is not None:
                            output_dict['predicate'] = predicate['predicate']
                        if Object['object'] is not None:
                            output_dict['object'] = Object['object']
                        if arrtibure_arr is not None:
                            output_dict['attributes'] = arrtibure_arr

                    output_list.append(output_dict)
                except Exception:
                        print (Exception)
                        continue

        return output_list




    def traverse(self,t):
        try:
            t.label()
        except AttributeError:
            print(t)
        else:
            # Now we know that t.node is defined
            print('(', t.label())
            for child in t:
                self.traverse(child)

            print(')')

    def sentence_split(self,text):
        """
        returns the Parse Tree of a Sample
        """
        sentences = self.sent_detector.tokenize(text)
        return sentences


    def get_parse_tree(self,sentence):
        """
        returns the Parse Tree of a Sample
        """
        parse_tree = self.parser.raw_parse(sentence)

        return parse_tree


    def clean_document(self,document):
        tokenized_docs_no_punctuation = []
        stop_words = set(stopwords.words("english"))


        for word in document:
            if word not in stop_words:
                text = ''.join([i for i in word if not i.isdigit()])
                tokenized_docs_no_punctuation.append(text)

        return tokenized_docs_no_punctuation


    def getAttributes(self,classes, taggedArr_):
        result = []
        count = 0
        for each in taggedArr_:
            item = []
            count +=1
            for clas in classes:
                if each[0] == clas and taggedArr_[count-2][1] in self.adjective_types:
                    print(taggedArr_[count-2])
                    item.append(taggedArr_[count-2][0])
                    item.append(clas)
                    result.append(item)

        print(result)
        return

    #use this method to append a noun to coorectly parse unstructured sentences
    def imperative_pos_tag(self,sent):
    
        return nltk.pos_tag(sent + ['food'])[0:]


    def getSVO(self, sentence):
        svo = SVO()
        if sentence:
            lemmatizer = WordNetLemmatizer();

            # sentence="a small bird is perched on a branch"

            tokenized = nltk.word_tokenize(sentence)

            tagged = nltk.pos_tag(tokenized)

            document = svo.clean_document(tokenized)

            propernouns = [word for word, pos in tagged if pos == 'VBG']

            apended_sentence = []

            for x in document:
                if (x in propernouns):
                    apended_sentence.append(lemmatizer.lemmatize(x, 'v'))
                else:
                    apended_sentence.append(x)

                edt_sentence = " ".join(apended_sentence)

                edt_sentences = svo.sentence_split(edt_sentence)

                val = []

                for sent in edt_sentences:
                    root_tree = svo.get_parse_tree(sent)
                    val.append(svo.process_parse_tree(next(root_tree)))


            if (val == [[]]):
                val = []

                print('empty extraction')

                noun_pos = [word for word, pos in tagged if pos == 'NN' or pos == 'NNS']
                adjectives_pos = [word for word, pos in tagged if pos == 'JJ']
                verbs_pos = [word for word, pos in tagged if pos == 'VB' or pos == 'VBG']

                for each in noun_pos:
                    if each in webcolors.CSS3_NAMES_TO_HEX:
                        adjectives_pos.append(each)
                        noun_pos.remove(each)

                if noun_pos is not None:
                    if (len(noun_pos) > 2):
                        sub = [noun_pos[1]];
                    else:
                        sub = [noun_pos[0]];

                    obj = []
                    if len(noun_pos) > 3:
                        obj.append(noun_pos[2])

                        if (sub == [noun_pos[0]]):
                            obj.append(noun_pos[1])

                    subObjMap = {}
                    subObjMap['subject'] = sub

                    if obj != []:
                        subObjMap['object'] = obj


                if adjectives_pos is not None:
                    subObjMap['attributes']=adjectives_pos


                val.append([subObjMap]);

            return val


