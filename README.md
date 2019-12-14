# MHQG: Multi-hop Question Generation from Knowledge Graphs

Source code and dataset for our paper "Difficulty-controllable Multi-hop Question Generation From Knowledge Graphs" accepted at [ISWC 2019](https://iswc2019.semanticweb.org/).

Some instructions to run the code:
===================================
1) Download pre-trained embeddings from here (http://139.129.163.161/index/toolkits#pretrained-freebase)
2) Preprocess cwq dataset and create binary file data.pt (which also contains a vocabulary)
4) Extract embeddings for entities and relationships in CWQ dataset (given in this repo)  from vocabulary.
5) Create an embedding file with all entities, relationships and 256 dimensional embedding (all space separated) say pretrained.pt 
6) Run train.py with '-data' path set to data.pt
7) To generate a question from the trained model run "generate_question.py" with required arguments such as model path etc.



