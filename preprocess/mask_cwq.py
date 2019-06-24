mid2string = {}
ent_dict_list = []
import nltk
def create_mid_string_dict(path):
    with open(path) as f:
        for line in f:
            line = line.strip()
            l_spliited = line.split("\t")
            mid2string[l_spliited[1]] = [s.lower() for s in l_spliited[2].split("<t>")]
def create_ent_dict_subgraph(path):

    with open(path) as f:
        for line in f:
            ent_dict ={}
            line = line.strip()
            #print(line)
            triples = line.split("<t>")[:-1]

            id =1
            for t in triples:
                t_split = t.strip().split()
                if not t_split[0].startswith("m."):
                    ent_dict["Ent_" + str(id)] = [t_split[0].lower()]
                    id += 1
                else:
                    if t_split[0] in mid2string.keys() and mid2string[t_split[0]]!="none":
                        ent_dict["Ent_"+str(id)] = mid2string[t_split[0]]
                        id+=1

                if not t_split[2].startswith("m."):
                    ent_dict["Ent_" + str(id)] = [t_split[2].lower()]
                    id+=1
                else:
                    if t_split[2]  in mid2string.keys() and mid2string[t_split[2]] !="none":
                        ent_dict["Ent_"+str(id)] = mid2string[t_split[2]]
                        id+=1


            ent_dict_list.append(ent_dict)
    #print(ent_dict_list)

def mask(tgt_path):
    tgt_file = open(tgt_path+".masked",'w')
    with open(tgt_path) as tgt:
        for i,line in enumerate(tgt):
            line = line.strip().lower()
            #print(line)
            line = process_tgt_line(line,ent_dict_list[i])
            #print(line)
            tgt_file.write(line+"\n")
            if i==1115:
                print("gotit")
    tgt_file.close()

def write_dict_to_file(dict,path):
    fp = open(path,'w')
    for key,value in dict.items():
        fp.write(str(key)+"\t"+str(value)+"\n")
    fp.close()

def write_list_to_file(list,path):
    fp = open(path,'w')
    for item in list:
        fp.write(str(item)+"\n")
    fp.close()




def process_tgt_line(line,dict):
    for key,v_list in dict.items():
        for value in v_list:
            if value in line:
                line = line.replace(value,key)
                break
    return line

if __name__=="__main__":
    print("masking entities in subgraph")
    create_mid_string_dict('../data/cwq/masking/ert/entity_info.txt')
    create_ent_dict_subgraph('../data/cwq/masking/ert/subgraph.txt')
    write_list_to_file(ent_dict_list,'../data/cwq/masking/ert/ent_dict_list.txt')
    mask('../data/cwq/masking/ert/full.tgt')
