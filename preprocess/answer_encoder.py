''' @author vishwajeet'''

def get_answers(path):
    answer_id_list = []
    answer_string_list = []
    ansfp = open("../data/cwq/answer_encoded/answer_id.txt",'w')
    ansfps = open("../data/cwq/answer_encoded/answer_string.txt",'w')


    with open(path) as f:
        for line in f:
            line = line.strip()
            line_splitted = line.split("<VK>")
            answer_string = line_splitted[0].split("<t>")
            answer_id = line_splitted[1].split("<t>")
            ansfp.write(" ".join(answer_id))
            ansfps.write(" ".join(answer_string))
            ansfp.write("\n")
            ansfps.write("\n")
    ansfp.close()
    ansfps.close()




if __name__=="__main__":
    get_answers("../data/cwq/answer_encoded/subgraph.txt")