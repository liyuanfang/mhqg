''' @author vishwajeet'''

import wikipediaapi
import re
import spacy
import json
from pycorenlp import StanfordCoreNLP
from multiprocessing.dummy import Pool as ThreadPool
import tagme
# Set the authorization token for subsequent calls.
tagme.GCUBE_TOKEN = "4a3db199-3ae0-416b-a467-80e5b0bbd016-843339462"

wiki = wikipediaapi.Wikipedia('en')
fp = open('../data/cwq/ertsequence/full.json')
data = json.load(fp)

nlp = spacy.load("en_core_web_sm")

def getpopularity_score(entity):
    ent = wiki.page(entity)
    score = 0
    if repr(ent.exists()):

        outlinks = len(ent.backlinks)
        #inlinks = len(ent.links)
        score= score+outlinks
    else:
        ent = wiki.page(entity.replace('the'," "))
        if repr(ent.exists()):
            outlinks = len(ent.backlinks)
            # inlinks = len(ent.links)
            score = score + outlinks
    return score

def selectivity_score(entity):
    print("selectivity score")

def tagme_annotation(quest_path):
    print("annotating using tagme")
    tagme_entity_list =[]
    with open(quest_path) as f:
        for i, line in enumerate(f):
            print(i)
            line = line.strip()
            ent_t_score = {}
            lunch_annotations = tagme.annotate(line)
            # Print annotations with a score higher than 0.1
            for ann in lunch_annotations.get_annotations(0.2):
                #print(ann.entity_title)
                ent_t_score[ann.entity_title] = ann.score
            tagme_entity_list.append(ent_t_score)
    return tagme_entity_list


def get_named_entities_from_corenlp(text):
    nlp = StanfordCoreNLP('http://localhost:9000')
    output = nlp.annotate(text, properties={
        'annotators': 'ner',
        'outputFormat': 'json'
    })
    return [a['text'] for a in output['sentences'][0]['entitymentions']]
    #print([str(a) +"\n"for a in output['sentences'][0]['entitymentions']])


def get_named_entities(ques):
    #print("get named entities for all questions and dump to a file")
    named_entities = []
    doc = nlp(ques)
    for ent in doc.ents:
        #print(ent.text, ent.start_char, ent.end_char, ent.label_)
        named_entities.append(ent.text)
    return named_entities

def search_topic_entity_in_json(ques):
    entity = []

    for d in data:
        if d['question'] == ques:
            entity.append(d['TopicEntityName'])
    return entity


def process_all_questions(path):
    print("processing questions file and getting all named entities")
    final_ent_name = []
    with open(path) as f:
        for i,line in enumerate(f):
            line = line.strip()
            if i < 2939:
                #continue
                entity_list = search_topic_entity_in_json(line)
                final_ent_name.append(entity_list)
                #print(i)
                #print(entity_list)
            else:
                entity_list = get_named_entities(line)
                if not entity_list:
                    entity_list = get_named_entities_from_corenlp(line)
                final_ent_name.append(entity_list)
                #print(i)
                #print(entity_list)
    return final_ent_name

def get_popularity_score_for_ent_list(ent_list_path):
    to_write_file = open(ent_list_path+"withscore",'w')
    ent_pop_score_list =[]
    with open(ent_list_path) as f:
        for line in f:
            ent_pop_score ={}
            line = line.strip()
            ent_list = eval(line)
            if ent_list:
                for ent in ent_list:
                    ent_pop_score[ent] = getpopularity_score(ent.strip())
                    print(ent_pop_score)
            to_write_file.write(str(ent_pop_score)+"\n")
            ent_pop_score_list.append(ent_pop_score)
    to_write_file.close()

labels2mid_dict = {}
def load_labels_dict(path):
    print("loading labels into a dict")

    with open(path) as f:
        for line in f:
            line = line.strip().replace('"','').replace('@en','')
            line_splitted = line.split("\t")
            labels2mid_dict[line_splitted[0]] = line_splitted[1].lower()
    return labels2mid_dict


def get_selectivity_score(path):
    print("Get selectivity score")
    label_list = list(labels2mid_dict.values())
    fp = open(path+"selectivityscore",'w')
    with open(path) as f:
        for line in f:
            sel_score ={}
            line = line.strip()
            line = eval(line)
            ent_list = line.keys()
            for ent in ent_list:
                score =label_list.count(ent.strip().lower())
                if score ==0:
                    tmp = ent.strip().split()[0]
                    score = label_list.count(tmp.strip().lower())
                sel_score[ent] = score
            #print(str(sel_score))
            fp.write(str(sel_score)+"\n")
    fp.close()







# def get_named_entities_from_string(ques):
#     doc = nlp(ques)
#     tagged_sent = [(w.text, w.tag_) for w in doc]
#     normalized_sent = [w.capitalize() if t in ["NN", "NNS"] else w for (w, t) in tagged_sent]
#     normalized_sent[0] = normalized_sent[0].capitalize()
#     string = re.sub(" (?=[\.,'!?:;])", "", ' '.join(normalized_sent))
#     doc = nlp(string)
#     print(string)
#     named_entities = []
#     for ent in doc.ents:
#         print(ent.text, ent.start_char, ent.end_char, ent.label_)
#         named_entities.append(ent.text)
#
#     return named_entities

