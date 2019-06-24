import numpy as np
entity_dict = {}
rel_dict = {}
entity_embed_dict ={}
rel_embed_dict = {}


''' processing subgraph replace 0 for unk '''
def process_subgraph(subg_path,answer_path):
    fp = open(subg_path+".processed",'w')
    print("processing sub graph")
    with open(subg_path) as f, open(answer_path) as ansf:
        for line,answer in zip(f,ansf):
            answer_ids = answer.strip().split()
            #print(line)
            processed_triples =[]
            line = line.strip()
            triples = line.split("<t>")
            for t in triples:
                if t.strip():
                    t_split = t.split()
                    head = t_split[0]
                    tail = t_split[2]
                    relation = t_split[1]
                    h_id = get_id(head,'ent')
                    if head in answer_ids:
                        h_id = h_id+"e￨A"
                    else:
                        h_id = h_id + "e￨O"
                    t_id = get_id(tail,'ent')
                    if tail in answer_ids:
                        t_id = t_id + "e￨A"
                    else:
                        t_id = t_id + "e￨O"
                    r_id = get_id(relation,'rel')
                    triple_converted = h_id+' '+r_id+"r￨O"+' '+t_id
                    processed_triples.append(triple_converted)
            processed_line = " <t> ".join(processed_triples)
            fp.write(processed_line+"\n")
    fp.close()

def write_dict(dict,path):
    fp = open(path,'w')
    for key,value in dict.items():
        fp.write(key+"\t"+value+"\n")
    fp.close()




def get_id(x,what):
    id = "0"
    if what =="ent":
        for key,value in entity_dict.items():
            if x == value:
                id = key

    if what == "rel":
        for key,value in rel_dict.items():
            if x == value:
                id = key
    return id

''' load entity dictionary '''
def load_entity_dict(path):
    with open(path) as f:
        for line in f:
            line = line.strip().split("\t")
            entity_dict[line[0]] = line[1]
            entity_embed_dict[line[0]] = line[3]

    return entity_dict,entity_embed_dict

'''Load relation dictionary'''
def load_relation_dict(path):
    with open(path) as f:
        for line in f:
            line = line.strip().split()
            rel_dict[line[0]] = line[1]
            rel_embed_dict[line[0]] = line[3]

    return rel_dict,rel_embed_dict


def create_triple_dict_process_subgraph(path):
    triple_dict ={}
    id = 1
    triples_set = set()
    fp = open(path+".processed",'w')
    fp_td = open(path+".triple_dict",'w')
    with open(path) as f:
        for line in f:
            line = line.strip()
            triples = line.split("<t>")
            for t in triples:
                triples_set.add(t)
    for t in triples_set:
        triple_dict[id] = t
        id+=1
    for key, value in triple_dict.items():
        fp_td.write(str(key) + "\t" + value + "\n")
    with open(path) as f:
        for line in f:
            line = line.strip()
            for key,value in triple_dict.items():
                #fp_td.write(str(key)+"\t"+value+"\n")
                if value in line:
                    line = line.replace(value,str(key))
            fp.write(line+"\n")
    fp.close()
    fp_td.close()

def embed_subgraph(subg_path):
    with open(subg_path) as f:
        triple_dict ={}
        for line in f:
            line = line.strip()
            triples = line.split("<t>")
            for t in triples:
                print("triple is :",t)
                t_split = t.split()
                h = t_split[0]
                r = t_split[1]
                t = t_split[2]
                if h in entity_embed_dict.keys():
                    h_emb = entity_embed_dict[h]
                else:
                    h_emb = np.random.normal(0,1,50)
                if r in rel_embed_dict.keys():
                    r_emb = rel_embed_dict[r]
                else:
                    r_emb = np.random.normal(0,1,50)
                if t in entity_embed_dict.keys():
                    h_emb = entity_embed_dict[h]
                else:
                    h_emb = np.random.normal(0,1,50)

if __name__=="__main__":

    print("preprocessing complex web questions")

    entity_dict,entity_embed_dict = load_entity_dict('../data/cwq/no_masking/ert_embed/entity_info.txt')
    write_dict(entity_dict,'../data/cwq/no_masking/ert_embed/entity_dict.txt')
    write_dict(entity_embed_dict,'../data/cwq/no_masking/ert_embed/entity_embed_dict.txt')
    #print(entity_dict)
    rel_dict,rel_embed_dict = load_relation_dict('../data/cwq/no_masking/ert_embed/relation_info.txt')
    write_dict(rel_dict, '../data/cwq/no_masking/ert_embed/rel_dict.txt')
    write_dict(rel_embed_dict, '../data/cwq/no_masking/ert_embed/rel_embed_dict.txt')
    #print(rel_dict)
    print("Entity and relation dict loaded")
    process_subgraph('../data/cwq/no_masking/ert_embed/subgraph.txt',"../data/cwq/no_masking/ert_embed/answer_id.txt")
    #create_triple_dict_process_subgraph('../data/cwq/no_masking/triple_sequence/full.src')
    #embed_subgraph('../data/cwq/no_masking/triple_sequence/full.src')

    #embed_triples('../data/cwq/no_masking/subgraph.txt',entity_dict,rel_dict)