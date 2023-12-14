import jieba
import sys

# jieba custom setting.
# jieba.set_dictionary('jieba_dict/dict.txt.big')

#file_save  = open('TestSeg.txt','w')


ret = open("taiwa20170709.txt", "r").read()
seglist = jieba.cut(ret, cut_all=False)
print(" ".join(seglist))

#sentence = "今天好熱"
#seglist = jieba.cut(sentence, cut_all=False)
#print (" ".join(seglist))



"""
print("Writing files ...")
#for word in seglist:
#    file_save.write(word+" ")
sys.stdout = file_save
print(" ".join(seglist))
#sys.stdout = orig_stdout
print("Finished writing!")

#ret.close()
file_save.close()
"""

