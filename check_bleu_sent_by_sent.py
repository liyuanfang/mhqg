# import pickle as pkl
# def count_entities(pq):
#     data = pkl.load(open(pq,'rb'))
#     ent_list =[]
#     for i in data:
#         ent_list.append(i.values())
#     ent_final = [item for sublist in ent_list for item in sublist]
#     ent_final = set(ent_final)
#
#     print(len(ent_final))
#
# #def count_relations
#
#
# if __name__=="__main__":
#     print("counting entities, relations and triples")
#     count_entities('data/pq/test/test.dict.pkl')



from nltk.translate.bleu_score import sentence_bleu
reference = [['this', 'is', 'a', 'test'], ['this', 'is' 'test']]
candidate = ['this', 'is', 'a', 'test']
score = sentence_bleu(reference, candidate)
print(score)
