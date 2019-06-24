import torch
import numpy as np
def load_vocab(vocab_path):
    predefined_data = torch.load(vocab_path)
    assert 'dict' in predefined_data

    print('[Info] Pre-defined vocabulary found.')
    src_word2idx = predefined_data['dict']['src']
    tgt_word2idx = predefined_data['dict']['tgt']
    return src_word2idx,tgt_word2idx

def load_dict(path,dict_name):
    with open(path) as f:
        for line in f:
            line = line.strip()
            line_splitted = line.split("\t")
            dict_name[line_splitted[0]] = line_splitted[1]
    return dict_name

def read_embeddings(src_word2idx,ent_emb_path,rel_emb_path):
    ent_emb = {}
    rel_emb = {}
    ent_emb = load_dict(ent_emb_path,ent_emb)
    rel_emb = load_dict(rel_emb_path,rel_emb)

    emb_dict = {}
    print("[info] dict len",len(src_word2idx))
    for key,value in src_word2idx.items():

        if 'e' in key and key != '0e':
            #print(key)
            to_search = key.replace('e','')
            emb_dict[value] = ent_emb[to_search]
        if 'r' in key and key != '0r':
            to_search = key.replace('r', '')
            emb_dict[value] = rel_emb[to_search]
    print(len(emb_dict))

    return emb_dict,len(src_word2idx)
def finalize_embeddings(emb_dict,vocab_len):

    filtered_embeddings = np.zeros((vocab_len, 50))
    print(filtered_embeddings.shape)
    for k,v in emb_dict.items():
        filtered_embeddings[int(k)] = [float(x) for x in v.split()]
    return torch.Tensor(filtered_embeddings)






if __name__=="__main__":
    print("embedding entities and relations")
    src_word2idx,_ =load_vocab('../data/cwq/ert_embed/cqg_vocab.pt')
    emb_dict,vocab_len = read_embeddings(src_word2idx,'../data/cwq/ert_embed/entity_embed_dict.txt','../data/cwq/ert_embed/rel_embed_dict.txt')
    filter_embed = finalize_embeddings(emb_dict,vocab_len)
    torch.save(filter_embed,'../data/cwq/ert_embed/src_embed.pt')