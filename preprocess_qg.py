''' @author vishwajeet'''


import numpy as np
from numpy import array
import pickle as pkl
ent_emb_file = 'data/ent_emb_file'
rel_emb_file = 'data/rel_emb_file'


ent_emb_dict = {}
rel_emb_dict = {}

def load_emb_dict():
    with open(ent_emb_file) as emb:
        for line in emb:
            id = line.split()[0]
            vec = line.split()[1:]
            ent_emb_dict[id] = vec

    with open(rel_emb_file) as relemb:
        for line in relemb:
            id = line.split()[0]
            vec = line.split()[1:]
            #print(id,vec)
            rel_emb_dict[id]= vec

#print(ent_emb_dict.keys())
#print(rel_emb_dict.keys())
def process_triple(triple):
    h_entity = triple[0].strip()
    t_entity = triple[2].strip()
    relation = triple[1].strip()
    h_emb = ent_emb_dict.get(h_entity)
    t_emb = ent_emb_dict.get(t_entity)
    r_emb = rel_emb_dict.get(relation)
    triple_emb = h_emb+r_emb+t_emb
    print(len(triple_emb))
    return triple_emb
def get_max_triples(file_path):
    max =1
    with open(file_path,'r') as src:
        for line in src:
            triples = line.split('<t>')
            if max<len(triples):
                max=len(triples)
    return max

def process_data(file_path):
    tdata = []
    listofzeros = [0] * 300
    max_triples = get_max_triples(file_path)

    with open(file_path) as src:
        for line in src:
            data=[]
            triples = line.split('<t>')
            #print("triples length",len(triples))
            for triple in triples:
                data.append(process_triple(triple.split()))
            if len(data)<max_triples:
                for i in range(0, max_triples-len(data)):
                    data.append(listofzeros)
            tdata.append(data)
    print(tdata)
    train_data = array(tdata)
    lens = [len(ll) for ll in tdata]

    return train_data
def generate_emb(triples_dict):
    embed_file = "triples_embed.txt"
    fp = open(embed_file,'w')
    with open(triples_dict) as src:
        for line in src:
            id = line.split()[0]
            triple = line.split()[1:]
            vec = process_triple(triple)
            fp.write(id+" "+" ".join(vec))
            fp.write("\n")
    fp.close()





def save_to_numpy(data,path):
    np.save(path,data)
def save_pkl(data,path):
    pkl.dump(data,path)




if __name__=="__main__":
    print("======Converting triples to embedings========")
    load_emb_dict()
    generate_emb("data/train_triples.src")
    # train_data = process_data("data/train.src")
    # print(train_data.shape)
    # fp = open('data/train_src.pkl','wb')
    # save_pkl(train_data,fp)


