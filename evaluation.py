from sklearn.metrics import precision_recall_fscore_support as pr
import random
from nltk.translate.bleu_score import sentence_bleu
import nltk
def get_random(path):
    fp = open(path,'w')
    for i in range(50):
        num = random.randint(1,1000)
        fp.write(str(num)+"\n")
    fp.close()

def process_cwq_for_evaluation(path,dict_path):
    fp = open(path+".processed",'w')
    with open(path) as f , open(dict_path) as df:
        for ques,dic in zip(f,df):
            proc_dic ={}
            ques = ques.strip()
            #print(ques)
            dic = eval(dic.strip())
            for k,v in dic.items():
                proc_dic[k] = v[0]
            for k,v in proc_dic.items():
                ques = ques.replace(k,v)
            fp.write(ques+"\n")
    fp.close()

def process_src(subg_path,ent_info_path):
    fp = open(subg_path+".processed",'w')
    id2string ={}
    with open(ent_info_path) as f:
        for line in f:
            line = line.strip()
            l_s = line.split("\t")
            id2string[l_s[1]] = l_s[2].split("<t>")[0]
    with open(subg_path) as f:
        for line in f:
            line = line.strip()
            triples = line.split("<t>")
            triples = triples[:-1]
            t_list =[]
            for t in triples:
                t_s = t.split()
                if t_s[0] in id2string.keys():

                    h = id2string[t_s[0]]
                else:
                    h= "None"
                r = t_s[1]
                if t_s[2] in id2string.keys():

                    t = id2string[t_s[2]]
                else:
                    t="None"
                t_list.append(h+" "+r+" "+t)
            line = " <t> ".join(t_list)
            fp.write(line+"\n")
    fp.close()

def get_a_random_number():
    return random.randint(1,1000)
def get_random_50_ids(s1,s2,s3):
    fp = open('data/eval/random.txt','w')
    id_list = []
    with open(s1) as s1f , open(s2) as s2f , open(s3) as s3f:
        s1_ls = s1f.readlines()
        s2_ls = s2f.readlines()
        s3_ls = s3f.readlines()
        for i in range(100):
            id = get_a_random_number()
            if "none" not in s1_ls[id] and "none" not in s2_ls[id] and "none" not in s3_ls[id]:
                id_list.append(str(id))
    id_list = set(id_list)
    fp.write("\n".join(id_list))
    fp.close()

def get_sentences(path,radom_path):
    fp = open(path+"_50",'w')
    f1 = open(path)
    f_lines = f1.readlines()
    with open(radom_path) as f:
        for line in f:
            line = line.strip()
            l_p = f_lines[int(line)]
            fp.write(l_p)
    fp.close()


def calculate_f1(gold,pred):

    bPrecis, bRecall, bFscore, bSupport = pr(gold, pred, average='binary')
    print(bFscore,bRecall,bFscore)

def calculate_bleu(goldfile,pred_file):
    fp = open(pred_file+"bleu.txt",'w')
    with open(goldfile) as gf, open(pred_file) as pf:
        for g,p in zip(gf,pf):
            g = g.strip()
            # print(g)
            # print(p)
            p = nltk.word_tokenize(p.strip())
            g = nltk.word_tokenize(g.strip())

            score = sentence_bleu([g],p,weights=(0.25, 0.25, 0.25, 0.25))


            fp.write(str(round(score*100,4))+"\n")
    fp.close()




if __name__=="__main__":
    print("Preparation for evaluation")
    #get_random('data/eval/random_pq.txt')
    #calculate_bleu('/Users/vkum38/eval/good_example/test.tgt','/Users/vkum38/eval/good_example/SYS4.txt.processed')
    #get_sentences('data/eval/SYS6.txt','data/eval/random_pq.txt')
    #get_random_50_ids('data/eval/SYS1.txt.processed','data/eval/SYS2.txt.processed','data/eval/SYS3.txt.processed')
    process_cwq_for_evaluation('data/eval/cwq/difficulty_level/pred_hard_2664.txt.processed','data/eval/cwq/test_ent_dict.txt')
    #process_src('data/eval/cwq/test.src','data/eval/cwq/entity_info.txt')
    # g = [0,1,1,1,0,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,0,1,1,0,1]
    # pred =
    # calculate_f1()