def write_to_file(tlist,path):
    fp = open(path,'w')
    print("writing to file")
    for item in tlist:
        fp.write(str(item)+"\n")

    fp.close()
#------------After preprocessing we are normalizing scores ---------------



def normalize_score_dict(dict_path):
    minx = 0.2
    maxx = 1.0
    fp = open(dict_path+".normalized",'w')

    with open(dict_path) as f:
        for line in f:
            line = eval(line.strip())
            norm_dict = {}
            if line:
                for key,value in line.items():
                    norm_dict[key] = normalize_score(float(value),minx,maxx)

            fp.write(str(norm_dict)+"\n")
    fp.close()

def average_score(dict_path):
    fp = open(dict_path + ".averaged", 'w')
    with open(dict_path) as f:
        for line in f:
            line = eval(line.strip())
            avg_score =0.0
            if line:
                vs = [float(v) for v in line.values()]
                avg_score = sum(vs)/len(vs)
            fp.write(str(avg_score)+"\n")
    fp.close()

def get_min_max(file):
    #fp = open(file+".normalized",'w')
    with open(file) as f:
        linelist = f.readlines()
        linelist = [float(i) for i in linelist]
        print(sum(linelist)/len(linelist))
        print(max(linelist))
        print(min(linelist))
    #     for line in linelist:
    #
    #         print(line)
    #         norm_line = normalize_score(line,0.0,89.10780006715379)
    #         fp.write(str(norm_line)+"\n")
    # fp.close()

def get_final_score(el,sel):
    fp = open("../data/cwq/difficulty_exp/final_score.txt",'w')
    with open(el) as elf, open(sel) as slf:
        for e,s in zip(elf,slf):
            diff_score = float(s.strip())/float(e.strip())
            fp.write(str(diff_score)+"\n")
    fp.close()


def get_difficulty(path):
    fp = open(path+".difficulty",'w')
    with open(path) as f:
        for line in f:
            line = float(line.strip())

            if line >= 0.00010013724356219268:
                dif = "hard"
            else:
                dif = "easy"
            fp.write(dif+"\n")
    fp.close()


def Nmaxelements(file, N):
    with open(file) as f:
        linelist = f.readlines()
        list1 = [float(i) for i in linelist]
    final_list = []

    for i in range(0, N):
        max1 = 0

        for j in range(len(list1)):
            if list1[j] > max1:
                max1 = list1[j]

        list1.remove(max1)
        final_list.append(max1)

    print(final_list)










def normalize_score(x,minx,maxx):
    return (x - minx) / (maxx - minx)



if __name__=="__main__":
    #final_ent_name = process_all_questions('../data/cwq/ertsequence/full.tgt')
    #write_to_file(final_ent_name,'../data/cwq/ertsequence/ent_list.txt')
    # print(len(final_ent_name))
    # pool = ThreadPool(5)
    # ent_paths = ['../data/cwq/ertsequence/tagme_ent_partaa','../data/cwq/ertsequence/tagme_ent_partab','../data/cwq/ertsequence/tagme_ent_partac','../data/cwq/ertsequence/tagme_ent_partad','../data/cwq/ertsequence/tagme_ent_partae']
    # #
    # results = pool.map(get_popularity_score_for_ent_list,ent_paths )
    # pool.close()
    # pool.join()
    #get_popularity_score_for_ent_list('../data/cwq/ertsequence/ent_list.txt')
    #print(getpopularity_score("Alka Lamba"))
    #strt = "Which player started his career late and went on to be the Vancouver Canucks coach?"
    #tagme_annotation(strt)
    #tag_me_ent_list = tagme_annotation('../data/cwq/ertsequence/full.tgt')
    #write_to_file(tag_me_ent_list,'../data/cwq/ertsequence/ent_list_tagme.txt')
    #get_named_entities_from_corenlp(strt)
    # labels2mid_dict = load_labels_dict('../data/cwq/ertsequence/LABELS_EN.tsv')
    # results = pool.map(get_selectivity_score,ent_paths )
    # pool.close()
    # pool.join()
    #get_selectivity_score('../data/cwq/ertsequence/ent_list_tagme.txt',labels2mid_dict )

    #print(get_named_entities(strt))

    #print(getpopularity_score("Narendra Modi"))
    #print(getpopularity_score("India"))
    #print(getpopularity_score("Wiki"))
    #print(getpopularity_score("united states"))
    #print(getpopularity_score("facebook"))

    print("Normalize scores ")
    #normalize_score_dict('../data/cwq/difficulty_exp/ent_list_tagme.txt')
    #average_score('../data/cwq/difficulty_exp/ent_list_tagme.txtselectivityscore')
    get_difficulty('../data/cwq/difficulty_exp/final_score.txt.cleaned_outliers.normalized')
    #get_final_score('../data/cwq/difficulty_exp/ent_list_tagme.txt.averaged.normalized','../data/cwq/difficulty_exp/ent_list_tagme.txtselectivityscore.averaged.normalized')
    #Nmaxelements('../data/cwq/difficulty_exp/final_score.txt',50)
    get_min_max('../data/cwq/difficulty_exp/temp.txt')



