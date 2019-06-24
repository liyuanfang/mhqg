''' @author vishwajeet'''


def encode_diff(src_path, diff_path):
    fp = open(src_path+".de",'w')
    with open(src_path) as src, open(diff_path) as dif:
        for s,d in zip(src,dif):
            s = s.strip()
            d = d.strip()
            processed_s = ""
            if d =="easy":
                s_split = s.split()
                s_split = [i+"￨E" for i in s_split]
                processed_s = " ".join(s_split)
            else:
                s_split = s.split()
                s_split = [i + "￨H" for i in s_split]
                processed_s = " ".join(s_split)
            fp.write(processed_s+"\n")
    fp.close()




if __name__=="__main__":
    print("encoding difficulty into train and dev")
    encode_diff('../data/cwq/no_masking/ert_embed/test.src','../data/cwq/no_masking/ert_embed/test.diff')