import pickle as pkl
import nltk
import re

def create_dict(ent_list,type):
    #print("creating entities dictionary")
    #print(ent_list)
    ent_dict ={}
    for i, item in enumerate(ent_list):
        ent_dict[type+'_'+str(i)] = item
    return ent_dict



def process_subgraph(file_path):
    sub_ent_dicts =[]
    obj_ent_dicts =[]
    rel_dicts =[]
    with open(file_path) as fp:
        for line in fp:
            print(line)
            input()


def process_tgt(tgt_file_path,sub_ents,rels,obj_ents):
    print("processing tgt file ")
    output_file = open('../data/final_data/processed_tgt.txt','w')
    with open(tgt_file_path,'r') as tgt:
        for i,line in enumerate(tgt):
            sub_dict = sub_ents[i]
            rel_dict = rels[i]
            obj_dict = obj_ents[i]
            line_words = nltk.word_tokenize(line.lower())
            line = ' '.join(line_words)
            line = process_tgt_line(line.strip(),sub_dict)
            line = process_tgt_line(line,rel_dict)
            line = process_tgt_line(line,obj_dict)
            print(line)
            output_file.write(line)
            output_file.write("\n")
    output_file.close()



def process_tgt_line(line,dict):
    for key,value in dict.items():
        found = False
        value_words = nltk.word_tokenize(value.lower())
        value = " ".join(value_words).lower()
        if value.lower() in line:
            start_idx = line.find(value.lower())
            end_idx = start_idx + len(value.lower())
            found = True
        if value.replace(" ",'') in line:
            start_idx = line.find(value.replace(" ",'').lower())
            line = line.replace(value.replace(" ",''),value)
            end_idx = start_idx + len(value.lower())
            found = True
        if found:
            line = line[:start_idx] + ' ' + key + ' ' + line[end_idx + 1:]
    return line







def write_dicts(sub_ent_dicts,rel_dicts,obj_ent_dicts):
    sub_ent_file = open('../data/final_data/sub_ent_dicts.pkl','wb')
    rel_file = open('../data/final_data/rel_dicts.pkl','wb')
    obj_ent_file = open('../data/final_data/obj_ent_dicts.pkl','wb')
    pkl.dump(sub_ent_dicts,sub_ent_file)
    pkl.dump(rel_dicts,rel_file)
    pkl.dump(obj_ent_dicts,obj_ent_file)




if __name__=="__main__":
    print("Code for processing the subgraph and creating dictionaries")
    subs,rels,objs = process_subgraph('../data/final_data/mid2name.txt')
    #process_tgt('../data/final_data/lcquad_questions.txt',subs,rels,objs)
    #write_dicts(subs,rels,objs)
    print(subs)
    print(rels)
    print(objs)
