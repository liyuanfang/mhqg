'''@author vishwajeet'''

import wikipediaapi

from multiprocessing.dummy import Pool as ThreadPool

wiki = wikipediaapi.Wikipedia('en')

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
                    #print(ent_pop_score)
            to_write_file.write(str(ent_pop_score)+"\n")
            ent_pop_score_list.append(ent_pop_score)
    to_write_file.close()





if __name__=="__main__":

    pool = ThreadPool(4)
    ent_paths = ['./part_entlistaa','./part_entlistab','./part_entlistac','./part_entlistad','./part_entlistae','./part_entlistaf','./part_entlistag','./part_entlistah']

    results = pool.map(get_popularity_score_for_ent_list,ent_paths )
    pool.close()
    pool.join()
