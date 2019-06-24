import tagme
# Set the authorization token for subsequent calls.
tagme.GCUBE_TOKEN = "4a3db199-3ae0-416b-a467-80e5b0bbd016-843339462"

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

def write_to_file(tlist,path):
    fp = open(path,'w')
    print("writing to file")
    for item in tlist:
        fp.write(str(item)+"\n")

    fp.close()

if __name__=="__main__":
    tag_me_ent_list = tagme_annotation('./full.tgt')
    write_to_file(tag_me_ent_list, './ent_list_tagme.txt')