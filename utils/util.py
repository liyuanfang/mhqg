import numpy as np
import torch
def load_embeddings(n_src_vocab, d_word_vec):
    emb = np.zeros((n_src_vocab,d_word_vec))
    with open('data/final_data/triple_emb.txt') as embed:
        for line in embed:
            id = line.split()[0]
            emb[int(id)] = line.split()[1:]
    return torch.from_numpy(emb).float()

'''load pre trained vectors from the embed file'''
def load_pretrained_vectors(self, emb_file):
    """Load in pretrained embeddings.

    Args:
      emb_file (str) : path to torch serialized embeddings
    """

    if emb_file:
        pretrained = torch.load(emb_file)
        pretrained_vec_size = pretrained.size(1)
        if self.word_vec_size > pretrained_vec_size:
            self.word_lut.weight.data[:, :pretrained_vec_size] = pretrained
        elif self.word_vec_size < pretrained_vec_size:
            self.word_lut.weight.data \
                .copy_(pretrained[:, :self.word_vec_size])
        else:
            self.word_lut.weight.data.copy_(pretrained)